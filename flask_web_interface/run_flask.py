#!/usr/bin/env python3
"""
Flask application runner for Chevy Casting Lookup Web Interface.
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # Set environment variables for development
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    print("=" * 60)
    print("🚗 Chevy Casting Lookup Web Interface")
    print("=" * 60)
    print("Starting Flask development server...")
    print("Web interface will be available at: http://localhost:5001")
    print("Make sure your FastAPI server is running on port 8000")
    print("=" * 60)
    
    try:
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5001,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down Flask server...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting Flask server: {e}")
        sys.exit(1)
