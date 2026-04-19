#!/bin/bash

# Attendance Management System - Deployment Script

echo "🚀 Starting deployment process..."
echo ""

# Check if we're in the right directory
if [ ! -f "wsgi.py" ]; then
    echo "❌ Error: wsgi.py not found. Please run this script from the project root."
    exit 1
fi

echo "✅ Project structure verified"
echo ""

# Check git status
echo "📋 Git Status:"
git status
echo ""

# Add all changes
echo "📝 Adding all changes to git..."
git add .
echo ""

# Commit if there are changes
if git diff --cached --quiet; then
    echo "ℹ️  No changes to commit"
else
    echo "📤 Committing changes..."
    git commit -m "Deploy: Attendance Management System to Vercel"
    echo ""
fi

# Push to GitHub
echo "🔗 Pushing to GitHub (branch: $(git rev-parse --abbrev-ref HEAD))..."
git push origin $(git rev-parse --abbrev-ref HEAD)
echo ""

echo "✅ Changes pushed to GitHub!"
echo ""
echo "🎉 Deployment Instructions:"
echo "1. The changes have been pushed to your GitHub repository"
echo "2. Vercel will automatically deploy from your GitHub connection"
echo "3. Check your Vercel dashboard at: https://vercel.com/dashboard"
echo "4. Your live URL will be available shortly"
echo ""
