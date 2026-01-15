# Deploying Your FastAPI Backend to Vercel

This guide will walk you through deploying your FastAPI application to Vercel.

## Prerequisites

1. A GitHub account with your code repository
2. Vercel account (sign up at https://vercel.com)
3. Vercel CLI installed (optional): `npm i -g vercel`

## Current Configuration

Your application is already configured for Vercel with:
- `vercel.json` - Vercel deployment configuration
- `api_handler.py` - Serverless function handler using Mangum
- `requirements.txt` - Python dependencies

## Step-by-Step Deployment Guide

### Step 1: Prepare Your Repository

1. Ensure all your backend files are committed to your GitHub repository
2. Make sure you have the following files in your repository:
   - `main.py` (your FastAPI application)
   - `api_handler.py` (Vercel entry point)
   - `requirements.txt` (dependencies)
   - `vercel.json` (Vercel configuration)
   - All other necessary Python files (models, database, api, auth, etc.)

### Step 2: Set Up Your Vercel Account

1. Go to https://vercel.com and sign up for an account
2. Log in to your Vercel dashboard

### Step 3: Import Your Project

1. In your Vercel dashboard, click "Add New..." and select "Project"
2. Connect to your GitHub account
3. Select your repository that contains the backend code

### Step 4: Configure the Project

Vercel should automatically detect your Python project. Verify these settings:

- **Framework Preset**: None (or Python if available)
- **Root Directory**: Should be the directory containing your files
- **Build Command**: Leave empty or use `pip install -r requirements.txt`
- **Output Directory**: Leave empty for Python projects

### Step 5: Configure Environment Variables

In the "Environment Variables" section, add the following:

#### Required Environment Variables:

1. **DATABASE_URL**:
   - For PostgreSQL: `postgresql://username:password@host:port/database_name`
   - For Neon (recommended for serverless): Your Neon database connection string
   - For testing: `sqlite:///./test.db` (not recommended for production)

2. **SECRET_KEY**:
   - Generate a strong secret key for JWT tokens
   - Example: Use Python to generate one:
     ```python
     import secrets
     print(secrets.token_urlsafe(32))
     ```

3. **FRONTEND_URL**:
   - Set this to your frontend URL (e.g., your frontend Vercel URL)

#### Optional Variables:
- `ALGORITHM`: HS256 (default in your code)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 30 (default in your code)

### Step 6: Deploy

1. Click "Deploy" to start the deployment process
2. Vercel will install dependencies and build your application
3. Monitor the deployment logs in the Vercel dashboard

### Step 7: Verify Deployment

Once deployed:
1. Visit your assigned Vercel URL (shown in the dashboard)
2. Test the health check endpoint: `https://your-project.vercel.app/health`
3. Test the root endpoint: `https://your-project.vercel.app/`
4. Check API documentation: `https://your-project.vercel.app/docs`

## Vercel Configuration Explained

Your `vercel.json` file is configured as follows:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api_handler.py",
      "use": "@vercel/python",
      "config": { "runtime": "python3.9" }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api_handler.py"
    }
  ]
}
```

- **version**: Vercel platform version (2 is current)
- **builds**: Defines how to build your application using Python runtime
- **routes**: Routes all requests to your API handler

## Serverless Handler (api_handler.py)

Your `api_handler.py` uses Mangum to bridge FastAPI with Vercel's serverless functions:

```python
from main import app
from mangum import Mangum

# Create the Mangum handler to convert FastAPI app to Vercel serverless function
mangum_handler = Mangum(app, lifespan="off")

def handler(request, *args, **kwargs):
    """Vercel serverless function handler"""
    return mangum_handler(request, *args, **kwargs)
```

## Database Configuration

Your database configuration is optimized for serverless environments:

- Uses connection pooling settings appropriate for serverless
- Falls back gracefully if database connection fails
- Designed to work with both PostgreSQL and SQLite

## Troubleshooting

### Common Issues:

1. **Import Errors**:
   - Ensure all dependencies are in requirements.txt
   - Verify that runtime matches your development environment

2. **Database Connection Issues**:
   - Check that DATABASE_URL is properly set in environment variables
   - Ensure your database allows connections from Vercel's IP ranges

3. **Cold Start Issues**:
   - First request may be slow due to cold start
   - This is normal for serverless functions

4. **Timeout Issues**:
   - Vercel has timeout limits for serverless functions
   - Optimize your code to respond quickly

### Useful Endpoints After Deployment:

- Root: `https://your-project.vercel.app/`
- Health check: `https://your-project.vercel.app/health`
- API docs: `https://your-project.vercel.app/docs`
- Redoc: `https://your-project.vercel.app/redoc`

## Environment-Specific Considerations

- **Development**: Uses SQLite by default
- **Production (Vercel)**: Uses DATABASE_URL from environment variables
- **Authentication**: JWT tokens with configurable expiration

## Scaling and Performance

- Vercel automatically scales your functions based on demand
- Each request may run on a different instance
- Design your application to be stateless
- Use external services for persistent storage

## Next Steps

After successful deployment:
1. Test all API endpoints thoroughly
2. Set up a custom domain if desired
3. Configure domain-specific environment variables
4. Set up analytics or monitoring if needed
5. Plan for database scaling as your application grows