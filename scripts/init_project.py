import os
import sys
from pathlib import Path

def create_directory_structure():
    """Create the project directory structure."""
    directories = [
        "app/core",
        "app/models",
        "app/schemas",
        "app/services",
        "app/api/v1/endpoints",
        "app/tests",
        "alembic/versions",
        "scripts",
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        # Create __init__.py files
        init_file = Path(directory) / "__init__.py"
        init_file.touch()

def create_empty_files():
    """Create empty required files."""
    files = [
        ".env",
        ".gitignore",
        "Dockerfile",
        "docker-compose.yml",
    ]
    
    for file in files:
        Path(file).touch()

def update_gitignore():
    """Update .gitignore with common Python patterns."""
    gitignore_content = """
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

# Virtual Environment
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment variables
.env

# Local development
*.log
*.sqlite
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content.strip())

def main():
    """Initialize the project structure."""
    print("Creating directory structure...")
    create_directory_structure()
    
    print("Creating empty files...")
    create_empty_files()
    
    print("Updating .gitignore...")
    update_gitignore()
    
    print("Project structure created successfully!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env and update the values")
    print("2. Create and activate a virtual environment")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Initialize database: alembic upgrade head")
    print("5. Run the application: uvicorn app.main:app --reload")

if __name__ == "__main__":
    main()