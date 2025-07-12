#!/usr/bin/env python3
"""
Installation test script for PDF to Excel Converter Pro
Verifies that all dependencies are installed correctly
"""

import sys
import subprocess

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ {module_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - FAILED: {e}")
        if package_name:
            print(f"   Install with: pip install {package_name}")
        return False

def test_java():
    """Test if Java is available (required for tabula-py)"""
    try:
        result = subprocess.run(['java', '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Java - OK")
            return True
        else:
            print("❌ Java - FAILED")
            print("   Java is required for tabula-py")
            print("   Install Java from: https://www.oracle.com/java/technologies/downloads/")
            return False
    except FileNotFoundError:
        print("❌ Java - NOT FOUND")
        print("   Java is required for tabula-py")
        print("   Install Java from: https://www.oracle.com/java/technologies/downloads/")
        return False

def main():
    """Run all installation tests"""
    print("🚀 PDF to Excel Converter Pro - Installation Test")
    print("=" * 60)
    
    print("\n📦 Testing Python Dependencies:")
    dependencies = [
        ('pandas', 'pandas'),
        ('pdfplumber', 'pdfplumber'),
        ('tabula', 'tabula-py'),
        ('openpyxl', 'openpyxl'),
        ('pathlib', 'pathlib2'),
        ('argparse', None),  # Built-in module
        ('flask', 'flask'),
        ('werkzeug', 'werkzeug'),
        ('tkinter', None),  # Built-in module (usually)
    ]
    
    failed_imports = []
    for module, package in dependencies:
        if not test_import(module, package):
            failed_imports.append((module, package))
    
    print("\n☕ Testing Java (required for tabula-py):")
    java_ok = test_java()
    
    print("\n🔧 Testing Core Functionality:")
    try:
        from pdf_to_excel_converter import PDFToExcelConverter
        converter = PDFToExcelConverter()
        print("✅ PDF to Excel Converter - OK")
        core_ok = True
    except Exception as e:
        print(f"❌ PDF to Excel Converter - FAILED: {e}")
        core_ok = False
    
    print("\n" + "=" * 60)
    
    if not failed_imports and java_ok and core_ok:
        print("🎉 All tests passed! Your installation is ready.")
        print("\n🚀 You can now:")
        print("   • Run GUI: python gui_converter.py")
        print("   • Run Web App: python web_app.py")
        print("   • Use CLI: python pdf_to_excel_converter.py --help")
        print("   • See examples: python example_usage.py")
        
        print("\n💰 Ready to start making money!")
        print("   • Check README.md for monetization ideas")
        print("   • Test with a sample PDF file")
        print("   • Start building your PDF conversion business")
        
    else:
        print("❌ Some tests failed. Please fix the following:")
        
        if failed_imports:
            print(f"\n📦 Missing Python packages ({len(failed_imports)}):")
            for module, package in failed_imports:
                if package:
                    print(f"   pip install {package}")
        
        if not java_ok:
            print("\n☕ Java installation required:")
            print("   Download from: https://www.oracle.com/java/technologies/downloads/")
        
        if not core_ok:
            print("\n🔧 Core functionality issues:")
            print("   Check that all dependencies are installed correctly")
        
        print("\n🔄 After fixing issues, run this test again:")
        print("   python test_installation.py")
    
    print("\n" + "=" * 60)
    return len(failed_imports) == 0 and java_ok and core_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 