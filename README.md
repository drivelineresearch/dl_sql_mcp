# DL SQL MCP for Claude Desktop

🚀 **Easy Installation** - Ask any question about baseball biomechanics data in natural language!

## Complete Beginner Installation Guide

### For People With ZERO Technical Knowledge

### STEP 1: Install uv (5 minutes)

**If you have Windows:**
1. Press `Windows Key + R` on your keyboard
2. Type `powershell` and press Enter
3. A blue window will open (this is PowerShell)
4. Copy and paste this EXACT text:
   ```
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
5. Press Enter and wait (it will download and install automatically)
6. Close the blue window when it's done

**If you have Mac:**
1. Press `Command + Space` on your keyboard
2. Type `terminal` and press Enter
3. A black window will open (this is Terminal)
4. Copy and paste this EXACT text:
   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
5. Press Enter and wait (it will download and install automatically)
6. Close the black window when it's done

### STEP 2: Add to Claude Desktop (2 minutes)

1. Open Claude Desktop (the app on your computer)
2. Click the gear icon ⚙️ in the bottom left corner
3. Click "MCP" in the menu that appears
4. You'll see a text box - copy and paste this EXACT text:
   ```json
   "dl-sql-mcp": {
     "command": "uv",
     "args": ["tool", "run", "--from", "https://github.com/drivelineresearch/dl_sql_mcp/archive/refs/heads/master.zip", "dl-sql-mcp"]
   }
   ```
5. Click "Save" or "Apply"
6. Close Claude Desktop completely
7. Re-open Claude Desktop

### STEP 3: Set Your Database Password (2 minutes)

1. Start a conversation with Claude Desktop
2. Claude will automatically create a configuration file
3. **On Windows:** Press `Windows Key + R`, type `%APPDATA%\dl-sql-mcp` and press Enter
4. **On Mac:** Press `Command + Space`, type `~/Library/Application\ Support/dl-sql-mcp` and press Enter
5. You'll see a file called `.env` - double-click it
6. Change `CHANGE_THIS_TO_YOUR_ACTUAL_PASSWORD` to your real database password
7. Save the file (Ctrl+S on Windows, Cmd+S on Mac)
8. Close Claude Desktop and re-open it

### STEP 4: Test It Works (30 seconds)

Ask Claude: **"Show me all players in the database"**

If it works, you're done! If not, contact IT support.

---

## What Did We Just Do?

- **Step 1:** Installed a tool that can download and run programs from the internet
- **Step 2:** Told Claude Desktop where to find your baseball data program
- **Step 3:** Gave the program your database password so it can access your data
- **Step 4:** Tested that everything works

**Total Time:** 10 minutes maximum

## Now You Can Ask Questions Like:

## Example Questions

### Player Analysis
- *"Show me John Smith's velocity progression over his last 5 sessions"*
- *"How does Sarah's bat speed compare to team average?"*
- *"Find Mike's best throwing session this month"*

### Comparative Analysis
- *"Compare shoulder rotation between our pitchers and catchers"*
- *"Which hitters have the most consistent attack angles?"*
- *"Show velocity differences between age groups"*

### Mechanical Analysis
- *"Find correlations between stride length and velocity"*
- *"Show players with improving hip-shoulder separation"*
- *"Analyze timing patterns in our most successful hitters"*

### Team Analytics
- *"What's the average exit velocity by position?"*
- *"Show velocity distribution across all our pitchers"*
- *"Find outliers in elbow stress measurements"*

### Progress Tracking
- *"Track velocity changes over the season"*
- *"Show improvement patterns after our training program"*
- *"Identify any declining performance metrics"*

## What Data is Available?

### Pitching Metrics (47+ measurements)
- **Performance**: Velocity, timing, accuracy
- **Mechanics**: Stride length, arm slot, joint angles
- **Kinetic Chain**: Hip-shoulder separation, timing sequences
- **Forces**: Elbow stress, shoulder stress
- **Energy**: Transfer, generation, absorption

### Hitting Metrics (50+ measurements)  
- **Performance**: Exit velocity, bat speed, attack angle
- **Body Mechanics**: Pelvis/torso angles throughout swing
- **Hand/Arm**: Speed at all swing phases
- **Rotational Power**: Peak angular velocities
- **Contact**: Sweet spot velocity, contact position

## No SQL Knowledge Required!

The system automatically:
- ✅ Finds players by name (partial matching)
- ✅ Joins across all related tables
- ✅ Handles time-based queries
- ✅ Calculates averages and trends
- ✅ Formats results for easy reading

## Troubleshooting

### Common Issues and Solutions

**🔧 Claude Desktop Won't Start After Adding MCP Server**
1. **Close Claude Desktop completely** (quit the application)
2. **Re-open Claude Desktop** - it should create the `.env` file automatically
3. If it still crashes, check the logs:
   - **Windows:** `%APPDATA%\Claude\Logs\mcp-server-dl-sql-mcp.log`
   - **Mac:** `/Users/YOUR_USERNAME/Library/Logs/Claude/mcp-server-dl-sql-mcp.log`

**📁 Can't Find the .env File?**
- **On Windows:** Press `Windows Key + R`, type `%APPDATA%\dl-sql-mcp` and press Enter
- **On Mac:** Press `Command + Space`, type `~/Library/Application\ Support/dl-sql-mcp` and press Enter
- **In Windows Explorer:** Show hidden files (View → Hidden items)
- **In Mac Finder:** Press `Command + Shift + .` (period) to show hidden files
- **Alternative commands:**
  - **Windows:** `explorer %APPDATA%\dl-sql-mcp`
  - **Mac:** `open ~/Library/Application\ Support/dl-sql-mcp`
- If the folder doesn't exist, restart Claude Desktop once more

**🔗 Database Connection Issues**
- **"Can't connect to MySQL server"** error:
  1. Connect to your organization's VPN first
  2. Verify you can reach the database server:
     - **Windows:** `ping 10.200.200.107` in Command Prompt
     - **Mac:** `ping 10.200.200.107` in Terminal
  3. Check your `.env` file has the correct password (not `CHANGE_THIS_TO_YOUR_ACTUAL_PASSWORD`)
  4. Contact IT support if network issues persist

**🔄 How Many Times to Restart Claude Desktop?**
- **After adding MCP config:** Restart once to create `.env` file
- **After editing password:** Restart once to pick up new credentials
- **If still having issues:** Restart one more time after VPN connection
- **Total expected restarts:** 2-3 times maximum

**⚠️ Server Keeps Disconnecting**
- Check you're connected to the correct network/VPN
- Verify your database credentials are correct
- Look for "Successfully connected" messages in the logs
- If you see "TaskGroup" errors, try restarting Claude Desktop

**🐛 Still Having Problems?**
1. **Check the logs:**
   - **Windows:** `%APPDATA%\Claude\Logs\mcp-server-dl-sql-mcp.log`
   - **Mac:** `/Users/YOUR_USERNAME/Library/Logs/Claude/mcp-server-dl-sql-mcp.log`
2. **Look for these success messages:**
   - "Created config file at: ..."
   - "Successfully connected to theia_pitching_db!"
   - "Successfully connected to theia_hitting_db!"
3. **Common error patterns:**
   - "Database password not configured" → Edit your `.env` file
   - "Can't connect to MySQL server" → Check VPN connection
   - "Request timed out" → Restart Claude Desktop

**📞 Need Help?**
- Contact your technical administrator
- Include the contents of your log file when reporting issues
- Verify player names exist in the system before querying

## Support

For help with setup or questions about the data:
- Contact your technical administrator
- Check the database connection is working
- Verify player names exist in the system

---

**Powered by Driveline Baseball Research & Development**