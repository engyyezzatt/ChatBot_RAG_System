using System.ComponentModel.DataAnnotations;

namespace ChatbotAPI.DTOs;

public class ChatRequestDto
{
    [Required]
    [StringLength(2000, MinimumLength = 1, ErrorMessage = "Question must be between 1 and 2000 characters")]
    public string Question { get; set; } = string.Empty;
    
    public Guid? SessionId { get; set; }
    
    
} 