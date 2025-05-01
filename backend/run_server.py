import uvicorn
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Run the directory setup script
    try:
        from setup_dirs import setup_directories
        setup_directories()
        logger.info("Directory setup completed successfully")
    except Exception as e:
        logger.error(f"Error during directory setup: {str(e)}")
        logger.info("Continuing with server startup...")
    
    # Check if we're in the right directory
    if not os.path.exists("app"):
        logger.warning("Warning: 'app' directory not found in current directory.")
        logger.warning("Make sure you're running this script from the backend directory.")
    
    # Start the server
    logger.info("Starting FastAPI server...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)