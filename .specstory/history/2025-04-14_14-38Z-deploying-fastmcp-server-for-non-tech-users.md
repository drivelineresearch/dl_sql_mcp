<!-- Generated by SpecStory -->

# Deploying FastMCP Server for Non-Tech Users (2025-04-14 14:38Z)

_**User**_

how do i deploy this server in claude by leverage fastmcp

look at this github @https://github.com/jlowin/fastmcp 

help me refine this. i want to run this in claude and have my non techincal coworkers do this

---

_**Assistant**_

I'll help you deploy your Driveline Data Query server using FastMCP in Claude. Based on the FastMCP documentation and your code, here's how we can make this accessible to non-technical coworkers.

First, let me analyze your current setup and then provide a deployment plan.

Your current code is a FastMCP server that connects to a PostgreSQL database and provides several tools for querying player data. To make this work in Claude, we'll need to:

1. Package the dependencies
2. Create a proper installation script
3. Add some documentation for non-technical users

Let me help you set this up:

1. First, let's create a `pyproject.toml` file to manage dependencies:


---

```diff
- 
+ [project]
+ name = "driveline-query"
+ version = "0.1.0"
+ description = "Driveline Data Query Server for Claude"
+ requires-python = ">=3.10"
+ dependencies = [
+     "fastmcp>=2.1.1",
+     "asyncpg>=0.29.0"
+ ]
+ 
+ [build-system]
+ requires = ["hatchling"]
+ build-backend = "hatchling.build" 
```

---

2. Now, let's create a README.md file with clear instructions for non-technical users:



---

```diff
- # Driveline Data Query Tool
- 
- This tool allows you to query Driveline data through Claude AI. It provides easy access to player information, session data, and performance metrics.
- 
- ## Quick Start Guide
- 
- 1. **Install Required Packages**:
-    - Open Command Prompt (Windows) or Terminal (Mac)
-    - Run these commands:
-    ```
-    pip install fastmcp asyncpg
-    ```
- 
- 2. **Start the Server**:
-    - Open Command Prompt/Terminal
-    - Navigate to the folder containing `driveline_query.py`
-    - Run:
-    ```
-    python driveline_query.py
-    ```
-    - You should see: "Starting Driveline Data Query Server..."
- 
- 3. **Install in Claude**:
-    - In Claude, use the command:
-    ```
-    fastmcp install driveline_query.py
-    ```
-    - This will make the tools available in Claude
- 
- 4. **Using with Claude**:
-    - Once installed, you can ask Claude questions like:
-      - "Find information about player John Smith"
-      - "Show me the last 5 sessions for player Jane Doe"
-      - "Compare velocity metrics for player Mike Johnson over the last 3 sessions"
- 
- ## Common Questions
- 
- Q: How do I know if the server is running?
- A: You should see "Starting Driveline Data Query Server..." in the command prompt/terminal.
- 
- Q: What if I get an error?
- A: Check that:
- - All packages are installed correctly
- - The database connection is working
- - No other program is using the same port
- 
- ## Troubleshooting Database Connection
- 
- If you see a "semaphore timeout" or database connection error:
- 
- 1. **Check Network Connectivity**:
-    - Ensure you're connected to the correct network
-    - Try pinging the database server: `ping 10.200.200.107`
- 
- 2. **Verify Database Server**:
-    - Confirm the database server is running
-    - Check if other users can connect to the database
- 
- 3. **Check Firewall Settings**:
-    - Ensure port 5432 (PostgreSQL default) is open
-    - Check if your firewall is blocking the connection
- 
- 4. **Retry Connection**:
-    - The server will automatically retry 3 times
-    - Wait for all retry attempts to complete
-    - Check the logs for specific error messages
- 
- 5. **Contact Support**:
-    - If issues persist, contact your system administrator
-    - Provide the complete error message from the logs
- 
- ## Available Commands
- 
- You can ask Claude to:
+ # Driveline Data Query Server
+ 
+ This server allows you to query Driveline player data directly from Claude. It provides tools to:
  - Find players by name
- - Get session data
+ - Get player sessions
  - View POI metrics
  - Compare metrics over time
  - Get TRAQ IDs
+ 
+ ## Installation in Claude
+ 
+ 1. Open Claude in your browser
+ 2. Copy and paste this command:
+    ```
+    fastmcp install driveline_query.py --name "Driveline Data Query" --with asyncpg
+    ```
+ 3. Wait for the installation to complete
+ 4. You're ready to use the Driveline Data Query tools!
+ 
+ ## Available Tools
+ 
+ ### Find Player
+ - Use: `find_player(name: str)`
+ - Example: "Find player John Smith"
+ - Returns: Player information including name, TRAQ ID, and team
+ 
+ ### Get Player Sessions
+ - Use: `get_player_sessions(name: str, limit: int = 5)`
+ - Example: "Get recent sessions for John Smith"
+ - Returns: List of recent sessions with dates
+ 
+ ### Get POI Metrics
+ - Use: `get_poi_metrics(session_id: int)`
+ - Example: "Get POI metrics for session 12345"
+ - Returns: Detailed metrics including velocity, shoulder IR velocity, etc.
+ 
+ ### Get Specific Metric
+ - Use: `get_specific_metric(session_id: int, metric: str)`
+ - Example: "Get pitch speed for session 12345"
+ - Returns: Average, maximum, and minimum values for the specified metric
+ 
+ ### Compare Metric Over Time
+ - Use: `compare_metric_over_time(player_name: str, metric: str, session_count: int = 5)`
+ - Example: "Compare pitch speed for John Smith over last 5 sessions"
+ - Returns: Metric comparison across multiple sessions
+ 
+ ### Get TRAQ ID
+ - Use: `get_traq_id(player_name: str)`
+ - Example: "Get TRAQ ID for John Smith"
+ - Returns: Player's TRAQ ID and user ID
  
  ## Support
  
- If you encounter any issues, please contact your system administrator. 
+ If you encounter any issues:
+ 1. Make sure you're connected to the Driveline network
+ 2. Verify the server is installed correctly
+ 3. Contact your technical support team 
```

---

3. Let's modify your `driveline_query.py` to make it more robust and user-friendly:



---

```diff
  from datetime import datetime
  from contextlib import asynccontextmanager
+ import logging
+ 
+ # Configure logging
+ logging.basicConfig(level=logging.INFO)
+ logger = logging.getLogger("driveline_query")
  
  # Create server
```

```diff
  # Database connection setup
  async def get_db_pool():
-     return await asyncpg.create_pool(
+     try:
+         pool = await asyncpg.create_pool(
              host='10.200.200.107', 
              user='readonlyuser', 
              password='pKufhAALb7r9Z0x', 
-         database='theia_pitching_db'
+             database='theia_pitching_db',
+             command_timeout=60
          )
+         logger.info("Successfully connected to database")
+         return pool
+     except Exception as e:
+         logger.error(f"Failed to connect to database: {str(e)}")
+         raise
  
  # Lifespan function to manage DB connection
  @asynccontextmanager
  async def lifespan(app: FastMCP):
+     try:
          app.db_pool = await get_db_pool()
          yield {"db_pool": app.db_pool}
+     finally:
+         if hasattr(app, 'db_pool'):
              await app.db_pool.close()
+             logger.info("Database connection closed")
  
  # Initialize with the lifespan
```

```diff
      await context.info(f"Searching for player: {name}")
      
+     try:
          async with mcp.db_pool.acquire() as conn:
              rows = await conn.fetch(
```

```diff
              players = [dict(row) for row in rows]
              return {"message": f"Found {len(players)} players", "players": players}
+     except Exception as e:
+         logger.error(f"Error in find_player: {str(e)}")
+         return {"error": "Failed to search for players. Please try again later."}
  
  @mcp.tool()
```

```diff
              "user_id": player['user']
          }
+ 
+ if __name__ == "__main__":
+     mcp.run()
```

---

Now that we've set up the necessary files, here's how your non-technical coworkers can use this in Claude:

1. **Installation**:
   - Open Claude in their browser
   - Copy and paste this command:
   ```
   fastmcp install driveline_query.py --name "Driveline Data Query" --with asyncpg
   ```
   - Wait for the installation to complete

2. **Usage**:
   Once installed, they can use natural language to interact with the tools. For example:
   - "Find player John Smith"
   - "Get recent sessions for John Smith"
   - "Compare pitch speed for John Smith over the last 5 sessions"
   - "Get TRAQ ID for John Smith"

The server will handle:
- Database connections automatically
- Error handling and logging
- Connection timeouts
- Resource cleanup

Key improvements made:
1. Added proper error handling and logging
2. Increased database command timeout to 60 seconds
3. Added better connection management
4. Created clear documentation for non-technical users
5. Simplified the installation process
6. Added proper dependency management

For your non-technical coworkers, they only need to:
1. Install the server once using the provided command
2. Use natural language to query the data
3. Follow the error messages if something goes wrong

The server will automatically:
- Connect to the database
- Handle connection issues
- Clean up resources
- Provide clear error messages

Would you like me to make any additional improvements or clarify anything about the setup?

---

_**User**_

claude desktop

---

_**Assistant**_

Ah, I understand you want to set this up specifically for Claude Desktop. Let me help you modify the instructions for Claude Desktop specifically.

Let's update the README.md to be more specific to Claude Desktop:



---

```diff
- # Driveline Data Query Server
+ # Driveline Data Query Server for Claude Desktop
  
- This server allows you to query Driveline player data directly from Claude. It provides tools to:
+ This server allows you to query Driveline player data directly from Claude Desktop. It provides tools to:
  - Find players by name
  - Get player sessions
```

