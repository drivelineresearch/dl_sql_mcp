import os
import platform
from pathlib import Path

def get_config_dir():
    """Get the appropriate config directory for the current OS"""
    if platform.system() == 'Windows':
        return Path.home() / 'AppData' / 'Roaming' / 'dl-sql-mcp'
    elif platform.system() == 'Darwin':  # macOS
        return Path.home() / 'Library' / 'Application Support' / 'dl-sql-mcp'
    else:  # Linux
        return Path.home() / '.config' / 'dl-sql-mcp'

def initialize_config():
    """Initialize config directory and .env file"""
    app_config_dir = get_config_dir()
    env_file = app_config_dir / '.env'
    
    # Create directory and template .env file on first run
    if not app_config_dir.exists():
        app_config_dir.mkdir(parents=True, exist_ok=True)
        print(f"INFO: Created config directory at: {app_config_dir}", file=sys.stderr)
    
    if not env_file.exists():
        template_content = """# DL SQL MCP Database Configuration
# Edit the values below with your actual database credentials

DB_HOST=10.200.200.107
DB_USER=readonlyuser
DB_PASSWORD=CHANGE_THIS_TO_YOUR_ACTUAL_PASSWORD
"""
        with open(env_file, 'w') as f:
            f.write(template_content)
        print(f"INFO: Created config file at: {env_file}", file=sys.stderr)
        print("INFO: Please edit this file with your actual database password", file=sys.stderr)
        return False  # Indicate that config was just created
    
    return True  # Config already exists

def load_env_variables():
    """Load environment variables from .env file"""
    env_file = get_config_dir() / '.env'
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

# Initialize config on import
import sys
config_exists = initialize_config()
load_env_variables()

# Database configuration
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'databases': ['theia_pitching_db', 'theia_hitting_db'],
    'autocommit': True,
    'connect_timeout': 30,
    'pool_recycle': 3600,
    'config_file': str(get_config_dir() / '.env')
}

def log_error(message):
    """Helper function to log errors to stderr"""
    import sys
    print(f"ERROR: {message}", file=sys.stderr)

def log_info(message):
    """Helper function to log info to stderr"""
    import sys
    print(f"INFO: {message}", file=sys.stderr)