"""
Cleanup script to prepare repository for GitHub/Railway deployment
Removes unnecessary files and organizes structure
"""

import os
import shutil
from pathlib import Path

def cleanup_repo():
    """Clean up repository for deployment"""
    print("🧹 Cleaning up repository for deployment...")
    
    # Files to remove (development/testing only)
    files_to_remove = [
        "demo.py", 
        "demo_api.py",
        "launcher.py",
        "PROJECT_SUMMARY.py",
        "quick_test.py", 
        "setup_and_run.py",
        "start.bat",
        "start.sh", 
        "start_server.bat",
        "start_server.ps1",
        "test_api_endpoint.py",
        "test_curl.bat", 
        "test_direct.py",
        "test_openrouter.py",
        "ARCHITECTURE.md",
        "COMPETITION_READY.md",
        "DEPLOYMENT_READY.md",
        "SUBMISSION_CHECKLIST.md",
        "__pycache__"
    ]
    
    current_dir = Path(".")
    removed_count = 0
    
    for item in files_to_remove:
        item_path = current_dir / item
        if item_path.exists():
            try:
                if item_path.is_dir():
                    shutil.rmtree(item_path)
                    print(f"   Removed directory: {item}")
                else:
                    item_path.unlink()
                    print(f"   Removed file: {item}")
                removed_count += 1
            except Exception as e:
                print(f"   ⚠️ Could not remove {item}: {e}")
    
    print(f"\n✅ Cleanup complete! Removed {removed_count} items")
    
    # Show final structure
    print("\n📁 Final repository structure:")
    show_structure()

def show_structure():
    """Show the final clean repository structure"""
    important_files = [
        "main.py",
        "requirements.txt", 
        "railway.json",
        "Procfile",
        ".gitignore",
        ".env.example",
        "README.md",
        "DEPLOYMENT.md",
        "test_production.py",
        "src/",
        "tests/",
        ".github/"
    ]
    
    for item in important_files:
        if Path(item).exists():
            print(f"   ✅ {item}")
        else:
            print(f"   ❌ {item} (missing)")

def create_final_git_commands():
    """Create git commands for initial commit"""
    git_commands = """
# Git commands to deploy to GitHub and Railway:

# 1. Initialize git repository
git init

# 2. Add all files
git add .

# 3. Create initial commit
git commit -m "feat: HackRx LLM Query-Retrieval System

- FastAPI backend with competition endpoint
- OpenRouter/OpenAI GPT-4 integration  
- Document processing (PDF, DOCX, Email)
- Semantic search with vector similarity
- Railway deployment ready
- Competition-compliant API format"

# 4. Add your GitHub repository
git remote add origin https://github.com/yourusername/hackrx-llm-system.git

# 5. Push to GitHub
git branch -M main
git push -u origin main

# 6. Deploy to Railway:
# - Visit railway.app
# - Connect GitHub repo
# - Add OPENAI_API_KEY environment variable
# - Deploy automatically
"""
    
    with open("GIT_DEPLOY_COMMANDS.txt", "w") as f:
        f.write(git_commands)
    
    print(f"\n📝 Git commands saved to: GIT_DEPLOY_COMMANDS.txt")

if __name__ == "__main__":
    cleanup_repo()
    create_final_git_commands()
    
    print("\n🚀 Repository is now ready for deployment!")
    print("\n📋 Next steps:")
    print("   1. Review the structure above")
    print("   2. Check GIT_DEPLOY_COMMANDS.txt for git commands")
    print("   3. Push to GitHub")
    print("   4. Deploy to Railway")
    print("   5. Test with test_production.py")
    print("\n🎯 Your HackRx system is deployment-ready!")
