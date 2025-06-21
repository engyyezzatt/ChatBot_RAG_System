using System.Text;
using System.Text.Json;
using ChatbotAPI.DTOs;
using Microsoft.Extensions.Options;

namespace ChatbotAPI.Services;

public class PythonBackendService : IPythonBackendService
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<PythonBackendService> _logger;
    private readonly JsonSerializerOptions _jsonOptions;

    public PythonBackendService(
        HttpClient httpClient,
        IOptions<PythonBackendConfig> config,
        ILogger<PythonBackendService> logger)
    {
        _httpClient = httpClient;
        _logger = logger;
        
        _httpClient.BaseAddress = new Uri(config.Value.BaseUrl);
        _httpClient.Timeout = TimeSpan.FromSeconds(config.Value.TimeoutSeconds);
        
        _jsonOptions = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
            PropertyNameCaseInsensitive = true
        };
    }

    public async Task<PythonChatResponse> SendChatRequestAsync(string question)
    {
        try
        {
            _logger.LogInformation("Sending chat request to Python backend: {Question}", question);
            _logger.LogInformation("Python backend URL: {BaseUrl}", _httpClient.BaseAddress);
            
            var request = new PythonChatRequest { Question = question };
            var json = JsonSerializer.Serialize(request, _jsonOptions);
            var content = new StringContent(json, Encoding.UTF8, "application/json");
            
            _logger.LogInformation("Sending POST request to /chat endpoint...");
            var response = await _httpClient.PostAsync("/chat", content);
            
            _logger.LogInformation("Received response from Python backend. Status: {StatusCode}", response.StatusCode);
            
            response.EnsureSuccessStatusCode();
            
            var responseContent = await response.Content.ReadAsStringAsync();
            _logger.LogInformation("Response content length: {Length} characters", responseContent.Length);
            
            var chatResponse = JsonSerializer.Deserialize<PythonChatResponse>(responseContent, _jsonOptions);
            
            if (chatResponse == null)
            {
                throw new InvalidOperationException("Failed to deserialize response from Python backend");
            }
            
            _logger.LogInformation("Successfully received response from Python backend");
            return chatResponse;
        }
        catch (TaskCanceledException ex) when (ex.InnerException is TimeoutException)
        {
            _logger.LogError(ex, "Timeout occurred while communicating with Python backend after {Timeout} seconds", _httpClient.Timeout.TotalSeconds);
            throw new InvalidOperationException($"Python backend request timed out after {_httpClient.Timeout.TotalSeconds} seconds. Please check if the Python backend is running and responding.", ex);
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "HTTP error occurred while communicating with Python backend");
            
            // Provide a fallback response for testing when Python backend is not available
            _logger.LogWarning("Python backend not available, providing fallback response for testing");
            return new PythonChatResponse
            {
                Response = "This is a fallback response from the .NET API because the Python backend is not available. The Python backend needs to be running for full RAG functionality.",
                Sources = new List<string> { "Fallback Response" }
            };
        }
        catch (JsonException ex)
        {
            _logger.LogError(ex, "JSON deserialization error from Python backend response");
            throw new InvalidOperationException("Invalid response format from Python backend", ex);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unexpected error occurred while communicating with Python backend");
            throw;
        }
    }

    public async Task<PythonHealthResponse> GetHealthStatusAsync()
    {
        try
        {
            _logger.LogInformation("Checking Python backend health status at {BaseUrl}", _httpClient.BaseAddress);
            
            var response = await _httpClient.GetAsync("/health");
            response.EnsureSuccessStatusCode();
            
            var responseContent = await response.Content.ReadAsStringAsync();
            var healthResponse = JsonSerializer.Deserialize<PythonHealthResponse>(responseContent, _jsonOptions);
            
            if (healthResponse == null)
            {
                throw new InvalidOperationException("Failed to deserialize health response from Python backend");
            }
            
            _logger.LogInformation("Python backend health status: {Status}", healthResponse.Status);
            return healthResponse;
        }
        catch (TaskCanceledException ex) when (ex.InnerException is TimeoutException)
        {
            _logger.LogError(ex, "Timeout occurred while checking Python backend health");
            throw new InvalidOperationException("Python backend health check timed out. Please check if the Python backend is running.", ex);
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "HTTP error occurred while checking Python backend health");
            
            // Provide a fallback health response for testing
            _logger.LogWarning("Python backend not available, providing fallback health response for testing");
            return new PythonHealthResponse
            {
                Status = "unavailable",
                VectorStoreStatus = "unavailable",
                Error = "Python backend is not running"
            };
        }
        catch (JsonException ex)
        {
            _logger.LogError(ex, "JSON deserialization error from Python backend health response");
            throw new InvalidOperationException("Invalid health response format from Python backend", ex);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unexpected error occurred while checking Python backend health");
            throw;
        }
    }
}

public class PythonBackendConfig
{
    public string BaseUrl { get; set; } = "http://localhost:8000";
    public int TimeoutSeconds { get; set; } = 60; // Increased from 30 to 60 seconds
} 