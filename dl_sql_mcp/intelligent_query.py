"""
Intelligent query system that allows natural language queries
The LLM interprets the question and generates appropriate SQL
"""

import aiomysql
from datetime import datetime
from .database import search_player
from .complete_schema import get_complete_schema_context
from .config import log_info, log_error

async def execute_intelligent_query(question: str, mcp_db_pools) -> dict:
    """
    Execute an intelligent query based on natural language input
    The LLM will determine what database to query and generate SQL
    """
    
    if not mcp_db_pools:
        return {"error": "Database connection not available"}
    
    # Get available databases
    available_dbs = []
    for db_name in ["theia_pitching_db", "theia_hitting_db"]:
        if db_name in mcp_db_pools:
            available_dbs.append(db_name)
    
    if not available_dbs:
        return {"error": "No databases available"}
    
    # Start with pitching database as default, but LLM can choose
    primary_db = "theia_pitching_db" if "theia_pitching_db" in available_dbs else available_dbs[0]
    
    try:
        async with mcp_db_pools[primary_db].acquire() as conn:
            cursor = await conn.cursor(aiomysql.DictCursor)
            
            # This is where the magic happens - the LLM in the MCP tool
            # will interpret the question and generate appropriate SQL
            # For now, we'll provide the framework and let the calling tool
            # handle the intelligent interpretation
            
            return {
                "question": question,
                "available_databases": available_dbs,
                "primary_database": primary_db,
                "schema_context": get_schema_context(),
                "status": "ready_for_interpretation"
            }
            
    except Exception as e:
        log_error(f"Error in intelligent query setup: {str(e)}")
        return {"error": f"Query setup failed: {str(e)}"}

async def execute_custom_sql(sql_query: str, database: str, mcp_db_pools, limit: int = 100) -> dict:
    """
    Execute a custom SQL query on the specified database
    Used by the intelligent query system after LLM generates SQL
    """
    
    if not mcp_db_pools or database not in mcp_db_pools:
        return {"error": f"Database {database} not available"}
    
    try:
        async with mcp_db_pools[database].acquire() as conn:
            cursor = await conn.cursor(aiomysql.DictCursor)
            
            # Add LIMIT if not already present and it's a SELECT query
            if sql_query.strip().upper().startswith('SELECT') and 'LIMIT' not in sql_query.upper():
                sql_query += f" LIMIT {limit}"
            
            await cursor.execute(sql_query)
            results = await cursor.fetchall()
            
            # Format results for readability
            formatted_results = []
            for row in results:
                formatted_row = {}
                for key, value in row.items():
                    if isinstance(value, datetime):
                        formatted_row[key] = value.strftime("%Y-%m-%d")
                    elif isinstance(value, float):
                        # Round to 2 decimal places for readability
                        formatted_row[key] = round(value, 2)
                    else:
                        formatted_row[key] = value
                formatted_results.append(formatted_row)
            
            return {
                "database": database,
                "sql_query": sql_query,
                "result_count": len(formatted_results),
                "results": formatted_results
            }
            
    except Exception as e:
        log_error(f"Error executing SQL query: {str(e)}")
        return {"error": f"SQL execution failed: {str(e)}", "sql_query": sql_query}

async def get_table_info(database: str, table_name: str, mcp_db_pools) -> dict:
    """
    Get detailed information about a specific table
    Useful for the LLM to understand table structure
    """
    
    if not mcp_db_pools or database not in mcp_db_pools:
        return {"error": f"Database {database} not available"}
    
    try:
        async with mcp_db_pools[database].acquire() as conn:
            cursor = await conn.cursor(aiomysql.DictCursor)
            
            # Get column information
            await cursor.execute(f"DESCRIBE {table_name}")
            columns = await cursor.fetchall()
            
            # Get sample data (first 3 rows)
            await cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            sample_data = await cursor.fetchall()
            
            return {
                "database": database,
                "table": table_name,
                "columns": columns,
                "sample_data": sample_data
            }
            
    except Exception as e:
        log_error(f"Error getting table info: {str(e)}")
        return {"error": f"Failed to get table info: {str(e)}"}

def format_query_response(raw_results: dict, question: str) -> dict:
    """
    Format the query results in a trainer-friendly way
    """
    
    if "error" in raw_results:
        return raw_results
    
    results = raw_results.get("results", [])
    
    if not results:
        return {
            "question": question,
            "answer": "No data found matching your query.",
            "result_count": 0
        }
    
    # Basic formatting - can be enhanced based on query type
    if len(results) == 1:
        # Single result
        return {
            "question": question,
            "answer": "Found one result:",
            "data": results[0],
            "result_count": 1
        }
    else:
        # Multiple results
        return {
            "question": question,
            "answer": f"Found {len(results)} results:",
            "data": results,
            "result_count": len(results),
            "summary": f"Showing {min(len(results), 100)} of {len(results)} total results"
        }