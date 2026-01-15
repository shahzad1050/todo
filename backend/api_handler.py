import logging
from mangum import Mangum

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Import the app inside a try block to catch import errors
    from main import app
    logger.info("Successfully imported FastAPI app")

    # Create the Mangum handler to convert FastAPI app to Vercel serverless function
    handler = Mangum(app, lifespan="off")
    logger.info("Successfully created Mangum handler")

except Exception as e:
    logger.error(f"Error initializing application: {e}")
    # Create a simple fallback app for error cases
    from fastapi import FastAPI
    fallback_app = FastAPI()

    @fallback_app.get("/")
    def health_check():
        return {"status": "error", "message": f"Application failed to initialize: {str(e)}"}

    handler = Mangum(fallback_app, lifespan="off")