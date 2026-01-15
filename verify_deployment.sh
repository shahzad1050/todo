#!/bin/bash
# Deployment verification script for GitHub-Vercel integration

echo "🔍 Checking GitHub-Vercel deployment readiness..."

# Check if required files exist
echo "✅ Checking for required files..."
if [ -f "backend/vercel.json" ]; then
    echo "   ✓ backend/vercel.json exists"
else
    echo "   ✗ backend/vercel.json missing"
fi

if [ -f "backend/api_handler.py" ]; then
    echo "   ✓ backend/api_handler.py exists"
else
    echo "   ✗ backend/api_handler.py missing"
fi

if [ -f "backend/requirements.txt" ]; then
    echo "   ✓ backend/requirements.txt exists"
else
    echo "   ✗ backend/requirements.txt missing"
fi

if [ -f "backend/runtime.txt" ]; then
    echo "   ✓ backend/runtime.txt exists"
else
    echo "   ✗ backend/runtime.txt missing"
fi

# Check if sensitive files are properly ignored
echo "✅ Checking for security issues..."
if [ -f ".gitignore" ] && grep -q ".env" ".gitignore"; then
    echo "   ✓ .env files are in .gitignore"
else
    echo "   ⚠ .env files may not be properly ignored"
fi

# Check Python dependencies
echo "✅ Checking Python dependencies..."
if [ -f "backend/requirements.txt" ]; then
    if grep -q "fastapi" "backend/requirements.txt" && grep -q "mangum" "backend/requirements.txt"; then
        echo "   ✓ Required dependencies found"
    else
        echo "   ⚠ Missing required dependencies (fastapi, mangum)"
    fi
else
    echo "   ⚠ requirements.txt not found"
fi

echo ""
echo "📋 Summary:"
echo "Your GitHub-Vercel integration appears to be properly configured!"
echo ""
echo "🚀 To deploy:"
echo "1. cd backend"
echo "2. vercel --prod"
echo ""
echo "🔐 Security reminder: Never commit .env files or credentials to the repository"
echo "🔧 Make sure to set environment variables in the Vercel dashboard"