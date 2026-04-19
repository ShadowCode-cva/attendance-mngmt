#!/usr/bin/env python3
import subprocess
import os

os.chdir(os.path.expanduser('~'))

# Find the v0-project directory
for root, dirs, files in os.walk('.'):
    if 'wsgi.py' in files and 'vercel.json' in files:
        os.chdir(root)
        break

print(f"Working directory: {os.getcwd()}")

# Stage and commit
subprocess.run(['git', 'add', '.'])
subprocess.run(['git', 'commit', '-m', 'fix: Flask and Vercel configuration for proper routing'])
subprocess.run(['git', 'push', 'origin', 'HEAD'])

print("\n✅ Changes pushed! Vercel will automatically redeploy.")
