import os
from pathlib import Path

# Motia API configuration
config = {
    "name": "ServeFrontend",
    "type": "api",
    "path": "/medical",
    "method": "GET",
    "description": "Serve the medical report frontend application",
    "emits": [],
    "responseSchema": {
        200: {
            "type": "string"
        }
    }
}

async def handler(req, context):
    """Serve the frontend HTML"""
    try:
        # Get the frontend directory path
        project_root = Path(__file__).parent.parent.parent
        frontend_path = project_root / "frontend" / "index.html"
        
        # Read the HTML file
        with open(frontend_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        return {
            "status": 200,
            "headers": {"Content-Type": "text/html"},
            "body": html_content
        }
    except Exception as e:
        context.logger.error(f"Error serving frontend: {str(e)}")
        return {
            "status": 500,
            "body": f"Error loading frontend: {str(e)}"
        }
