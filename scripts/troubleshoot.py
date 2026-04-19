#!/usr/bin/env python3
"""
Troubleshooting script for Vercel deployment issues
"""
import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a shell command"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        if result.returncode != 0:
            print(f"❌ Failed with return code {result.returncode}")
            return False
        print("✅ Success")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    os.chdir('/vercel/share/v0-project')
    
    print("\n🔧 Attendance Management System - Deployment Troubleshooting")
    print("="*60)
    
    # Check git status
    run_command(['git', 'status'], "📋 Git Status")
    
    # Stage changes
    run_command(['git', 'add', '.'], "📝 Staging changes")
    
    # Commit
    if not run_command(
        ['git', 'commit', '-m', 'fix: Correct Vercel Flask configuration and error handling'],
        "📤 Committing changes"
    ):
        print("ℹ️  No changes to commit")
    
    # Get current branch
    result = subprocess.run(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
        capture_output=True,
        text=True,
        cwd='/vercel/share/v0-project'
    )
    branch = result.stdout.strip()
    
    # Push
    run_command(
        ['git', 'push', 'origin', branch],
        f"🚀 Pushing to GitHub (branch: {branch})"
    )
    
    print("\n" + "="*60)
    print("✅ Deployment fixes pushed!")
    print("="*60)
    print("\n📋 NEXT STEPS:")
    print("1. Visit Vercel Dashboard → Your Project")
    print("2. Check that these environment variables are set:")
    print("   - MONGO_URI (your MongoDB connection string)")
    print("   - SECRET_KEY (random secure string)")
    print("   - JWT_SECRET_KEY (random secure string)")
    print("   - FLASK_ENV = 'prod'")
    print("   - DEBUG = 'False'")
    print("3. Click 'Redeploy' to trigger a new build")
    print("4. Wait 2-3 minutes for deployment to complete")
    print("5. Visit your app URL and test the endpoints:")
    print("   - / (should show API is running)")
    print("   - /health (check MongoDB connection)")
    print("   - /config-check (verify environment variables)")

if __name__ == '__main__':
    main()
