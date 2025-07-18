import os
from pathlib import Path

# Load environment variables from .env file
env_file = Path(__file__).parent / '.env'
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