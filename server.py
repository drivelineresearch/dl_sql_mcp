#!/usr/bin/env python3
"""
Driveline Data Query MCP Server
A clean, structured MCP server for querying baseball analytics data
"""

import subprocess
import sys
import os

def check_and_install_dependencies():
    """Check for required dependencies and install them if missing."""
    dependencies = {
        'aiomysql': 'aiomysql',
        'mcp': 'mcp[fast]'
    }
    
    for module_name, package_name in dependencies.items():
        try:
            __import__(module_name)
            print(f"INFO: {module_name} already installed", file=sys.stderr)
        except ImportError:
            print(f"INFO: Installing {package_name}...", file=sys.stderr)
            try:
                process = subprocess.Popen(
                    [sys.executable, "-m", "pip", "install", package_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                stdout, stderr = process.communicate(timeout=300)
                
                if process.returncode != 0:
                    print(f"ERROR: Error installing {package_name}. Return code: {process.returncode}", file=sys.stderr)
                    print(f"ERROR: Error output: {stderr}", file=sys.stderr)
                    sys.exit(1)
                    
                print(f"INFO: {package_name} installed successfully!", file=sys.stderr)
                
            except subprocess.TimeoutExpired:
                print(f"ERROR: Installation of {package_name} timed out after 300 seconds", file=sys.stderr)
                process.kill()
                sys.exit(1)
            except Exception as e:
                print(f"ERROR: Unexpected error installing {package_name}: {str(e)}", file=sys.stderr)
                sys.exit(1)

# Install dependencies before importing
try:
    check_and_install_dependencies()
except Exception as e:
    print(f"ERROR: Unexpected error during dependency check: {str(e)}", file=sys.stderr)
    sys.exit(1)

# Now import the modules
try:
    from mcp.server import FastMCP
    from database import lifespan
    from tools import register_tools
    from config import log_info, log_error
    print("INFO: All required modules imported successfully", file=sys.stderr)
except ImportError as e:
    print(f"ERROR: Failed to import required modules: {str(e)}", file=sys.stderr)
    sys.exit(1)

def create_server():
    """Create and configure the MCP server"""
    try:
        mcp = FastMCP("Driveline Data Query", lifespan=lifespan)
        log_info("FastMCP server created successfully")
        
        # Register all tools
        register_tools(mcp)
        log_info("All tools registered successfully")
        
        return mcp
    except Exception as e:
        log_error(f"Failed to create MCP server: {str(e)}")
        sys.exit(1)

def main():
    """Main entry point"""
    log_info("Starting Driveline Data Query MCP server...")
    log_info("This server is configured for Claude Desktop integration")
    log_info("To use this server with Claude Desktop:")
    log_info("1. Open Claude Desktop")
    log_info("2. Go to Settings > Tools")
    log_info("3. Click 'Add Tool'")
    log_info("4. Select this file and check 'Install with aiomysql'")
    log_info("\nPress Ctrl+C to stop the server")
    
    mcp = create_server()
    
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        log_error(f"Error starting server: {str(e)}")
        log_error("Please check your configuration and try again")
        sys.exit(1)

if __name__ == "__main__":
    main()