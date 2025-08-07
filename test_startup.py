"""
Quick test to verify the app can start and respond to health checks
"""
import asyncio
import aiohttp
import subprocess
import time
import sys
import os

async def test_health_check():
    """Test if the health check endpoint responds"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8000/') as response:
                data = await response.json()
                print(f"Root endpoint response: {data}")
                
            async with session.get('http://localhost:8000/health') as response:
                data = await response.json()
                print(f"Health endpoint response: {data}")
                return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def main():
    """Test the application startup"""
    print("Testing FastAPI app startup...")
    
    # Set environment variables for testing
    os.environ['PORT'] = '8000'
    os.environ['ENVIRONMENT'] = 'development'
    
    # Try to start the app
    try:
        print("Starting uvicorn server...")
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--log-level", "info"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for startup
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✓ Server started successfully")
            
            # Test health checks
            print("Testing health checks...")
            result = asyncio.run(test_health_check())
            
            if result:
                print("✓ Health checks passed")
            else:
                print("✗ Health checks failed")
                
        else:
            stdout, stderr = process.communicate()
            print("✗ Server failed to start")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            
        # Clean up
        if process.poll() is None:
            process.terminate()
            process.wait()
            
    except Exception as e:
        print(f"Error testing app: {e}")

if __name__ == "__main__":
    main()
