using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ChatbotAPI.Models;

[Table("UserQueries")]
public class UserQuery
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int QueryId { get; set; }
    
    [Required]
    [MaxLength(2000)]
    public string Question { get; set; } = string.Empty;
    
    [DatabaseGenerated(DatabaseGeneratedOption.Computed)]
    public DateTime Timestamp { get; set; }
    
    [MaxLength(100)]
    public string? SessionId { get; set; }
    
    [MaxLength(20)]
    public string Status { get; set; } = "Pending";
    
    // Navigation property
    public virtual ChatbotResponse? Response { get; set; }
} 