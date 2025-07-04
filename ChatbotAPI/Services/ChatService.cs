using System.Text.Json;
using ChatbotAPI.Data;
using ChatbotAPI.DTOs;
using ChatbotAPI.Models;
using Microsoft.EntityFrameworkCore;

namespace ChatbotAPI.Services;

public class ChatService : IChatService
{
    private readonly ChatbotDbContext _context;
    private readonly IPythonBackendService _pythonBackendService;
    private readonly ILogger<ChatService> _logger;

    public ChatService(
        ChatbotDbContext context,
        IPythonBackendService pythonBackendService,
        ILogger<ChatService> logger)
    {
        _context = context;
        _pythonBackendService = pythonBackendService;
        _logger = logger;
    }

    public async Task<ChatResponseDto> ProcessChatRequestAsync(ChatRequestDto request)
    {
        var stopwatch = System.Diagnostics.Stopwatch.StartNew();
        
        try
        {
            _logger.LogInformation("Processing chat request: {Question}", request.Question);
            
            // 1. Save user query to database
            var userQuery = new UserQuery
            {
                Question = request.Question,
                SessionId = request.SessionId ?? Guid.NewGuid(),
                Status = "Processing"
            };
            
            _context.UserQueries.Add(userQuery);
            await _context.SaveChangesAsync();
            
            _logger.LogInformation("Saved user query to database with ID: {QueryId}", userQuery.QueryId);
            
            // 2. Send request to Python backend
            var pythonResponse = await _pythonBackendService.SendChatRequestAsync(request.Question, userQuery.SessionId);
            
            stopwatch.Stop();
            double processingTimeSeconds = stopwatch.Elapsed.TotalSeconds;
            
            // 3. Save chatbot response to database
            var chatbotResponse = new ChatbotResponse
            {
                QueryId = userQuery.QueryId,
                Response = pythonResponse.Response,
                ProcessingTimeSeconds = processingTimeSeconds,
                Sources = pythonResponse.Sources != null ? JsonSerializer.Serialize(pythonResponse.Sources) : null,
                Status = "Success"
            };
            
            _context.ChatbotResponses.Add(chatbotResponse);
            
            // Update user query status
            userQuery.Status = "Completed";
            
            await _context.SaveChangesAsync();
            
            _logger.LogInformation("Successfully processed chat request. Processing time: {ProcessingTimeSeconds}s", processingTimeSeconds);
            
            // 4. Return response DTO
            return new ChatResponseDto
            {
                QueryId = userQuery.QueryId,
                Question = userQuery.Question,
                Response = chatbotResponse.Response,
                QuestionTimestamp = userQuery.Timestamp,
                ResponseTimestamp = chatbotResponse.Timestamp,
                ProcessingTimeSeconds = chatbotResponse.ProcessingTimeSeconds,
                Sources = pythonResponse.Sources,
                Status = chatbotResponse.Status
            };
        }
        catch (Exception ex)
        {
            stopwatch.Stop();
            double processingTimeSeconds = stopwatch.Elapsed.TotalSeconds;
            
            _logger.LogError(ex, "Error processing chat request: {Question}", request.Question);
            
            // Update user query status to failed
            if (request.Question != null) // This should always be true due to validation
            {
                var userQuery = await _context.UserQueries
                    .FirstOrDefaultAsync(q => q.Question == request.Question && q.Status == "Processing");
                
                if (userQuery != null)
                {
                    userQuery.Status = "Failed";
                    
                    // Save error response
                    var errorResponse = new ChatbotResponse
                    {
                        QueryId = userQuery.QueryId,
                        Response = "Sorry, I encountered an error while processing your request. Please try again.",
                        ProcessingTimeSeconds = processingTimeSeconds,
                        Status = "Error",
                        ErrorMessage = ex.Message
                    };
                    
                    _context.ChatbotResponses.Add(errorResponse);
                    await _context.SaveChangesAsync();
                    
                    return new ChatResponseDto
                    {
                        QueryId = userQuery.QueryId,
                        Question = userQuery.Question,
                        Response = errorResponse.Response,
                        QuestionTimestamp = userQuery.Timestamp,
                        ResponseTimestamp = errorResponse.Timestamp,
                        ProcessingTimeSeconds = errorResponse.ProcessingTimeSeconds,
                        Status = errorResponse.Status,
                        ErrorMessage = errorResponse.ErrorMessage
                    };
                }
            }
            
            throw;
        }
    }

    public async Task<IEnumerable<ChatResponseDto>> GetConversationHistoryAsync(Guid? sessionId = null, int limit = 50)
    {
        try
        {
            var query = _context.UserQueries
                .Include(q => q.Response)
                .AsQueryable();
            
            if (sessionId.HasValue)
            {
                query = query.Where(q => q.SessionId == sessionId.Value);
            }
            
            var conversations = await query
                .OrderByDescending(q => q.Timestamp)
                .Take(limit)
                .ToListAsync();
            
            var result = conversations.Select(q => new ChatResponseDto
            {
                QueryId = q.QueryId,
                Question = q.Question,
                Response = q.Response != null ? q.Response.Response : string.Empty,
                QuestionTimestamp = q.Timestamp,
                ResponseTimestamp = q.Response != null ? q.Response.Timestamp : q.Timestamp,
                ProcessingTimeSeconds = q.Response != null ? q.Response.ProcessingTimeSeconds : null,
                Sources = q.Response != null && q.Response.Sources != null ? JsonSerializer.Deserialize<List<string>>(q.Response.Sources) : null,
                Status = q.Response != null ? q.Response.Status : "Pending",
                ErrorMessage = q.Response != null ? q.Response.ErrorMessage : null
            }).ToList();
            
            _logger.LogInformation("Retrieved {Count} conversation records", result.Count);
            return result;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving conversation history");
            throw;
        }
    }
} 