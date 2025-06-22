using ChatbotAPI.Data;
using ChatbotAPI.Services;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllers();

// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Configure CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowSpecificOrigins", policy =>
    {
        var allowedOrigins = builder.Configuration.GetSection("Cors:AllowedOrigins").Get<string[]>() ?? new string[0];
        policy.WithOrigins(allowedOrigins)
              .AllowAnyMethod()
              .AllowAnyHeader()
              .AllowCredentials();
    });
});

// Configure Entity Framework with SQLite
var dbPath = Path.GetFullPath(Path.Combine(builder.Environment.ContentRootPath, "..", "Database", "ChatbotDB.db"));
builder.Services.AddDbContext<ChatbotDbContext>(options =>
    options.UseSqlite($"Data Source={dbPath}"));

// Configure Python Backend Service
builder.Services.Configure<PythonBackendConfig>(
    builder.Configuration.GetSection("PythonBackend"));

builder.Services.AddHttpClient<IPythonBackendService, PythonBackendService>();

// Register application services
builder.Services.AddScoped<IChatService, ChatService>();

// Configure logging
builder.Services.AddLogging(logging =>
{
    logging.ClearProviders();
    logging.AddConsole();
    logging.AddDebug();
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

// Use CORS
app.UseCors("AllowSpecificOrigins");

app.UseAuthorization();

app.MapControllers();

// Health check endpoint
app.MapGet("/", () => new
{
    message = "Chatbot API",
    version = "1.0.0",
    endpoints = new
    {
        chat = "/api/chat",
        health = "/api/health",
        swagger = "/swagger"
    }
});

// Ensure database is created
using (var scope = app.Services.CreateScope())
{
    var context = scope.ServiceProvider.GetRequiredService<ChatbotDbContext>();
    try
    {
        context.Database.EnsureCreated();
        Console.WriteLine("SQLite database created successfully or already exists.");
        
        var connection = context.Database.GetDbConnection();
        Console.WriteLine($"Database file location: {connection.DataSource}");
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Error creating database: {ex.Message}");
    }
}

app.Run(); 