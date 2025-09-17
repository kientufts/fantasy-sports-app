#!/bin/bash
# Git Setup Script for Personal Project
# Run this script to configure git with your personal credentials

echo "🔧 Setting up git configuration for Fantasy Sports App"
echo "======================================================"

# Get personal email from user
echo ""
read -p "Enter your personal email address: " personal_email
read -p "Enter your name for git commits: " git_name

# Configure git for this repository only (not global)
git config user.email "$personal_email"
git config user.name "$git_name"

echo ""
echo "✅ Git configured with:"
echo "   Name: $git_name"  
echo "   Email: $personal_email"
echo ""

# Show current configuration
echo "Current git config for this repository:"
git config --local --list | grep user

echo ""
echo "🎉 Ready to commit! Your work credentials remain unchanged globally."
echo "📝 Next steps:"
echo "   1. git add ."
echo "   2. git commit -m 'Initial commit: Fantasy Sports App'"
echo "   3. git remote add origin <your-repo-url>"
echo "   4. git push -u origin main"
