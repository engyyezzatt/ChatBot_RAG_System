-- Chatbot Database Schema for SQL Server
-- This database stores user-chatbot interactions for the RAG chatbot system

-- Create database (SQL Server syntax)
CREATE DATABASE ChatbotDB;
GO

USE ChatbotDB;
GO

-- Create UserQueries table
CREATE TABLE UserQueries (
    QueryId INT IDENTITY(1,1) PRIMARY KEY,
    Question NVARCHAR(2000) NOT NULL,
    Timestamp DATETIME2 DEFAULT GETUTCDATE(),
    SessionId NVARCHAR(100) NULL, -- For tracking conversation sessions
    UserId NVARCHAR(100) NULL,    -- For future user authentication
    Status NVARCHAR(20) DEFAULT 'Pending' -- Pending, Processing, Completed, Failed
);
GO

-- Create ChatbotResponses table
CREATE TABLE ChatbotResponses (
    ResponseId INT IDENTITY(1,1) PRIMARY KEY,
    QueryId INT NOT NULL,
    Response NVARCHAR(MAX) NOT NULL,
    Timestamp DATETIME2 DEFAULT GETUTCDATE(),
    ProcessingTimeMs INT NULL, -- Time taken to process the request
    Sources NVARCHAR(MAX) NULL, -- JSON array of source documents
    Status NVARCHAR(20) DEFAULT 'Success', -- Success, Error
    ErrorMessage NVARCHAR(500) NULL,
    CONSTRAINT FK_ChatbotResponses_UserQueries FOREIGN KEY (QueryId) REFERENCES UserQueries(QueryId)
);
GO

-- Create indexes for better performance
CREATE INDEX IX_UserQueries_Timestamp ON UserQueries(Timestamp);
GO
CREATE INDEX IX_UserQueries_SessionId ON UserQueries(SessionId);
GO
CREATE INDEX IX_ChatbotResponses_QueryId ON ChatbotResponses(QueryId);
GO
CREATE INDEX IX_ChatbotResponses_Timestamp ON ChatbotResponses(Timestamp);
GO

-- Create a view for easy query-response retrieval
CREATE VIEW ConversationHistory AS
SELECT 
    q.QueryId,
    q.Question,
    q.Timestamp AS QuestionTimestamp,
    q.SessionId,
    q.UserId,
    r.Response,
    r.Timestamp AS ResponseTimestamp,
    r.ProcessingTimeMs,
    r.Sources,
    r.Status AS ResponseStatus
FROM UserQueries q
LEFT JOIN ChatbotResponses r ON q.QueryId = r.QueryId;
GO

-- Insert sample data for testing (optional - uncomment if needed)
/*
INSERT INTO UserQueries (Question, SessionId, UserId) 
VALUES ('What is the company leave policy?', 'session-001', 'user-001');

INSERT INTO ChatbotResponses (QueryId, Response, ProcessingTimeMs, Sources)
VALUES (1, 'Based on the HR policy document, employees are entitled to 20 days of annual leave per year.', 1500, '["HR_Policy_Dataset1.txt"]');
*/

PRINT 'ChatbotDB database and tables created successfully!';
GO 