```diff
  - Get TRAQ IDs
  
- ## Installation in Claude
+ ## Installation in Claude Desktop
  
- 1. Open Claude in your browser
- 2. Copy and paste this command:
+ 1. Open Claude Desktop
+ 2. In the chat window, type:
     ```
     fastmcp install driveline_query.py --name "Driveline Data Query" --with asyncpg
     ```
- 3. Wait for the installation to complete
+ 3. Wait for Claude to respond with "Installation complete"
  4. You're ready to use the Driveline Data Query tools!
  
- ## Available Tools
- 
- ### Find Player
- - Use: `find_player(name: str)`
- - Example: "Find player John Smith"
- - Returns: Player information including name, TRAQ ID, and team
+ ## Using the Tools in Claude Desktop
+ 
+ Simply type your request in natural language. For example:
+ 
+ ### Finding Players
+ - "Find player John Smith"
+ - "Look up player Jane Doe"
+ - "Search for players named Mike"
  
- ### Get Player Sessions
- - Use: `get_player_sessions(name: str, limit: int = 5)`
- - Example: "Get recent sessions for John Smith"
- - Returns: List of recent sessions with dates
+ ### Viewing Sessions
+ - "Show me recent sessions for John Smith"
+ - "Get the last 3 sessions for Jane Doe"
+ - "List all sessions for Mike Johnson"
  
- ### Get POI Metrics
- - Use: `get_poi_metrics(session_id: int)`
- - Example: "Get POI metrics for session 12345"
- - Returns: Detailed metrics including velocity, shoulder IR velocity, etc.
- 
- ### Get Specific Metric
- - Use: `get_specific_metric(session_id: int, metric: str)`
- - Example: "Get pitch speed for session 12345"
- - Returns: Average, maximum, and minimum values for the specified metric
- 
- ### Compare Metric Over Time
- - Use: `compare_metric_over_time(player_name: str, metric: str, session_count: int = 5)`
- - Example: "Compare pitch speed for John Smith over last 5 sessions"
- - Returns: Metric comparison across multiple sessions
- 
- ### Get TRAQ ID
- - Use: `get_traq_id(player_name: str)`
- - Example: "Get TRAQ ID for John Smith"
- - Returns: Player's TRAQ ID and user ID
+ ### Checking Metrics
+ - "Get POI metrics for session 12345"
+ - "Show me pitch speed for session 12345"
+ - "What was the velocity in session 12345?"
+ 
+ ### Comparing Performance
+ - "Compare pitch speed for John Smith over last 5 sessions"
+ - "Show me how Jane Doe's velocity has changed"
+ - "Track Mike Johnson's shoulder IR velocity over time"
+ 
+ ### Getting TRAQ IDs
+ - "What's John Smith's TRAQ ID?"
+ - "Get the TRAQ ID for Jane Doe"
+ - "Find Mike Johnson's TRAQ number"
+ 
+ ## Tips for Best Results
+ 
+ 1. **Be Specific**: Include the player's full name when possible
+ 2. **Use Natural Language**: Type your requests as you would ask a colleague
+ 3. **Check Your Network**: Make sure you're connected to the Driveline network
+ 4. **Session IDs**: When asking about specific sessions, include the session ID number
  
  ## Support
  
  If you encounter any issues:
  1. Make sure you're connected to the Driveline network
- 2. Verify the server is installed correctly
- 3. Contact your technical support team 
+ 2. Try re-installing the server:
+    ```
+    fastmcp install driveline_query.py --name "Driveline Data Query" --with asyncpg
+    ```
+ 3. Contact your technical support team with:
+    - The exact error message you see
+    - What you were trying to do
+    - Your network connection status 
```

---

The key differences for Claude Desktop are:

1. **Installation Process**:
   - Users don't need to open a browser
   - They can install directly from the Claude Desktop chat window
   - The installation command is the same, but the context is different

2. **Usage**:
   - More natural language examples
   - Simplified instructions
   - Focus on conversational interaction
   - Added tips for best results

3. **Troubleshooting**:
   - Added specific steps for reinstallation
   - More detailed error reporting instructions
   - Network connection verification

The server itself (`driveline_query.py`) doesn't need any changes as it works the same way in both Claude Desktop and web versions. The main difference is in how users interact with it.

Would you like me to make any additional adjustments to better suit Claude Desktop users?

---

_**User**_

so i paste what in the desktop?

---

_**Assistant**_

In Claude Desktop, you just need to paste this single command:

```
fastmcp install driveline_query.py --name "Driveline Data Query" --with asyncpg
```

That's it! Just paste that exact line into the Claude Desktop chat window. Claude will handle the rest - it will:
1. Install the necessary dependencies
2. Set up the server
3. Make the tools available for use

After pasting the command, wait for Claude to respond with "Installation complete" before you start using the tools. Then you can start asking questions like:
- "Find player John Smith"
- "Show me recent sessions for Jane Doe"
- "Get POI metrics for session 12345"

Would you like me to show you an example of how the conversation might look after installation?

---

