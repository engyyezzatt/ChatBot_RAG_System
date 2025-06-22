#!/usr/bin/env python3
"""
SQLite Database Viewer for Chatbot API
This script allows you to view the contents of the ChatbotDB.db file
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any
import os

class DatabaseViewer:
    def __init__(self, db_path: str = None):
        # Look for the database file in the Database directory
        if db_path is None:
            # Try to find the database file relative to this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(script_dir, "..", "Database", "ChatbotDB.db")
        
        self.db_path = db_path
    
    def connect(self):
        """Connect to the SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # This allows column access by name
            return conn
        except Exception as e:
            print(f"❌ Error connecting to database: {e}")
            return None
    
    def get_table_info(self) -> Dict[str, int]:
        """Get information about tables and their row counts"""
        conn = self.connect()
        if not conn:
            return {}
        
        try:
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            table_info = {}
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                table_info[table_name] = count
            
            return table_info
        except Exception as e:
            print(f"❌ Error getting table info: {e}")
            return {}
        finally:
            conn.close()
    
    def view_user_queries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """View recent user queries"""
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT QueryId, Question, Timestamp, SessionId, Status
                FROM UserQueries 
                ORDER BY Timestamp DESC 
                LIMIT ?
            """, (limit,))
            
            queries = []
            for row in cursor.fetchall():
                queries.append({
                    'QueryId': row['QueryId'],
                    'Question': row['Question'],
                    'Timestamp': row['Timestamp'],
                    'SessionId': row['SessionId'],
                    'Status': row['Status']
                })
            
            return queries
        except Exception as e:
            print(f"❌ Error viewing user queries: {e}")
            return []
        finally:
            conn.close()
    
    def view_chatbot_responses(self, limit: int = 10) -> List[Dict[str, Any]]:
        """View recent chatbot responses"""
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ResponseId, QueryId, Response, Timestamp, ProcessingTimeSeconds, Sources, Status, ErrorMessage
                FROM ChatbotResponses 
                ORDER BY Timestamp DESC 
                LIMIT ?
            """, (limit,))
            
            responses = []
            for row in cursor.fetchall():
                responses.append({
                    'ResponseId': row['ResponseId'],
                    'QueryId': row['QueryId'],
                    'Response': row['Response'][:100] + "..." if len(row['Response']) > 100 else row['Response'],
                    'Timestamp': row['Timestamp'],
                    'ProcessingTimeSeconds': row['ProcessingTimeSeconds'],
                    'Sources': row['Sources'],
                    'Status': row['Status'],
                    'ErrorMessage': row['ErrorMessage']
                })
            
            return responses
        except Exception as e:
            print(f"❌ Error viewing chatbot responses: {e}")
            return []
        finally:
            conn.close()
    
    def view_conversation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """View conversation history with both queries and responses"""
        conn = self.connect()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    q.QueryId,
                    q.Question,
                    q.Timestamp AS QuestionTimestamp,
                    q.SessionId,
                    r.Response,
                    r.Timestamp AS ResponseTimestamp,
                    r.ProcessingTimeSeconds,
                    r.Sources,
                    r.Status AS ResponseStatus
                FROM UserQueries q
                LEFT JOIN ChatbotResponses r ON q.QueryId = r.QueryId
                ORDER BY q.Timestamp DESC 
                LIMIT ?
            """, (limit,))
            
            conversations = []
            for row in cursor.fetchall():
                conversations.append({
                    'QueryId': row['QueryId'],
                    'Question': row['Question'],
                    'QuestionTimestamp': row['QuestionTimestamp'],
                    'SessionId': row['SessionId'],
                    'Response': row['Response'][:100] + "..." if row['Response'] and len(row['Response']) > 100 else row['Response'],
                    'ResponseTimestamp': row['ResponseTimestamp'],
                    'ProcessingTimeSeconds': row['ProcessingTimeSeconds'],
                    'Sources': row['Sources'],
                    'ResponseStatus': row['ResponseStatus']
                })
            
            return conversations
        except Exception as e:
            print(f"❌ Error viewing conversation history: {e}")
            return []
        finally:
            conn.close()
    
    def print_database_summary(self):
        """Print a summary of the database contents"""
        print("=" * 80)
        print("📊 CHATBOT DATABASE SUMMARY")
        print("=" * 80)
        
        # Get table info
        table_info = self.get_table_info()
        if not table_info:
            print("❌ Could not connect to database or database is empty")
            print(f"   Tried to connect to: {self.db_path}")
            print("   Make sure the .NET API has been run at least once to create the database.")
            return
        
        print(f"📁 Database file: {self.db_path}")
        print(f"📋 Tables found: {len(table_info)}")
        print()
        
        for table_name, count in table_info.items():
            print(f"   📄 {table_name}: {count} records")
        
        print()
        
        # Show recent conversations
        conversations = self.view_conversation_history(5)
        if conversations:
            print("🔄 RECENT CONVERSATIONS:")
            print("-" * 80)
            for i, conv in enumerate(conversations, 1):
                print(f"{i}. Query ID: {conv['QueryId']}")
                print(f"   Question: {conv['Question']}")
                print(f"   Asked: {conv['QuestionTimestamp']}")
                if conv['Response']:
                    print(f"   Response: {conv['Response']}")
                    print(f"   Processing Time: {conv['ProcessingTimeSeconds']}ms")
                    print(f"   Status: {conv['ResponseStatus']}")
                else:
                    print("   Response: Pending")
                print()
        else:
            print("📝 No conversations found in database")
        
        print("=" * 80)

def main():
    """Main function to view database"""
    viewer = DatabaseViewer()
    
    try:
        viewer.print_database_summary()
        
        # Interactive menu
        while True:
            print("\n🔍 What would you like to view?")
            print("1. Database Summary")
            print("2. Recent User Queries (10)")
            print("3. Recent Chatbot Responses (10)")
            print("4. Conversation History (10)")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                viewer.print_database_summary()
            elif choice == "2":
                queries = viewer.view_user_queries(10)
                print("\n📝 RECENT USER QUERIES:")
                print("-" * 60)
                for i, query in enumerate(queries, 1):
                    print(f"{i}. ID: {query['QueryId']} | {query['Question'][:50]}...")
                    print(f"   Time: {query['Timestamp']} | Status: {query['Status']}")
                    print()
            elif choice == "3":
                responses = viewer.view_chatbot_responses(10)
                print("\n🤖 RECENT CHATBOT RESPONSES:")
                print("-" * 60)
                for i, response in enumerate(responses, 1):
                    print(f"{i}. ID: {response['ResponseId']} | Query: {response['QueryId']}")
                    print(f"   Response: {response['Response']}")
                    print(f"   Time: {response['Timestamp']} | Status: {response['Status']}")
                    print()
            elif choice == "4":
                conversations = viewer.view_conversation_history(10)
                print("\n🔄 CONVERSATION HISTORY:")
                print("-" * 60)
                for i, conv in enumerate(conversations, 1):
                    print(f"{i}. Query: {conv['Question'][:50]}...")
                    if conv['Response']:
                        print(f"   Response: {conv['Response']}")
                        print(f"   Processing: {conv['ProcessingTimeSeconds']}ms")
                    else:
                        print("   Response: Pending")
                    print()
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main() 