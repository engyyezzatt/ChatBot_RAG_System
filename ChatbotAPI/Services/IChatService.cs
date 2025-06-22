using ChatbotAPI.DTOs;

namespace ChatbotAPI.Services;

public interface IChatService
{
    Task<ChatResponseDto> ProcessChatRequestAsync(ChatRequestDto request);
    Task<IEnumerable<ChatResponseDto>> GetConversationHistoryAsync(Guid? sessionId = null, int limit = 50);
} 