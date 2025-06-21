using System.Text.Json.Serialization;

namespace ChatbotAPI.DTOs;

// Models for communication with Python backend
public class PythonChatRequest
{
    [JsonPropertyName("question")]
    public string Question { get; set; } = string.Empty;
}

public class PythonChatResponse
{
    [JsonPropertyName("response")]
    public string Response { get; set; } = string.Empty;
    
    [JsonPropertyName("timestamp")]
    public DateTime Timestamp { get; set; }
    
    [JsonPropertyName("sources")]
    public List<string>? Sources { get; set; }
}

public class PythonHealthResponse
{
    [JsonPropertyName("status")]
    public string Status { get; set; } = string.Empty;
    
    [JsonPropertyName("timestamp")]
    public DateTime Timestamp { get; set; }
    
    [JsonPropertyName("vector_store_status")]
    public string VectorStoreStatus { get; set; } = string.Empty;
} 