#!/usr/bin/env python3
"""
Attendance Management System - Deployment to Vercel
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a shell command and handle errors"""
    print(f"\n{description}...")
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if result.returncode != 0:
            print(f"❌ Error: Command failed with return code {result.returncode}")
            return False
        return True
    except Exception as e:
        print(f"❌ Error executing command: {e}")
        return False

def main():
    project_root = os.getcwd()
    
    print("🚀 Starting Attendance Management System Deployment to Vercel")
    print("=" * 60)
    print(f"Project Root: {project_root}")
    
    # Check git status
    if not run_command(["git", "status"], "📋 Checking Git Status"):
        sys.exit(1)
    
    # Add all changes
    if not run_command(["git", "add", "."], "📝 Adding all changes"):
        sys.exit(1)
    
    # Commit changes
    if not run_command(
        ["git", "commit", "-m", "Deploy: Attendance Management System to Vercel"],
        "📤 Committing changes"
    ):
        print("ℹ️  No changes to commit (repository up to date)")
    
    # Push to GitHub
    current_branch = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        cwd=project_root
    ).stdout.strip()
    
    if not run_command(
        ["git", "push", "origin", current_branch],
        f"🔗 Pushing to GitHub (branch: {current_branch})"
    ):
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ Deployment Process Complete!")
    print("=" * 60)
    print("\n📌 Next Steps:")
    print("1. Your code has been pushed to GitHub")
    print("2. Vercel will automatically detect the push and start building")
    print("3. Monitor deployment at: https://vercel.com/dashboard")
    print("4. Your app will be live at the assigned Vercel URL")
    print("\n🎯 Vercel Project ID: prj_r5SmJDijRKXbTshQRuVqmtBsaoWt")
    print("📚 Repository: ShadowCode-cva/attendance-mngmt")
    print("\n💡 Key Information:")
    print("- Frontend: Static HTML/CSS/JS served from /frontend directory")
    print("- Backend: Flask API served from wsgi.py")
    print("- Database: MongoDB (ensure connection string is set in environment variables)")
    print("- Auth: JWT with bcrypt password hashing")
    print("\n")

if __name__ == "__main__":
    main()
