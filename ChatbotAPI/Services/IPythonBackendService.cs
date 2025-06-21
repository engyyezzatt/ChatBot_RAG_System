using ChatbotAPI.DTOs;

namespace ChatbotAPI.Services;

public interface IPythonBackendService
{
    Task<PythonChatResponse> SendChatRequestAsync(string question);
    Task<PythonHealthResponse> GetHealthStatusAsync();
} 