#!/usr/bin/env python3
"""
Build script for PDF to Excel Converter Pro Desktop Application
Automatically builds the executable using PyInstaller
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def check_dependencies():
    """Check if required build dependencies are installed"""
    print("🔍 Checking build dependencies...")
    
    # Check PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller installed")
    
    # Check main dependencies
    required_packages = ["pandas", "pdfplumber", "tabula", "openpyxl", "flask"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} found")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} not found")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages, check=True)
        print("✅ All dependencies installed")
    
    return True

def create_build_directory():
    """Create and clean build directory"""
    print("\n📁 Preparing build directory...")
    
    build_dir = Path("build")
    dist_dir = Path("dist")
    
    # Clean previous builds
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    print("✅ Build directory prepared")

def build_executable():
    """Build the executable using PyInstaller"""
    print("\n🔨 Building executable...")
    
    # Determine platform-specific settings
    system = platform.system().lower()
    
    if system == "windows":
        executable_name = "PDF_Excel_Converter_Pro.exe"
        icon_file = "icon.ico"
    elif system == "darwin":  # macOS
        executable_name = "PDF_Excel_Converter_Pro"
        icon_file = "icon.icns"
    else:  # Linux
        executable_name = "PDF_Excel_Converter_Pro"
        icon_file = None
    
    # Build command
    cmd = [
        "pyinstaller",
        "--onedir",  # One directory (easier to distribute)
        "--windowed",  # No console window
        "--name", "PDF_Excel_Converter_Pro",
        "--clean",  # Clean PyInstaller cache
        "--noconfirm",  # Overwrite output directory
    ]
    
    # Add icon if available
    if icon_file and os.path.exists(icon_file):
        cmd.extend(["--icon", icon_file])
    
    # Add additional files
    additional_files = [
        ("README.md", "."),
        ("LICENSE.txt", "."),
        ("marketing_materials.md", "."),
    ]
    
    for src, dst in additional_files:
        if os.path.exists(src):
            cmd.extend(["--add-data", f"{src}{os.pathsep}{dst}"])
    
    # Add hidden imports
    hidden_imports = [
        "pandas",
        "pdfplumber", 
        "tabula",
        "openpyxl",
        "tkinter",
        "tkinter.ttk",
        "tkinter.filedialog",
        "tkinter.messagebox",
        "tkinter.simpledialog",
        "tkinter.scrolledtext"
    ]
    
    for imp in hidden_imports:
        cmd.extend(["--hidden-import", imp])
    
    # Main script
    cmd.append("desktop_app.py")
    
    print(f"🚀 Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_installer():
    """Create installer package"""
    print("\n📦 Creating installer package...")
    
    dist_path = Path("dist/PDF_Excel_Converter_Pro")
    
    if not dist_path.exists():
        print("❌ Distribution directory not found")
        return False
    
    # Create README for distribution
    readme_content = """
# PDF to Excel Converter Pro

## Installation
1. Extract all files to a folder
2. Run PDF_Excel_Converter_Pro.exe (Windows) or PDF_Excel_Converter_Pro (Mac/Linux)
3. Follow the license activation process

## System Requirements
- Windows 10+ / macOS 10.14+ / Ubuntu 18.04+
- 4GB RAM minimum
- 500MB free disk space
- Java 8 or higher

## Support
For support, visit: https://your-website.com/support
Email: support@your-company.com

## License
This software is licensed under the terms in LICENSE.txt
    """
    
    with open(dist_path / "README.txt", "w") as f:
        f.write(readme_content)
    
    print("✅ Installer package created")
    return True

def test_executable():
    """Test the built executable"""
    print("\n🧪 Testing executable...")
    
    system = platform.system().lower()
    
    if system == "windows":
        exe_path = Path("dist/PDF_Excel_Converter_Pro/PDF_Excel_Converter_Pro.exe")
    else:
        exe_path = Path("dist/PDF_Excel_Converter_Pro/PDF_Excel_Converter_Pro")
    
    if not exe_path.exists():
        print(f"❌ Executable not found: {exe_path}")
        return False
    
    print(f"✅ Executable found: {exe_path}")
    print(f"📊 File size: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
    
    # Test if executable runs (quick test)
    try:
        # Start the process but don't wait for it to complete
        # Just verify it starts without immediate errors
        proc = subprocess.Popen([str(exe_path)], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
        
        # Give it a moment to start
        import time
        time.sleep(2)
        
        # Check if it's still running (good sign)
        if proc.poll() is None:
            print("✅ Executable starts successfully")
            proc.terminate()  # Clean shutdown
            return True
        else:
            print("❌ Executable exits immediately")
            stdout, stderr = proc.communicate()
            if stderr:
                print(f"Error: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing executable: {e}")
        return False

def main():
    """Main build process"""
    print("🚀 PDF to Excel Converter Pro - Build Script")
    print("=" * 50)
    
    try:
        # Step 1: Check dependencies
        if not check_dependencies():
            return False
        
        # Step 2: Prepare build directory
        create_build_directory()
        
        # Step 3: Build executable
        if not build_executable():
            return False
        
        # Step 4: Create installer package
        if not create_installer():
            return False
        
        # Step 5: Test executable
        if not test_executable():
            print("⚠️  Build completed but executable test failed")
            print("   Please test manually before distribution")
        
        print("\n" + "=" * 50)
        print("🎉 Build completed successfully!")
        print("\n📁 Output location:")
        print(f"   {os.path.abspath('dist/PDF_Excel_Converter_Pro')}")
        
        print("\n🚀 Next steps:")
        print("   1. Test the executable on your system")
        print("   2. Test on a clean machine without Python")
        print("   3. Create installer using NSIS or similar")
        print("   4. Add code signing for distribution")
        print("   5. Upload to your sales channels")
        
        print("\n💰 Ready to start selling!")
        print("   Check marketing_materials.md for sales strategies")
        
        return True
        
    except KeyboardInterrupt:
        print("\n❌ Build cancelled by user")
        return False
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 