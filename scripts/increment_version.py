import sys
import re
import os

def increment_version(version_str, branch_name):
    major, minor, patch = map(int, version_str.strip().split('.'))
    
    branch_name = branch_name.lower()
    
    if branch_name.startswith('upgrade/'):
        major += 1
        minor = 0
        patch = 0
    elif branch_name.startswith('feature/'):
        minor += 1
        patch = 0
    elif branch_name.startswith('bugfix/') or branch_name.startswith('hotfix/'):
        patch += 1
    else:
        # Default to patch if no specific prefix found
        patch += 1
        
    return f"{major}.{minor}.{patch}"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python increment_version.py <current_version> <branch_name>")
        sys.exit(1)
        
    current_version = sys.argv[1]
    branch = sys.argv[2]
    
    # Extract branch name if it's a full ref (e.g., refs/heads/feature/xxx)
    if '/' in branch and not branch.startswith(('feature/', 'bugfix/', 'hotfix/', 'upgrade/')):
        parts = branch.split('/')
        if len(parts) > 2:
            branch = "/".join(parts[2:])
            
    new_version = increment_version(current_version, branch)
    print(new_version)
