using Microsoft.AspNetCore.Mvc;
using ChatbotAPI.Services;
using ChatbotAPI.DTOs;

namespace ChatbotAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class HealthController : ControllerBase
{
    private readonly IPythonBackendService _pythonBackendService;
    private readonly ILogger<HealthController> _logger;

    public HealthController(IPythonBackendService pythonBackendService, ILogger<HealthController> logger)
    {
        _pythonBackendService = pythonBackendService;
        _logger = logger;
    }

    /// <summary>
    /// Check the health status of the .NET API and Python backend
    /// </summary>
    /// <returns>Health status information</returns>
    [HttpGet]
    public async Task<ActionResult<object>> GetHealth()
    {
        try
        {
            object healthStatus;

            try
            {
                var pythonHealth = await _pythonBackendService.GetHealthStatusAsync();
                healthStatus = new
                {
                    timestamp = DateTime.UtcNow,
                    dotnet_api = new
                    {
                        status = "healthy",
                        version = "1.0.0"
                    },
                    python_backend = new
                    {
                        status = pythonHealth.Status,
                        vector_store_status = pythonHealth.VectorStoreStatus
                    }
                };
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Python backend health check failed");
                healthStatus = new
                {
                    timestamp = DateTime.UtcNow,
                    dotnet_api = new
                    {
                        status = "healthy",
                        version = "1.0.0"
                    },
                    python_backend = new
                    {
                        status = "unhealthy",
                        vector_store_status = "unknown",
                        error = ex.Message
                    }
                };
            }

            return Ok(healthStatus);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Health check failed");
            return StatusCode(500, new { error = "Health check failed", details = ex.Message });
        }
    }
} 