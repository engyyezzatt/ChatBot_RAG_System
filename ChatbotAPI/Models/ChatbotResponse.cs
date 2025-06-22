using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ChatbotAPI.Models;

[Table("ChatbotResponses")]
public class ChatbotResponse
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int ResponseId { get; set; }
    
    [Required]
    public int QueryId { get; set; }
    
    [Required]
    public string Response { get; set; } = string.Empty;
    
    [DatabaseGenerated(DatabaseGeneratedOption.Computed)]
    public DateTime Timestamp { get; set; }
    
    public double? ProcessingTimeSeconds { get; set; }
    
    public string? Sources { get; set; } // JSON array of source documents
    
    [MaxLength(20)]
    public string Status { get; set; } = "Success";
    
    [MaxLength(500)]
    public string? ErrorMessage { get; set; }
    
    // Navigation property
    [ForeignKey("QueryId")]
    public virtual UserQuery UserQuery { get; set; } = null!;
} 