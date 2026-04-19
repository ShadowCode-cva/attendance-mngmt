#!/usr/bin/env python3
import subprocess
import sys

def run_command(cmd, description):
    print(f"\n{description}...")
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if result.returncode != 0:
            print(f"Error: Command failed with return code {result.returncode}")
            return False
        return True
    except Exception as e:
        print(f"Error executing command: {e}")
        return False

def main():
    print("Pushing fixes to GitHub...")
    print("=" * 60)
    
    # Add all changes
    if not run_command(["git", "add", "."], "Adding all changes"):
        sys.exit(1)
    
    # Commit changes
    if not run_command(
        ["git", "commit", "-m", "Fix: Add error handling and setup guide for Vercel deployment"],
        "Committing changes"
    ):
        print("No changes to commit")
        return
    
    # Get current branch
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True
    )
    current_branch = result.stdout.strip()
    
    # Push to GitHub
    if not run_command(
        ["git", "push", "origin", current_branch],
        f"Pushing to GitHub (branch: {current_branch})"
    ):
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ Changes pushed successfully!")
    print("Your Vercel deployment will be triggered automatically.")
    print("=" * 60)

if __name__ == "__main__":
    main()
