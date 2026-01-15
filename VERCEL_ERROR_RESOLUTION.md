# Resolving Vercel Deployment Error

## The Issue
You received the error: "`vercel.json` schema validation failed with the following message: should NOT have additional property `rootDirectory`"

## Root Cause
The `rootDirectory` property is only valid in specific contexts within Vercel configuration. It's typically used when you have a monorepo and want to specify which directory to deploy from.

## Solution
For deploying your backend specifically, you have two options:

### Option 1: Deploy Just the Backend Directory (Recommended)
1. Navigate to the `backend` directory: `cd backend`
2. Run `vercel` from within the backend directory
3. Use the `backend/vercel.json` configuration which is already properly configured

### Option 2: Fix the Root vercel.json for Monorepo Setup
If you want to keep a monorepo setup, the root `vercel.json` should not contain `rootDirectory` in the top-level configuration. Instead:

```json
{
  "version": 2,
  "git": {
    "deploymentEnabled": false
  }
}
```

Then deploy each part separately or use Vercel's monorepo linking features.

## Recommended Approach
Since you already have a properly configured `backend/vercel.json`, the simplest solution is to:

1. Deploy your backend from the `backend` directory:
   ```bash
   cd backend
   vercel --prod
   ```

2. Your current backend configuration is correct:
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

## Updated Root vercel.json
I've updated the root vercel.json to remove any conflicting configurations that could cause the schema validation error.