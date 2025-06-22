using Microsoft.EntityFrameworkCore;
using ChatbotAPI.Models;

namespace ChatbotAPI.Data;

public class ChatbotDbContext : DbContext
{
    public ChatbotDbContext(DbContextOptions<ChatbotDbContext> options) : base(options)
    {
    }

    public DbSet<UserQuery> UserQueries { get; set; }
    public DbSet<ChatbotResponse> ChatbotResponses { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Configure UserQuery entity
        modelBuilder.Entity<UserQuery>(entity =>
        {
            entity.HasKey(e => e.QueryId);
            entity.Property(e => e.Question).IsRequired().HasMaxLength(2000);
            entity.Property(e => e.Timestamp).HasDefaultValueSql("CURRENT_TIMESTAMP");
            entity.Property(e => e.SessionId);
            entity.Property(e => e.Status).HasMaxLength(20).HasDefaultValue("Pending");
            
            // Create index on Timestamp
            entity.HasIndex(e => e.Timestamp);
            entity.HasIndex(e => e.SessionId);
        });

        // Configure ChatbotResponse entity
        modelBuilder.Entity<ChatbotResponse>(entity =>
        {
            entity.HasKey(e => e.ResponseId);
            entity.Property(e => e.Response).IsRequired();
            entity.Property(e => e.Timestamp).HasDefaultValueSql("CURRENT_TIMESTAMP");
            entity.Property(e => e.Status).HasMaxLength(20).HasDefaultValue("Success");
            entity.Property(e => e.ErrorMessage).HasMaxLength(500);
            
            // Foreign key relationship
            entity.HasOne(e => e.UserQuery)
                  .WithOne(e => e.Response)
                  .HasForeignKey<ChatbotResponse>(e => e.QueryId)
                  .OnDelete(DeleteBehavior.Cascade);
            
            // Create index on QueryId and Timestamp
            entity.HasIndex(e => e.QueryId);
            entity.HasIndex(e => e.Timestamp);
        });
    }
} 