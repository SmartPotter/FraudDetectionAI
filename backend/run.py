import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("ENVIRONMENT", "development") == "development"
    
    print(f"Starting Walmart AI Fraud Prevention Platform API...")
    print(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"Server: http://{host}:{port}")
    print(f"Docs: http://{host}:{port}/docs")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )