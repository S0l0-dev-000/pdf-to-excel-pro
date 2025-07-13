#!/usr/bin/env python3
"""
Windows Build Script for PDF to Excel Converter Pro
Upload this to Replit, CodeSandbox, or Google Colab to build Windows executable
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install all required dependencies"""
    print("🔧 Installing dependencies...")
    
    packages = [
        'pandas>=1.5.0',
        'pdfplumber>=0.7.0', 
        'tabula-py>=2.5.0',
        'openpyxl>=3.0.0',
        'pathlib2>=2.3.0',
        'argparse>=1.4.0',
        'flask>=2.3.0',
        'werkzeug>=2.3.0',
        'pyinstaller>=5.0.0'
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    
    print("✅ Dependencies installed successfully!")

def build_windows_executable():
    """Build the Windows executable using PyInstaller"""
    print("🏗️ Building Windows executable...")
    
    # Build command for Windows
    build_cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name', 'PDF_Excel_Converter_Pro_Windows',
        'desktop_app.py'
    ]
    
    try:
        subprocess.check_call(build_cmd)
        print("✅ Windows executable built successfully!")
        print("📁 Check the 'dist' folder for your executable")
        
        # List contents of dist folder
        if os.path.exists('dist'):
            print("\n📦 Built files:")
            for file in os.listdir('dist'):
                filepath = os.path.join('dist', file)
                size = os.path.getsize(filepath) / (1024*1024)  # MB
                print(f"  - {file} ({size:.1f} MB)")
                
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True

def build_gui_version():
    """Build the simpler GUI version as backup"""
    print("🔄 Building GUI version as backup...")
    
    gui_cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name', 'PDF_Excel_Converter_GUI_Windows',
        'gui_converter.py'
    ]
    
    try:
        subprocess.check_call(gui_cmd)
        print("✅ GUI version built successfully!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ GUI build failed: {e}")

def main():
    """Main build process"""
    print("🚀 PDF to Excel Converter Pro - Windows Build Script")
    print("=" * 60)
    
    # Step 1: Install dependencies
    install_dependencies()
    
    # Step 2: Build main executable
    success = build_windows_executable()
    
    # Step 3: Build GUI version if main build succeeded
    if success:
        build_gui_version()
    
    print("\n🎉 Build process complete!")
    print("\n📋 Next steps:")
    print("1. Download files from 'dist' folder")
    print("2. Test on clean Windows machine")
    print("3. Package for distribution")
    print("4. Start selling! 💰")

if __name__ == "__main__":
    main() 