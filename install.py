#!/usr/bin/env python3
"""
Automatic installation script for PDF to Excel Converter Pro
Installs all required dependencies and verifies the installation
"""

import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"   Error: {e}")
        if e.stdout:
            print(f"   Output: {e.stdout}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False

def install_python_dependencies():
    """Install Python dependencies using pip"""
    print("\n📦 Installing Python Dependencies...")
    
    # Upgrade pip first
    run_command(f"{sys.executable} -m pip install --upgrade pip", 
                "Upgrading pip")
    
    # Install required packages
    packages = [
        "pandas>=1.5.0",
        "pdfplumber>=0.7.0", 
        "tabula-py>=2.5.0",
        "openpyxl>=3.0.0",
        "pathlib2>=2.3.0",
        "flask>=2.3.0",
        "werkzeug>=2.3.0"
    ]
    
    for package in packages:
        success = run_command(f"{sys.executable} -m pip install {package}", 
                            f"Installing {package}")
        if not success:
            return False
    
    return True

def check_java():
    """Check if Java is installed"""
    print("\n☕ Checking Java Installation...")
    try:
        result = subprocess.run(['java', '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Java is already installed")
            return True
        else:
            print("❌ Java installation issue")
            return False
    except FileNotFoundError:
        print("❌ Java not found")
        return False

def print_java_instructions():
    """Print instructions for installing Java"""
    print("\n☕ Java Installation Required:")
    print("   Java is required for the tabula-py library")
    print("   Please install Java manually:")
    
    system = platform.system().lower()
    if system == "darwin":  # macOS
        print("   macOS: brew install openjdk")
        print("   Or download from: https://www.oracle.com/java/technologies/downloads/")
    elif system == "linux":
        print("   Ubuntu/Debian: sudo apt-get install default-jdk")
        print("   CentOS/RHEL: sudo yum install java-1.8.0-openjdk")
    elif system == "windows":
        print("   Download from: https://www.oracle.com/java/technologies/downloads/")
    else:
        print("   Download from: https://www.oracle.com/java/technologies/downloads/")

def main():
    """Main installation function"""
    print("🚀 PDF to Excel Converter Pro - Auto Installer")
    print("=" * 60)
    
    print("This installer will set up all required dependencies")
    print("for the PDF to Excel Converter Pro tool.")
    
    # Check Python version
    print(f"\n🐍 Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print("   Please upgrade Python and try again")
        return False
    
    # Install Python dependencies
    if not install_python_dependencies():
        print("❌ Failed to install Python dependencies")
        return False
    
    # Check Java
    java_ok = check_java()
    if not java_ok:
        print_java_instructions()
    
    # Run final test
    print("\n🔧 Running Installation Test...")
    try:
        result = subprocess.run([sys.executable, 'test_installation.py'], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        success = result.returncode == 0
    except Exception as e:
        print(f"❌ Test failed: {e}")
        success = False
    
    print("\n" + "=" * 60)
    
    if success:
        print("🎉 Installation completed successfully!")
        print("\n🚀 You can now start using the converter:")
        print("   • GUI Version: python gui_converter.py")
        print("   • Web Version: python web_app.py")
        print("   • CLI Version: python pdf_to_excel_converter.py --help")
        print("   • Examples: python example_usage.py")
        
        print("\n💰 Next Steps:")
        print("   1. Test with a sample PDF file")
        print("   2. Read README.md for monetization ideas")
        print("   3. Start building your PDF conversion business!")
        
    else:
        print("❌ Installation completed with issues")
        print("   Please check the error messages above")
        if not java_ok:
            print("   Don't forget to install Java manually")
        print("   Run 'python test_installation.py' to verify fixes")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 