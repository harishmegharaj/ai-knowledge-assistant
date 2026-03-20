#!/usr/bin/env python3
"""Setup script for AI Knowledge Assistant"""

import subprocess
import sys
import os

def run_command(cmd):
    """Run a shell command"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd="/Users/harishashokmegharaj/reactnext/AIML")
    if result.returncode != 0:
        print(f"Error: Command failed with code {result.returncode}")
        sys.exit(1)

def main():
    """Main setup function"""
    os.chdir("/Users/harishashokmegharaj/reactnext/AIML")
    
    print("🚀 AI Knowledge Assistant Setup")
    print("=" * 50)
    
    # Check if venv exists
    if os.path.exists("venv"):
        print("\n📦 Removing existing virtual environment...")
        import shutil
        shutil.rmtree("venv")
    
    # Create venv
    print("📦 Creating virtual environment...")
    run_command([sys.executable, "-m", "venv", "venv"])
    
    venv_python = os.path.join("venv", "bin", "python")
    venv_pip = os.path.join("venv", "bin", "pip")
    
    # Upgrade pip
    print("📦 Upgrading pip...")
    run_command([venv_pip, "install", "-U", "pip", "setuptools", "wheel"])
    
    # Install requirements
    print("📦 Installing dependencies...")
    run_command([venv_pip, "install", "-r", "requirements.txt"])
    
    # Verify installation
    print("✓ Verifying installation...")
    run_command([venv_python, "-c", "import langchain; import fastapi; print('✓ All core packages imported successfully!')"])
    
    print("\n" + "=" * 50)
    print("✓ Installation complete!")
    print("\nNext steps:")
    print("1. Activate: source venv/bin/activate")
    print("2. Configure: cp .env.example .env")
    print("3. Add your OPENAI_API_KEY to .env")
    print("4. Run: python -m uvicorn src.api.main:app --reload")

if __name__ == "__main__":
    main()
