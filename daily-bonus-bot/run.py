#!/usr/bin/env python3
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Run the app
    app.run(
        host='0.0.0.0',  # Allow access from any IP (needed for mobile access)
        port=5000,
        debug=True  # Set to False in production
    )