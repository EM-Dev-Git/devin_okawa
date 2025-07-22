#!/usr/bin/env python3
"""
WSL-compatible FastAPI server startup script
Provides multiple host binding options for WSL environments
"""
import sys
import subprocess
import argparse

def start_server(host="127.0.0.1", port=8000, reload=True):
    """Start FastAPI server with specified host binding"""
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "src.main:app", 
        f"--host={host}", 
        f"--port={port}"
    ]
    if reload:
        cmd.append("--reload")
    
    print(f"Starting FastAPI server on {host}:{port}")
    print(f"Command: {' '.join(cmd)}")
    print(f"Access URLs:")
    print(f"  - http://{host}:{port}")
    if host == "127.0.0.1":
        print(f"  - http://localhost:{port}")
    print()
    
    subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description="WSL-compatible FastAPI server")
    parser.add_argument("--host", default="127.0.0.1", 
                       help="Host to bind to (default: 127.0.0.1 for WSL compatibility)")
    parser.add_argument("--port", type=int, default=8000, 
                       help="Port to bind to (default: 8000)")
    parser.add_argument("--no-reload", action="store_true", 
                       help="Disable auto-reload")
    
    args = parser.parse_args()
    
    print("WSL-Compatible FastAPI Server Startup")
    print("=" * 40)
    print("This script provides WSL-compatible host binding options.")
    print("If you experience 404 errors with 0.0.0.0 binding in WSL,")
    print("try using 127.0.0.1 binding instead.")
    print()
    
    start_server(
        host=args.host, 
        port=args.port, 
        reload=not args.no_reload
    )

if __name__ == "__main__":
    main()
