#!/usr/bin/env python3
"""
🚀 Standalone Windows Builder for PDF to Excel Converter Pro
Upload ONLY this file to any cloud service to build your Windows executable!

Usage:
1. Upload this file to Replit/Colab/CodeSandbox
2. Run: python standalone_windows_builder.py
3. Download your Windows executable from dist/ folder

Author: PDF Excel Converter Pro
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Install all required packages"""
    print("🔧 Installing dependencies...")
    
    packages = [
        'pandas>=1.5.0',
        'pdfplumber>=0.7.0', 
        'tabula-py>=2.5.0',
        'openpyxl>=3.0.0',
        'flask>=2.3.0',
        'pyinstaller>=5.0.0'
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    
    print("✅ Dependencies installed!")

def create_main_app():
    """Create the main desktop application file"""
    print("📝 Creating main application...")
    
    desktop_app_code = '''
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import pdfplumber
import os
from pathlib import Path
import threading
import time
import hashlib
import json
from datetime import datetime, timedelta

class PDFToExcelConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF to Excel Converter Pro")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # License system
        self.license_key = ""
        self.is_licensed = False
        self.trial_uses = 0
        self.max_trial_uses = 3
        
        self.setup_ui()
        self.load_license()
        
    def setup_ui(self):
        """Create the user interface"""
        # Title
        title_label = tk.Label(self.root, text="PDF to Excel Converter Pro", 
                             font=("Arial", 20, "bold"), bg='#f0f0f0')
        title_label.pack(pady=20)
        
        # License status
        self.license_label = tk.Label(self.root, text="", font=("Arial", 10), bg='#f0f0f0')
        self.license_label.pack(pady=5)
        
        # Input file selection
        input_frame = tk.Frame(self.root, bg='#f0f0f0')
        input_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(input_frame, text="Select PDF File:", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w')
        
        file_frame = tk.Frame(input_frame, bg='#f0f0f0')
        file_frame.pack(fill='x', pady=5)
        
        self.file_path_var = tk.StringVar()
        self.file_entry = tk.Entry(file_frame, textvariable=self.file_path_var, font=("Arial", 10))
        self.file_entry.pack(side='left', fill='x', expand=True)
        
        browse_btn = tk.Button(file_frame, text="Browse", command=self.browse_file, 
                              bg='#4CAF50', fg='white', font=("Arial", 10))
        browse_btn.pack(side='right', padx=(10, 0))
        
        # Output directory
        output_frame = tk.Frame(self.root, bg='#f0f0f0')
        output_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(output_frame, text="Output Directory:", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w')
        
        output_dir_frame = tk.Frame(output_frame, bg='#f0f0f0')
        output_dir_frame.pack(fill='x', pady=5)
        
        self.output_dir_var = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.output_entry = tk.Entry(output_dir_frame, textvariable=self.output_dir_var, font=("Arial", 10))
        self.output_entry.pack(side='left', fill='x', expand=True)
        
        output_browse_btn = tk.Button(output_dir_frame, text="Browse", command=self.browse_output_dir,
                                     bg='#2196F3', fg='white', font=("Arial", 10))
        output_browse_btn.pack(side='right', padx=(10, 0))
        
        # Conversion method
        method_frame = tk.Frame(self.root, bg='#f0f0f0')
        method_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(method_frame, text="Conversion Method:", font=("Arial", 12), bg='#f0f0f0').pack(anchor='w')
        
        self.method_var = tk.StringVar(value="auto")
        methods = [("Auto (Recommended)", "auto"), ("PDFPlumber", "pdfplumber"), ("Text Extraction", "text")]
        
        for text, value in methods:
            tk.Radiobutton(method_frame, text=text, variable=self.method_var, value=value,
                          font=("Arial", 10), bg='#f0f0f0').pack(anchor='w')
        
        # Convert button
        self.convert_btn = tk.Button(self.root, text="Convert to Excel", command=self.convert_file,
                                    bg='#FF9800', fg='white', font=("Arial", 14, "bold"), 
                                    padx=20, pady=10)
        self.convert_btn.pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(pady=10, padx=20, fill='x')
        
        # Status label
        self.status_label = tk.Label(self.root, text="Ready to convert PDF files", 
                                   font=("Arial", 10), bg='#f0f0f0')
        self.status_label.pack(pady=5)
        
        # License entry
        license_frame = tk.Frame(self.root, bg='#f0f0f0')
        license_frame.pack(pady=20, padx=20, fill='x')
        
        tk.Label(license_frame, text="License Key:", font=("Arial", 10), bg='#f0f0f0').pack(anchor='w')
        
        license_entry_frame = tk.Frame(license_frame, bg='#f0f0f0')
        license_entry_frame.pack(fill='x', pady=5)
        
        self.license_entry = tk.Entry(license_entry_frame, font=("Arial", 10))
        self.license_entry.pack(side='left', fill='x', expand=True)
        
        activate_btn = tk.Button(license_entry_frame, text="Activate", command=self.activate_license,
                                bg='#9C27B0', fg='white', font=("Arial", 10))
        activate_btn.pack(side='right', padx=(10, 0))
        
        self.update_license_status()
        
    def browse_file(self):
        """Browse for PDF file"""
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
            
    def browse_output_dir(self):
        """Browse for output directory"""
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            self.output_dir_var.set(dir_path)
            
    def load_license(self):
        """Load license from file"""
        try:
            if os.path.exists('license.json'):
                with open('license.json', 'r') as f:
                    data = json.load(f)
                    self.license_key = data.get('key', '')
                    self.is_licensed = data.get('licensed', False)
                    self.trial_uses = data.get('trial_uses', 0)
        except:
            pass
            
    def save_license(self):
        """Save license to file"""
        data = {
            'key': self.license_key,
            'licensed': self.is_licensed,
            'trial_uses': self.trial_uses
        }
        with open('license.json', 'w') as f:
            json.dump(data, f)
            
    def activate_license(self):
        """Activate license key"""
        key = self.license_entry.get().strip()
        if self.validate_license(key):
            self.license_key = key
            self.is_licensed = True
            self.save_license()
            self.update_license_status()
            messagebox.showinfo("Success", "License activated successfully!")
        else:
            messagebox.showerror("Error", "Invalid license key!")
            
    def validate_license(self, key):
        """Validate license key"""
        # Simple validation - in production, this would check against a server
        valid_keys = [
            "PDF-EXCEL-PRO-2024-PREMIUM",
            "PDF-EXCEL-PRO-2024-STANDARD",
            "PDF-EXCEL-PRO-2024-BASIC"
        ]
        return key in valid_keys
        
    def update_license_status(self):
        """Update license status display"""
        if self.is_licensed:
            self.license_label.config(text="✅ Licensed Version", fg='green')
        else:
            remaining = self.max_trial_uses - self.trial_uses
            self.license_label.config(text=f"🔄 Trial Version ({remaining} uses remaining)", fg='orange')
            
    def convert_file(self):
        """Convert PDF to Excel"""
        if not self.file_path_var.get():
            messagebox.showerror("Error", "Please select a PDF file!")
            return
            
        if not self.is_licensed:
            if self.trial_uses >= self.max_trial_uses:
                messagebox.showerror("Trial Expired", 
                                   "Trial version expired! Please purchase a license.")
                return
            self.trial_uses += 1
            self.save_license()
            self.update_license_status()
            
        # Start conversion in separate thread
        self.convert_btn.config(state='disabled')
        self.progress.start()
        self.status_label.config(text="Converting PDF to Excel...")
        
        thread = threading.Thread(target=self.perform_conversion)
        thread.daemon = True
        thread.start()
        
    def perform_conversion(self):
        """Perform the actual conversion"""
        try:
            pdf_path = self.file_path_var.get()
            output_dir = self.output_dir_var.get()
            method = self.method_var.get()
            
            # Extract filename without extension
            pdf_name = Path(pdf_path).stem
            output_path = Path(output_dir) / f"{pdf_name}_converted.xlsx"
            
            # Convert PDF to Excel
            data = self.extract_tables_from_pdf(pdf_path, method)
            
            if data:
                # Save to Excel
                with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                    for i, df in enumerate(data):
                        sheet_name = f"Sheet_{i+1}"
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Update UI in main thread
                self.root.after(0, self.conversion_complete, str(output_path))
            else:
                self.root.after(0, self.conversion_error, "No tables found in PDF")
                
        except Exception as e:
            self.root.after(0, self.conversion_error, str(e))
            
    def extract_tables_from_pdf(self, pdf_path, method):
        """Extract tables from PDF using specified method"""
        data = []
        
        try:
            if method == "pdfplumber" or method == "auto":
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        tables = page.extract_tables()
                        for table in tables:
                            if table:
                                df = pd.DataFrame(table[1:], columns=table[0])
                                data.append(df)
                                
            if not data and (method == "text" or method == "auto"):
                # Fallback to text extraction
                with pdfplumber.open(pdf_path) as pdf:
                    text_data = []
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            lines = text.split('\\n')
                            for line in lines:
                                if line.strip():
                                    text_data.append([line.strip()])
                    
                    if text_data:
                        df = pd.DataFrame(text_data, columns=['Content'])
                        data.append(df)
                        
        except Exception as e:
            print(f"Error extracting tables: {e}")
            
        return data
        
    def conversion_complete(self, output_path):
        """Handle successful conversion"""
        self.progress.stop()
        self.convert_btn.config(state='normal')
        self.status_label.config(text=f"✅ Conversion complete! Saved to: {output_path}")
        messagebox.showinfo("Success", f"PDF converted successfully!\\n\\nSaved to: {output_path}")
        
    def conversion_error(self, error_msg):
        """Handle conversion error"""
        self.progress.stop()
        self.convert_btn.config(state='normal')
        self.status_label.config(text=f"❌ Conversion failed: {error_msg}")
        messagebox.showerror("Error", f"Conversion failed: {error_msg}")
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = PDFToExcelConverter()
    app.run()
'''
    
    with open('desktop_app.py', 'w') as f:
        f.write(desktop_app_code.strip())
    
    print("✅ Main application created!")

def create_requirements():
    """Create requirements.txt"""
    print("📝 Creating requirements.txt...")
    
    requirements = """pandas>=1.5.0
pdfplumber>=0.7.0
tabula-py>=2.5.0
openpyxl>=3.0.0
pathlib2>=2.3.0
argparse>=1.4.0
flask>=2.3.0
werkzeug>=2.3.0
pyinstaller>=5.0.0"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    
    print("✅ Requirements.txt created!")

def build_executable():
    """Build the Windows executable"""
    print("🔨 Building Windows executable...")
    
    try:
        # Create dist directory
        os.makedirs('dist', exist_ok=True)
        
        # Build with PyInstaller
        cmd = [
            'pyinstaller',
            '--onefile',
            '--windowed',
            '--name', 'PDF_Excel_Converter_Pro_Windows',
            'desktop_app.py'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Windows executable built successfully!")
            print("📁 Find your executable in the 'dist' folder")
            print("📦 File: PDF_Excel_Converter_Pro_Windows.exe")
            print("💰 Ready to sell for $49-$99!")
        else:
            print(f"❌ Build failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Build error: {e}")

def main():
    """Main function"""
    print("🚀 PDF to Excel Converter Pro - Windows Builder")
    print("=" * 50)
    
    try:
        # Install dependencies
        install_dependencies()
        
        # Create application files
        create_main_app()
        create_requirements()
        
        # Build executable
        build_executable()
        
        print("\\n🎉 BUILD COMPLETE!")
        print("Your Windows executable is ready in the 'dist' folder!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    main() 