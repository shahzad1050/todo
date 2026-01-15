from main import app
from mangum import Mangum

# Create the Mangum handler to convert FastAPI app to Vercel serverless function
mangum_handler = Mangum(app, lifespan="off")


def handler(request, *args, **kwargs):
    """Vercel serverless function handler"""
    return mangum_handler(request, *args, **kwargs)