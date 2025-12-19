import os
from pathlib import Path

# Motia API configuration
config = {
    "name": "ServeAppJS",
    "type": "api",
    "path": "/app.js",
    "method": "GET",
    "description": "Serve the app.js file",
    "emits": [],
    "responseSchema": {
        200: {
            "type": "string"
        }
    }
}

async def handler(req, context):
    """Serve the app.js file"""
    try:
        # Get the frontend directory path
        project_root = Path(__file__).parent.parent.parent
        app_js_path = project_root / "frontend" / "app.js"
        
        # Read the JS file
        with open(app_js_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        return {
            "status": 200,
            "headers": {"Content-Type": "application/javascript"},
            "body": js_content
        }
    except Exception as e:
        context.logger.error(f"Error serving app.js: {str(e)}")
        return {
            "status": 500,
            "body": f"console.error('Error loading app.js: {str(e)}');"
        }
