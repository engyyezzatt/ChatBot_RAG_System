namespace ChatbotAPI.DTOs;

public class ChatResponseDto
{
    public int QueryId { get; set; }
    public string Question { get; set; } = string.Empty;
    public string Response { get; set; } = string.Empty;
    public DateTime QuestionTimestamp { get; set; }
    public DateTime ResponseTimestamp { get; set; }
    public int? ProcessingTimeMs { get; set; }
    public List<string>? Sources { get; set; }
    public string Status { get; set; } = "Success";
    public string? ErrorMessage { get; set; }
} 