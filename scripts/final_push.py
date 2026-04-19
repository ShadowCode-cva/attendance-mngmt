#!/usr/bin/env python3
import subprocess
import sys
import os

os.chdir("/vercel/share/v0-project")

def run(cmd, desc):
    print(f"\n{desc}...")
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if result.returncode != 0:
        print(f"ERROR: Command failed")
        return False
    return True

# Stage all changes
if not run(["git", "add", "."], "Staging changes"):
    sys.exit(1)

# Commit with descriptive message
if not run(
    ["git", "commit", "-m", "Fix: Ensure Flask app is exported at module level for Vercel"],
    "Committing fixes"
):
    print("No changes to commit")

# Push to GitHub
current_branch = subprocess.run(
    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
    capture_output=True,
    text=True
).stdout.strip()

if not run(["git", "push", "origin", current_branch], f"Pushing to {current_branch}"):
    sys.exit(1)

print("\n✅ Successfully pushed fixes to GitHub!")
print(f"Vercel will automatically redeploy your project.")
