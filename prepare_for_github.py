#!/usr/bin/env python
"""
Prepare the DevShare server for GitHub
This script helps you prepare the server directory for uploading to GitHub
as a standalone repository.
"""

import os
import shutil
import sys

def print_header(message):
    """Print a formatted header message"""
    print(f"\n=== {message} ===")

def print_step(message):
    """Print a step message"""
    print(f"→ {message}")

def rename_file(source, target):
    """Rename a file if it exists"""
    if os.path.exists(source):
        print_step(f"Renaming {source} to {target}")
        if os.path.exists(target):
            os.remove(target)
        shutil.copy2(source, target)
        return True
    return False

def main():
    print_header("DevShare Server - GitHub Preparation Utility")
    print("This script will prepare your server directory for GitHub upload.")
    
    # Check if we're in the server directory
    if not os.path.exists("app.py"):
        print("Error: app.py not found. Please run this script from the server directory.")
        sys.exit(1)
    
    # Create .gitignore if it doesn't exist
    if not os.path.exists(".gitignore"):
        print_step("Creating .gitignore file")
        with open(".gitignore", "w") as f:
            f.write("""# Environment variables
.env
.env.local
.env.development
.env.production

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg
.venv
venv/
ENV/
.pytest_cache/
.coverage
htmlcov/

# System files
.DS_Store
Thumbs.db

# IDE files
.idea/
.vscode/
*.swp
*.swo
.project
.pydevproject
.settings/

# Logs
*.log
logs/
npm-debug.log*

# Local dev files
tmp/
temp/
""")
    
    # Create GitHub Actions directory if it doesn't exist
    github_dir = ".github/workflows"
    if not os.path.exists(github_dir):
        print_step(f"Creating {github_dir} directory")
        os.makedirs(github_dir, exist_ok=True)
        
        # Create GitHub Actions workflow file
        workflow_file = f"{github_dir}/python-test.yml"
        print_step(f"Creating {workflow_file}")
        with open(workflow_file, "w") as f:
            f.write("""name: Python Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install pytest pytest-cov
    - name: Lint with flake8
      run: |
        pip install flake8
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    - name: Test with pytest
      run: |
        pytest
""")
    
    # Check if LICENSE file exists; if not, create one
    if not os.path.exists("LICENSE"):
        print_step("Creating LICENSE file (MIT License)")
        with open("LICENSE", "w") as f:
            f.write("""MIT License

Copyright (c) 2023 Ritik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")
    
    # Make sure the DEPLOY.md file exists
    if not os.path.exists("DEPLOY.md"):
        if os.path.exists("deploy_instructions.md"):
            print_step("Renaming deploy_instructions.md to DEPLOY.md")
            shutil.copy2("deploy_instructions.md", "DEPLOY.md")
    
    print_header("Preparation Complete")
    print("Your server directory is now ready for GitHub!")
    print("\nNext steps:")
    print("1. Create a new GitHub repository (e.g., 'DevShare-server')")
    print("2. Initialize git repository and commit all files:")
    print("   $ git init")
    print("   $ git add .")
    print("   $ git commit -m \"Initial commit\"")
    print("3. Add the GitHub repository as remote and push:")
    print("   $ git remote add origin https://github.com/YOUR_USERNAME/DevShare-server.git")
    print("   $ git branch -M main")
    print("   $ git push -u origin main")
    print("\nNote: Desktop client repository: https://github.com/Rkcr7/DevShare")

if __name__ == "__main__":
    main() 