#!/usr/bin/env python3
"""
Build script for Image Converter Pro executable
"""

import subprocess
import sys
import os

def build_image_converter():
    """Build the Image Converter Pro executable"""
    print("🔨 Building Image Converter Pro...")
    
    # Install dependencies
    print("📦 Installing dependencies...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'image_converter_requirements.txt'])
    
    # Create executable
    print("⚙️ Creating executable...")
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name', 'Image_Converter_Pro',
        '--add-data', 'image_converter_requirements.txt;.',
        'IMAGE_CONVERTER_STARTER.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Image Converter Pro built successfully!")
        print("📁 Find your executable in the 'dist' folder")
        print("💰 Ready to sell for $49-$99!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
        
    return True

if __name__ == "__main__":
    success = build_image_converter()
    
    if success:
        print("\n🎉 BUILD COMPLETE!")
        print("Your Image Converter Pro executable is ready!")
        print("\n💡 Next steps:")
        print("1. Test the executable")
        print("2. Create marketing materials")
        print("3. Set up sales page")
        print("4. Launch at $49-$99!")
    else:
        print("\n❌ Build failed. Please check the errors above.") 