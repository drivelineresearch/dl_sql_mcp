import aiomysql
from datetime import datetime
from .database import search_player, get_available_metrics
from .config import log_info, log_error
from .intelligent_query import execute_custom_sql, get_table_info, format_query_response
from .complete_schema import get_complete_schema_context, get_all_pitching_metrics, get_all_hitting_metrics, get_metric_by_name

def register_tools(mcp):
    """Register all MCP tools"""
    
    @mcp.tool()
    async def query_baseball_data(question: str) -> dict:
        """
        Ask any question about baseball biomechanics data in natural language.
        
        This tool uses AI to interpret your question and query the appropriate database.
        You can ask about players, metrics, comparisons, trends, or any analysis.
        
        Examples:
        - "What was John Smith's average velocity last month?"
        - "Show me the top 5 players by exit velocity"
        - "How has Sarah's bat speed improved over time?"
        - "Compare pitcher shoulder rotation between age groups"
        - "Find all sessions where velocity increased more than 5 mph"
        
        Args:
            question: Your question in natural language
            
        Returns:
            Analysis results based on your question
        """
        log_info(f"Processing intelligent query: {question}")
        
        if not mcp.db_pools:
            return {"error": "Database connection not available"}
        
        # Provide the LLM with complete comprehensive context
        schema_context = get_complete_schema_context()
        
        # Available databases
        available_dbs = [db for db in ["theia_pitching_db", "theia_hitting_db"] if db in mcp.db_pools]
        
        response = {
            "question": question,
            "schema_context": schema_context,
            "available_databases": available_dbs,
            "instructions": """
            Based on the question and schema context above, you should:
            
            1. Determine which database(s) to query (pitching vs hitting)
            2. Identify the specific tables and columns needed
            3. Generate appropriate SQL query(ies)
            4. Use the execute_sql tool to run your query
            5. Format the results to answer the original question
            
            Key guidelines:
            - Always JOIN through the relationship chain: users → sessions → trials → poi
            - Use LIKE '%name%' for player name matching
            - Group by date/session for trends over time
            - Use AVG() for performance averages
            - Add appropriate LIMIT clauses for large result sets
            
            The execute_sql tool will handle the actual database execution.
            """,
            "next_step": "Use execute_sql tool with your generated SQL query"
        }
        
        return response

    @mcp.tool()
    async def execute_sql(sql_query: str, database: str = "theia_pitching_db", limit: int = 100) -> dict:
        """
        Execute a custom SQL query on the baseball database.
        
        Use this after query_baseball_data to run the SQL you generate.
        
        Args:
            sql_query: The SQL query to execute
            database: Database name ("theia_pitching_db" or "theia_hitting_db")
            limit: Maximum number of results to return (default 100)
            
        Returns:
            Query results formatted for analysis
        """
        log_info(f"Executing SQL query on {database}")
        
        result = await execute_custom_sql(sql_query, database, mcp.db_pools, limit)
        
        if "error" not in result:
            log_info(f"SQL query successful, returned {result.get('result_count', 0)} rows")
        
        return result

    @mcp.tool()
    async def get_database_schema(database: str = "theia_pitching_db", table: str = None) -> dict:
        """
        Get detailed schema information for database tables.
        
        Useful for understanding table structure before writing queries.
        
        Args:
            database: Database name ("theia_pitching_db" or "theia_hitting_db") 
            table: Specific table name (optional, returns info for that table)
            
        Returns:
            Schema information including columns and sample data
        """
        log_info(f"Getting schema info for {database}")
        
        if table:
            return await get_table_info(database, table, mcp.db_pools)
        else:
            # Return general schema context
            return {
                "database": database,
                "schema_context": get_complete_schema_context(),
                "key_tables": ["users", "sessions", "trials", "poi"],
                "suggestion": "Use get_database_schema with a specific table name for detailed column info"
            }

    @mcp.tool()
    async def explore_metrics(search_term: str = None, database: str = None) -> dict:
        """
        Explore available biomechanical metrics across databases.
        
        Use this to discover what metrics are available for analysis.
        
        Args:
            search_term: Optional search term to find specific metrics (e.g., "velocity", "rotation", "angle")
            database: Optional database filter ("theia_pitching_db" or "theia_hitting_db")
            
        Returns:
            Available metrics with descriptions
        """
        log_info(f"Exploring metrics with search term: {search_term}")
        
        if search_term:
            # Search for specific metrics
            results = get_metric_by_name(search_term, database)
            return {
                "search_term": search_term,
                "found_metrics": results,
                "total_found": len(results)
            }
        else:
            # Return all metrics
            response = {
                "total_metrics": 0,
                "databases": {}
            }
            
            if database != "theia_hitting_db":
                pitching_metrics = get_all_pitching_metrics()
                response["databases"]["theia_pitching_db"] = {
                    "description": "Pitching biomechanics metrics",
                    "metric_count": len(pitching_metrics),
                    "metrics": pitching_metrics
                }
                response["total_metrics"] += len(pitching_metrics)
            
            if database != "theia_pitching_db":
                hitting_metrics = get_all_hitting_metrics()
                response["databases"]["theia_hitting_db"] = {
                    "description": "Hitting biomechanics metrics", 
                    "metric_count": len(hitting_metrics),
                    "metrics": hitting_metrics
                }
                response["total_metrics"] += len(hitting_metrics)
            
            return response
    
    @mcp.tool()
    async def find_player(name: str, database: str = None) -> dict:
        """Find a player by name in both pitching and hitting databases."""
        log_info(f"Searching for player: {name}")
        
        result = await search_player(name, database, mcp.db_pools)
        
        if "error" in result:
            return result
            
        return {
            "message": f"Found player in {result['database']}",
            "player": result["player"],
            "database": result["database"]
        }

    @mcp.tool()
    async def get_player_sessions(name: str, database: str = None, limit: int = 5) -> dict:
        """Find recent sessions for a player."""
        log_info(f"Finding sessions for: {name}")
        
        result = await search_player(name, database, mcp.db_pools)
        
        if "error" in result:
            return result
            
        player = result["player"]
        db = result["database"]
        
        async with mcp.db_pools[db].acquire() as conn:
            cursor = await conn.cursor(aiomysql.DictCursor)
            
            await cursor.execute(
                """
                SELECT sessions.session, sessions.date
                FROM sessions
                WHERE sessions.user = %s
                ORDER BY sessions.date DESC
                LIMIT %s
                """,
                (player['user'], limit)
            )
            
            rows = await cursor.fetchall()
            
            if not rows:
                return {
                    "player": player,
                    "database": db,
                    "message": "No sessions found for this player",
                    "sessions": []
                }
            
            sessions = []
            for row in rows:
                session_date = row['date']
                if isinstance(session_date, datetime):
                    formatted_date = session_date.strftime("%Y-%m-%d")
                else:
                    formatted_date = str(session_date)
                    
                sessions.append({
                    "session_id": row['session'],
                    "date": formatted_date
                })
            
            return {
                "player": player,
                "database": db,
                "message": f"Found {len(sessions)} sessions",
                "sessions": sessions
            }

    @mcp.tool()
    async def get_poi_metrics(session_id: int, database: str = None) -> dict:
        """Get POI metrics for a specific session."""
        log_info(f"Getting POI data for session: {session_id}")
        
        if not mcp.db_pools:
            return {"error": "Database connection not available"}
        
        # Find which database this session is in if not specified
        if not database:
            for db in ['theia_pitching_db', 'theia_hitting_db']:
                if db not in mcp.db_pools:
                    continue
                    
                async with mcp.db_pools[db].acquire() as conn:
                    cursor = await conn.cursor(aiomysql.DictCursor)
                    await cursor.execute(
                        """
                        SELECT sessions.session, sessions.user, sessions.date
                        FROM sessions
                        WHERE sessions.session = %s
                        """,
                        (session_id,)
                    )
                    
                    if await cursor.fetchone():
                        database = db
                        break
        
        if not database:
            return {"error": f"No session found with ID {session_id}"}
        
        async with mcp.db_pools[database].acquire() as conn:
            cursor = await conn.cursor(aiomysql.DictCursor)
            
            # Get player info
            await cursor.execute(
                """
                SELECT users.name, users.traq, sessions.date
                FROM sessions
                INNER JOIN users ON users.user = sessions.user
                WHERE sessions.session = %s
                """,
                (session_id,)
            )
            
            session_info = await cursor.fetchone()
            if not session_info:
                return {"error": f"No session found with ID {session_id}"}
            
            # Get available metrics for this database
            metrics_map = await get_available_metrics(cursor, database)
            if not metrics_map:
                return {"error": "No metrics available for this database"}
            
            # Build dynamic query for available metrics
            metric_calculations = []
            for friendly_name, column_name in metrics_map.items():
                metric_calculations.extend([
                    f"AVG({column_name}) as avg_{friendly_name}",
                    f"MIN({column_name}) as min_{friendly_name}",
                    f"MAX({column_name}) as max_{friendly_name}",
                    f"STDDEV({column_name}) as stddev_{friendly_name}",
                    f"COUNT({column_name}) as count_{friendly_name}"
                ])
            
            query = f"""
                SELECT 
                    COUNT(*) as total_throws,
                    {', '.join(metric_calculations)}
                FROM poi
                WHERE session_trial = %s
            """
            
            await cursor.execute(query, (session_id,))
            stats = await cursor.fetchone()
            
            if not stats:
                return {"error": f"No POI data found for session {session_id}"}
            
            # Format the response
            metrics_data = {}
            for friendly_name in metrics_map.keys():
                if stats[f'avg_{friendly_name}'] is not None:
                    metrics_data[friendly_name] = {
                        "average": stats[f'avg_{friendly_name}'],
                        "minimum": stats[f'min_{friendly_name}'],
                        "maximum": stats[f'max_{friendly_name}'],
                        "stddev": stats[f'stddev_{friendly_name}'],
                        "count": stats[f'count_{friendly_name}']
                    }
            
            session_date = session_info['date']
            if isinstance(session_date, datetime):
                formatted_date = session_date.strftime("%Y-%m-%d")
            else:
                formatted_date = str(session_date)
            
            return {
                "session_id": session_id,
                "database": database,
                "player": {
                    "name": session_info['name'],
                    "traq_id": session_info['traq']
                },
                "date": formatted_date,
                "total_throws": stats['total_throws'],
                "metrics": metrics_data
            }

    @mcp.tool()
    async def get_traq_id(player_name: str, database: str = None) -> dict:
        """Find a player's TRAQ ID by name."""
        log_info(f"Looking up TRAQ ID for: {player_name}")
        
        result = await search_player(player_name, database, mcp.db_pools)
        
        if "error" in result:
            return result
            
        player = result["player"]
        
        return {
            "name": player['name'],
            "traq_id": player['traq'],
            "user_id": player['user'],
            "dob": player['dob'],
            "database": result["database"]
        }

    @mcp.tool()
    async def compare_metric_over_time(player_name: str, metric_name: str, session_count: int = 3, database: str = None) -> dict:
        """Compare a specific metric across multiple sessions for a player."""
        log_info(f"Comparing {metric_name} across {session_count} sessions for {player_name}")
        
        result = await search_player(player_name, database, mcp.db_pools)
        if "error" in result:
            return result
        
        player = result["player"]
        db = result["database"]
        
        async with mcp.db_pools[db].acquire() as conn:
            cursor = await conn.cursor(aiomysql.DictCursor)
            
            metrics_map = await get_available_metrics(cursor, db)
            if not metrics_map:
                return {"error": "No metrics available for this database"}
            
            # Find the actual column name for the requested metric
            column_name = None
            friendly_name = None
            
            if metric_name in metrics_map:
                friendly_name = metric_name
                column_name = metrics_map[metric_name]
            else:
                # Try case-insensitive partial match
                metric_lower = metric_name.lower()
                for fname, cname in metrics_map.items():
                    if metric_lower in fname.lower() or metric_lower in cname.lower():
                        friendly_name = fname
                        column_name = cname
                        break
            
            if not column_name:
                available_metrics = list(metrics_map.keys())
                return {
                    "error": f"Metric '{metric_name}' not found",
                    "available_metrics": available_metrics
                }
            
            # Get the sessions
            await cursor.execute(
                """
                SELECT session, date
                FROM sessions
                WHERE user = %s
                ORDER BY date DESC
                LIMIT %s
                """,
                (player['user'], session_count)
            )
            
            sessions = await cursor.fetchall()
            
            if not sessions:
                return {"error": f"No sessions found for {player['name']}"}
            
            # Get metric data for each session
            comparison = []
            for session in sessions:
                query = f"""
                    SELECT 
                        AVG({column_name}) as avg_value,
                        MAX({column_name}) as max_value,
                        MIN({column_name}) as min_value,
                        STDDEV({column_name}) as stddev_value,
                        COUNT({column_name}) as count_value
                    FROM poi
                    WHERE session_trial = %s
                """
                
                await cursor.execute(query, (session['session'],))
                data = await cursor.fetchone()
                
                session_date = session['date']
                if isinstance(session_date, datetime):
                    formatted_date = session_date.strftime("%Y-%m-%d")
                else:
                    formatted_date = str(session_date)
                
                if data and data['avg_value'] is not None:
                    comparison.append({
                        "session_id": session['session'],
                        "date": formatted_date,
                        "average": data['avg_value'],
                        "maximum": data['max_value'],
                        "minimum": data['min_value'],
                        "stddev": data['stddev_value'],
                        "count": data['count_value']
                    })
            
            if not comparison:
                return {"error": f"No data found for metric '{friendly_name}' in any session"}
            
            # Calculate trend information
            if len(comparison) >= 2:
                first_avg = comparison[-1]['average']  # Oldest session
                last_avg = comparison[0]['average']   # Newest session
                total_change = ((last_avg - first_avg) / first_avg) * 100
                
                is_increasing = all(comparison[i]['average'] >= comparison[i+1]['average'] 
                                  for i in range(len(comparison)-1))
                is_decreasing = all(comparison[i]['average'] <= comparison[i+1]['average'] 
                                  for i in range(len(comparison)-1))
                
                if is_increasing:
                    trend = "Consistently increasing"
                elif is_decreasing:
                    trend = "Consistently decreasing"
                else:
                    trend = "Variable"
            else:
                total_change = 0
                trend = "Insufficient data for trend"
            
            return {
                "player": player['name'],
                "database": db,
                "metric": {
                    "name": friendly_name,
                    "column": column_name
                },
                "sessions_analyzed": len(comparison),
                "comparison": comparison,
                "trend": trend,
                "total_change_percentage": total_change if len(comparison) >= 2 else None
            }