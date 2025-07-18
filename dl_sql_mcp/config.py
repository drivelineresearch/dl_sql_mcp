import os
import platform
from pathlib import Path

# Create app config directory and .env file if they don't exist
def get_config_dir():
    """Get the appropriate config directory for the current OS"""
    if platform.system() == 'Windows':
        return Path.home() / 'AppData' / 'Roaming' / 'dl-sql-mcp'
    elif platform.system() == 'Darwin':  # macOS
        return Path.home() / 'Library' / 'Application Support' / 'dl-sql-mcp'
    else:  # Linux
        return Path.home() / '.config' / 'dl-sql-mcp'

app_config_dir = get_config_dir()
env_file = app_config_dir / '.env'

# Create directory and template .env file on first run
if not app_config_dir.exists():
    app_config_dir.mkdir(parents=True, exist_ok=True)
    
if not env_file.exists():
    template_content = """# DL SQL MCP Database Configuration
# Edit the values below with your actual database credentials

DB_HOST=10.200.200.107
DB_USER=readonlyuser
DB_PASSWORD=CHANGE_THIS_TO_YOUR_ACTUAL_PASSWORD
"""
    with open(env_file, 'w') as f:
        f.write(template_content)
    print(f"INFO: Created config file at: {env_file}")
    print("INFO: Please edit this file with your actual database password")

# Load environment variables from .env file
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Database configuration
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'databases': ['theia_pitching_db', 'theia_hitting_db'],
    'autocommit': True,
    'connect_timeout': 30,
    'pool_recycle': 3600
}

def log_error(message):
    """Helper function to log errors to stderr"""
    import sys
    print(f"ERROR: {message}", file=sys.stderr)

def log_info(message):
    """Helper function to log info to stderr"""
    import sys
    print(f"INFO: {message}", file=sys.stderr)