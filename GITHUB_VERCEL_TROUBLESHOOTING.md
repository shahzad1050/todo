# GitHub-Vercel Deployment Troubleshooting Guide

This guide addresses common issues that cause GitHub-Vercel deployment failures and provides solutions.

## Common Deployment Issues & Solutions

### 1. Security Issues
**Problem**: Sensitive files like `.env` with credentials committed to repository
**Solution**:
- Added comprehensive `.gitignore` to exclude sensitive files
- Created `.env.example` template for users to configure their own environment variables
- Never commit actual credentials to the repository

### 2. Runtime Compatibility
**Problem**: Python version mismatch between local and Vercel
**Solution**:
- Confirmed `runtime.txt` specifies `python-3.9` which is supported by Vercel
- This matches the configuration in `vercel.json`

### 3. Serverless Function Configuration
**Problem**: Incorrect handler configuration for Vercel serverless functions
**Solution**:
- Fixed `api_handler.py` to use proper Mangum configuration for Vercel
- Removed problematic path manipulation that could cause issues
- Ensured proper handler function naming to avoid conflicts

### 4. Database Configuration for Serverless
**Problem**: Database connection not optimized for serverless environments
**Solution**:
- Updated `database.py` to rely solely on environment variables (no dotenv loading in serverless)
- Added fallback SQLite configuration for development only
- Maintained serverless-friendly connection pooling settings

### 5. Environment Variable Handling
**Problem**: Local environment variable loading incompatible with Vercel
**Solution**:
- Removed `dotenv` import from `main.py` as Vercel handles environment variables differently
- Updated code to use `os.getenv()` directly which works in Vercel environment

## Deployment Steps

### Before Deploying to Vercel:
1. Ensure your repository is properly connected to GitHub
2. Verify all sensitive files are in `.gitignore`
3. Make sure your `requirements.txt` includes all dependencies
4. Test locally with `vercel dev` or by running the application directly

### Setting Up Vercel Project:
1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure the project settings:
   - Framework Preset: None (since it's a Python/FASTAPI app)
   - Root Directory: `/backend` (if deploying just the backend)
   - Build Command: Leave empty (Vercel will detect automatically)
   - Output Directory: Leave empty

### Environment Variables in Vercel:
Add these environment variables in the Vercel dashboard under Settings → Environment Variables:
- `DATABASE_URL`: Your production database connection string
- `SECRET_KEY`: A strong, randomly generated secret key
- `FRONTEND_URL`: Your frontend application URL

## Testing Your Deployment

After deployment, verify these endpoints work:
- Root: `https://your-project-name.vercel.app/`
- Health check: `https://your-project-name.vercel.app/health`
- API docs: `https://your-project-name.vercel.app/docs`

## Common Error Messages and Fixes

### "Module not found" errors:
- Verify all dependencies are in `requirements.txt`
- Check that Vercel runtime matches your local Python version

### Database connection errors:
- Ensure `DATABASE_URL` environment variable is properly set in Vercel
- Verify your database allows connections from Vercel's IP ranges
- Check that your database connection string is properly formatted

### Handler function errors:
- Verify `api_handler.py` follows Vercel's serverless function format
- Ensure Mangum is properly configured to wrap your FastAPI app

## Best Practices for GitHub-Vercel Deployment

1. **Never commit sensitive data** to the repository
2. **Use environment variables** for configuration
3. **Test locally** before pushing to GitHub
4. **Monitor deployment logs** in the Vercel dashboard
5. **Keep dependencies updated** in `requirements.txt`
6. **Design stateless applications** for serverless environments

## Repository Structure for Deployment

Your repository should have:
```
project-root/
├── backend/
│   ├── main.py (FastAPI application)
│   ├── api_handler.py (Vercel entry point)
│   ├── requirements.txt (dependencies)
│   ├── vercel.json (Vercel configuration)
│   ├── runtime.txt (Python version)
│   └── other backend files...
├── .gitignore (properly configured)
└── other project files...
```

## Verifying Successful Deployment

After deployment, check:
- ✅ No error messages in Vercel dashboard logs
- ✅ Health check endpoint returns success
- ✅ API documentation is accessible
- ✅ Database connections work properly
- ✅ Environment variables are properly loaded

## Rollback Plan

If deployment fails:
1. Check Vercel logs for specific error messages
2. Revert to the last known working commit
3. Fix the identified issue
4. Redeploy