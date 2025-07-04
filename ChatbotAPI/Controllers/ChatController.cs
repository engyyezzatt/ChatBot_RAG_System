using Microsoft.AspNetCore.Mvc;
using ChatbotAPI.DTOs;
using ChatbotAPI.Services;
using ChatbotAPI.Data;
using Microsoft.EntityFrameworkCore;

namespace ChatbotAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ChatController : ControllerBase
{
    private readonly IChatService _chatService;
    private readonly ChatbotDbContext _context;
    private readonly ILogger<ChatController> _logger;

    public ChatController(IChatService chatService, ChatbotDbContext context, ILogger<ChatController> logger)
    {
        _chatService = chatService;
        _context = context;
        _logger = logger;
    }

    /// <summary>
    /// Process a chat request and return the AI response
    /// </summary>
    /// <param name="request">The chat request containing the user's question</param>
    /// <returns>The chatbot's response with metadata</returns>
    [HttpPost]
    public async Task<ActionResult<ChatResponseDto>> Chat([FromBody] ChatRequestDto request)
    {
        try
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            var userAgent = Request.Headers.UserAgent.ToString();
            _logger.LogInformation("Received chat request from {UserAgent}", userAgent);
            
            var response = await _chatService.ProcessChatRequestAsync(request);
            
            return Ok(response);
        }
        catch (InvalidOperationException ex)
        {
            _logger.LogError(ex, "Invalid operation during chat processing");
            return StatusCode(503, new { error = ex.Message });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unexpected error during chat processing");
            return StatusCode(500, new { error = "An unexpected error occurred while processing your request." });
        }
    }

    /// <summary>
    /// Test database connection and get database statistics
    /// </summary>
    /// <returns>Database statistics</returns>
    [HttpGet("db-stats")]
    public async Task<ActionResult<object>> GetDatabaseStats()
    {
        try
        {
            var userQueriesCount = await _context.UserQueries.CountAsync();
            var chatbotResponsesCount = await _context.ChatbotResponses.CountAsync();
            
            var recentQueries = await _context.UserQueries
                .OrderByDescending(q => q.Timestamp)
                .Take(5)
                .Select(q => new
                {
                    q.QueryId,
                    q.Question,
                    q.Timestamp,
                    q.Status
                })
                .ToListAsync();

            var recentResponses = await _context.ChatbotResponses
                .OrderByDescending(r => r.Timestamp)
                .Take(5)
                .Select(r => new
                {
                    r.ResponseId,
                    r.QueryId,
                    r.Response,
                    r.Timestamp,
                    r.ProcessingTimeSeconds,
                    r.Status
                })
                .ToListAsync();

            return Ok(new
            {
                database_status = "Connected",
                user_queries_count = userQueriesCount,
                chatbot_responses_count = chatbotResponsesCount,
                recent_queries = recentQueries,
                recent_responses = recentResponses
            });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting database statistics");
            return StatusCode(500, new { error = "Database connection failed", details = ex.Message });
        }
    }
} 