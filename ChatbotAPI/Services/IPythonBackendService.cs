using ChatbotAPI.DTOs;

namespace ChatbotAPI.Services;

public interface IPythonBackendService
{
    Task<PythonChatResponse> SendChatRequestAsync(string question, Guid sessionId);
    Task<PythonHealthResponse> GetHealthStatusAsync();
} 