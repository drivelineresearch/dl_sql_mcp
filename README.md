# DL SQL MCP for Claude Desktop

🚀 **One-Click Installation** - Ask any question about baseball biomechanics data in natural language!

## Quick Setup for Trainers

### Step 1: Add to Claude Desktop
Copy this into your Claude Desktop settings (Settings → MCP):

```json
"dl-sql-mcp": {
  "command": "uvx",
  "args": ["--from", "git+https://github.com/drivelineresearch/dl_sql_mcp", "dl-sql-mcp"]
}
```

### Step 2: Set Database Credentials
Create a `.env` file in your home directory with:
```
DB_HOST=10.200.200.107
DB_USER=readonlyuser  
DB_PASSWORD=your_password_here
```

### Step 3: Start Asking Questions!
That's it! You can now ask Claude:

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

**Connection Issues?**
- Check your `.env` file has correct database credentials
- Ensure you're on the network that can reach the database

**Installation Problems?**
- Make sure you have Python 3.10+ installed
- Try restarting Claude Desktop after adding the configuration

**Questions Not Working?**
- Be specific about player names and what you want to analyze
- Try simpler questions first, then build up complexity

## Support

For help with setup or questions about the data:
- Contact your technical administrator
- Check the database connection is working
- Verify player names exist in the system

---

**Powered by Driveline Baseball Research & Development**