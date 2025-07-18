import aiomysql
import asyncio
from datetime import datetime
from contextlib import asynccontextmanager
from .config import DATABASE_CONFIG, log_error, log_info

async def get_db_pools():
    """Create connection pools for all databases"""
    pools = {}
    
    # Check if credentials are configured
    if not DATABASE_CONFIG['password'] or DATABASE_CONFIG['password'] == 'CHANGE_THIS_TO_YOUR_ACTUAL_PASSWORD':
        log_error("Database password not configured. Please edit your .env file.")
        log_error(f"Config file location: {DATABASE_CONFIG.get('config_file', 'Unknown')}")
        return pools
    
    if not DATABASE_CONFIG['host'] or not DATABASE_CONFIG['user']:
        log_error("Database connection details incomplete.")
        return pools
    
    for db_name in DATABASE_CONFIG['databases']:
        try:
            log_info(f"Attempting to connect to {db_name}...")
            pool = await aiomysql.create_pool(
                host=DATABASE_CONFIG['host'],
                user=DATABASE_CONFIG['user'],
                password=DATABASE_CONFIG['password'],
                db=db_name,
                autocommit=DATABASE_CONFIG['autocommit'],
                connect_timeout=DATABASE_CONFIG['connect_timeout'],
                pool_recycle=DATABASE_CONFIG['pool_recycle']
            )
            log_info(f"Successfully connected to {db_name}!")
            pools[db_name] = pool
        except Exception as e:
            log_error(f"Failed to connect to {db_name}: {str(e)}")
            log_error("Connection Details:")
            log_error(f"- Host: {DATABASE_CONFIG['host']}")
            log_error(f"- Database: {db_name}")
            log_error(f"- User: {DATABASE_CONFIG['user']}")
    
    return pools

@asynccontextmanager
async def lifespan(app):
    """Manage database connections lifecycle"""
    log_info("Starting lifespan manager...")
    retries = 3
    
    for attempt in range(retries):
        try:
            log_info(f"Attempting database connections (attempt {attempt + 1}/{retries})...")
            app.db_pools = await get_db_pools()
            if app.db_pools:
                log_info(f"Database connections established on attempt {attempt + 1}")
                break
            else:
                log_error(f"Failed to connect on attempt {attempt + 1}, retrying...")
                if attempt < retries - 1:
                    await asyncio.sleep(2)
        except Exception as e:
            log_error(f"Error on attempt {attempt + 1}: {str(e)}")
            if attempt < retries - 1:
                await asyncio.sleep(2)

    if not hasattr(app, 'db_pools') or not app.db_pools:
        log_error("Warning: Starting server without any database connections. Features will not work.")
        app.db_pools = {}
    else:
        connected_dbs = ", ".join(app.db_pools.keys())
        log_info(f"Successfully connected databases: {connected_dbs}")
    
    try:
        yield {"db_pools": app.db_pools}
    except Exception as e:
        log_error(f"Error during server operation: {str(e)}")
    finally:
        log_info("Closing database connections...")
        for db_name, pool in app.db_pools.items():
            try:
                pool.close()
                await pool.wait_closed()
                log_info(f"Database connection closed for {db_name}")
            except Exception as e:
                log_error(f"Error closing connection for {db_name}: {str(e)}")

async def find_player_in_database(cursor, name: str, database: str) -> dict:
    """Find a player in a specific database"""
    await cursor.execute(
        """
        SELECT users.user, users.name, users.traq, users.dob
        FROM users
        WHERE users.name LIKE %s
        ORDER BY users.name
        LIMIT 1
        """,
        (f"%{name}%",)
    )
    
    player = await cursor.fetchone()
    if player and player['dob']:
        player['dob'] = player['dob'].strftime("%Y-%m-%d")
    
    return player

async def search_player(name: str, database: str = None, conn_pools = None) -> dict:
    """Search for a player across databases"""
    if conn_pools is None:
        return {"error": "Database connection not available"}
        
    if not conn_pools:
        return {"error": "Database connection not available"}
    
    databases = [database] if database else DATABASE_CONFIG['databases']
    
    for db in databases:
        if db not in conn_pools:
            continue
            
        async with conn_pools[db].acquire() as conn:
            cursor = await conn.cursor(aiomysql.DictCursor)
            player = await find_player_in_database(cursor, name, db)
            
            if player:
                return {
                    "player": player,
                    "database": db
                }
    
    return {"error": f"No player found matching '{name}'"}

async def get_available_metrics(cursor, database: str) -> dict:
    """Get available metrics for the specified database"""
    hitting_metrics = {
        "exit_velocity": "exit_velo_mph",
        "bat_speed": "blast_bat_speed_mph",
        "attack_angle": "attack_angle_contact",
        "hand_speed": "blast_hand_speed_max",
        "pelvis_rotation": "peak_pelvis_ang_velo",
        "torso_rotation": "peak_torso_ang_velo",
        "arm_speed": "peak_upper_arm_ang_velo",
        "hand_velocity": "peak_hand_ang_velo"
    }
    
    pitching_metrics = {
        "velocity": "pitch_speed_mph",
        "shoulder_rotation": "max_shoulder_internal_rotational_velo",
        "elbow_extension": "max_elbow_extension_velo",
        "torso_rotation": "max_torso_rotational_velo",
        "hip_shoulder_separation": "max_rotation_hip_shoulder_separation",
        "elbow_flexion": "max_elbow_flexion",
        "shoulder_external_rotation": "max_shoulder_external_rotation",
        "knee_extension": "lead_knee_extension_angular_velo_max",
        "stride": "stride_length",
        "arm_slot": "arm_slot",
        "timing": "timing_peak_torso_to_peak_pelvis_rot_velo"
    }
    
    await cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'poi' 
        AND table_schema = %s
        AND column_name NOT IN ('session_trial', 'throw_number')
    """, (database,))
    
    available_columns = set(row['column_name'] for row in await cursor.fetchall())
    
    metric_mapping = hitting_metrics if database == 'theia_hitting_db' else pitching_metrics
    
    available_metrics = {}
    for friendly_name, column_name in metric_mapping.items():
        if column_name in available_columns:
            available_metrics[friendly_name] = column_name
            
    return available_metrics