"""
run_web.py - Web Application Launcher

Run this script to start the Flask web server for Bill Manager.

Usage:
    python run_web.py

Then access the app at:
    http://localhost:5000
    
Or from another device on the same network:
    http://<your-computer-ip>:5000
"""

import sys
import subprocess

def main():
    print("=" * 60)
    print("Bill Manager - Web Application Launcher")
    print("=" * 60)
    print()
    
    # Check if Flask is installed
    try:
        import flask
        print("[OK] Flask is installed")
    except ImportError:
        print("[!] Flask is not installed")
        print()
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print()
        print("[OK] Packages installed successfully")
    
    print()
    print("Starting Flask web server...")
    print()
    print("=" * 60)
    print("Access the application at:")
    print("  Local:  http://localhost:5000")
    print("  Network: http://<your-ip>:5000")
    print("=" * 60)
    print()
    print("Press Ctrl+C to stop the server")
    print()
    
    # Import and run the Flask app
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
