"""
Quick setup and test script for the HackRx system - Python 3.13 Compatible
"""

import os
import sys
import subprocess
import asyncio


def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Python version is compatible")
        if version.minor == 13:
            print("ℹ️  Using Python 3.13 - some packages may need newer versions")
        return True
    else:
        print("❌ Python 3.8+ required")
        return False


def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        # Upgrade pip first for Python 3.13 compatibility
        print("🔄 Upgrading pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install dependencies
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("\n💡 Try these troubleshooting steps:")
        print("   1. Update pip: python -m pip install --upgrade pip")
        print("   2. Try installing packages individually")
        print("   3. Use virtual environment: python -m venv venv && venv\\Scripts\\activate")
        return False


def setup_environment():
    """Setup environment file"""
    if not os.path.exists('.env'):
        print("📝 Setting up environment file...")
        with open('.env', 'w') as f:
            f.write("# Add your OpenAI API key here\n")
            f.write("OPENAI_API_KEY=sk-your-openai-api-key-here\n")
        print("✅ Created .env file")
        print("⚠️  Please edit .env and add your OpenAI API key")
        return False
    else:
        print("✅ Environment file already exists")
        return True


def check_api_key():
    """Check if API key is configured"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'sk-your-openai-api-key-here':
            print("⚠️  OpenAI API key not configured in .env file")
            return False
        print("✅ OpenAI API key found")
        return True
    except ImportError:
        print("❌ python-dotenv not installed")
        return False


async def run_demo():
    """Run the system demo"""
    print("\n🚀 Running system demo...")
    try:
        # Import and run basic tests first
        from tests.test_system import main as test_main
        await test_main()
    except Exception as e:
        print(f"❌ Demo failed: {e}")


def start_server():
    """Start the FastAPI server"""
    print("\n🌐 Starting FastAPI server...")
    print("Server will be available at: http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")


def install_alternative_packages():
    """Install alternative packages for Python 3.13 compatibility"""
    print("🔄 Installing Python 3.13 compatible packages...")
    
    alternative_packages = [
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0", 
        "pydantic>=2.6.0",
        "pydantic-settings>=2.1.0",
        "openai>=1.12.0",
        "numpy>=1.26.0",
        "scikit-learn>=1.4.0",
        "requests>=2.31.0",
        "aiohttp>=3.9.0",
        "httpx>=0.27.0",
        "python-dotenv>=1.0.0",
        "PyPDF2>=3.0.1",
        "python-docx>=1.1.0",
        "python-multipart>=0.0.9",
        "email-reply-parser>=0.5.12"
    ]
    
    for package in alternative_packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Failed to install {package}: {e}")
    
    print("✅ Alternative package installation completed")


def main():
    """Main setup and run function"""
    print("🎯 HackRx LLM-Powered Intelligent Query-Retrieval System")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Step 1: Try installing dependencies
    if not install_dependencies():
        print("\n🔄 Trying alternative installation method...")
        install_alternative_packages()
    
    # Step 2: Setup environment
    env_ready = setup_environment()
    
    # Step 3: Check API key
    if env_ready and not check_api_key():
        print("\n💡 Please add your OpenAI API key to the .env file and run again")
        print("   Example: OPENAI_API_KEY=sk-your-actual-key-here")
        return
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("\nAvailable options:")
    print("1. Run tests: python setup_and_run.py test")
    print("2. Start server: python setup_and_run.py server")
    print("3. Run demo: python demo.py")
    print("4. View docs: http://localhost:8000/docs (after starting server)")
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'test':
            asyncio.run(run_demo())
        
        elif command == 'server':
            if check_api_key():
                start_server()
            else:
                print("❌ Cannot start server without API key")
        
        else:
            print(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    main()
