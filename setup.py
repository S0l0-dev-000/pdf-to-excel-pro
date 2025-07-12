from cx_Freeze import setup, Executable
import sys
import os

# Dependencies are automatically detected, but it may need fine tuning.
build_exe_options = {
    "packages": [
        "tkinter", "pandas", "pdfplumber", "tabula", "openpyxl", 
        "pathlib", "logging", "threading", "json", "hashlib", "datetime"
    ],
    "excludes": ["test", "unittest", "distutils"],
    "include_files": [
        "README.md",
        "LICENSE.txt",
        ("templates/", "templates/"),
        ("icon.ico", "icon.ico") if os.path.exists("icon.ico") else None
    ],
    "zip_include_packages": ["*"],
    "zip_exclude_packages": []
}

# Filter out None values from include_files
build_exe_options["include_files"] = [f for f in build_exe_options["include_files"] if f is not None]

# GUI applications require a different base on Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="PDF to Excel Converter Pro",
    version="1.0.0",
    description="Professional PDF to Excel conversion software",
    author="Your Company Name",
    author_email="sales@your-company.com",
    url="https://your-website.com",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "desktop_app.py",
            base=base,
            target_name="PDF_Excel_Converter_Pro.exe" if sys.platform == "win32" else "PDF_Excel_Converter_Pro",
            icon="icon.ico" if os.path.exists("icon.ico") else None,
            shortcut_name="PDF to Excel Converter Pro",
            shortcut_dir="DesktopFolder"
        )
    ]
) 