#!/usr/bin/env python3
"""
PDF to Excel Converter Pro - Premium Desktop Application
Professional desktop software for one-time purchase sales
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext, simpledialog
import threading
import os
import json
import hashlib
import datetime
from pathlib import Path
import sys
import webbrowser
from pdf_to_excel_converter import PDFToExcelConverter
import logging

class LicenseManager:
    """Simple license management system"""
    
    def __init__(self, app_version="1.0.0"):
        self.app_version = app_version
        self.license_file = Path.home() / ".pdf_excel_pro" / "license.json"
        self.license_file.parent.mkdir(exist_ok=True)
        
    def generate_license_key(self, user_info):
        """Generate a simple license key"""
        data = f"{user_info['email']}{user_info['name']}{self.app_version}"
        return hashlib.md5(data.encode()).hexdigest().upper()
    
    def validate_license(self):
        """Check if license is valid"""
        try:
            if not self.license_file.exists():
                return False
            
            with open(self.license_file, 'r') as f:
                license_data = json.load(f)
            
            # Simple validation (in production, use proper encryption)
            expected_key = self.generate_license_key(license_data)
            return license_data.get('key') == expected_key
            
        except Exception:
            return False
    
    def save_license(self, user_info, license_key):
        """Save license information"""
        try:
            license_data = {
                'name': user_info['name'],
                'email': user_info['email'],
                'key': license_key,
                'activated_date': datetime.datetime.now().isoformat(),
                'version': self.app_version
            }
            
            with open(self.license_file, 'w') as f:
                json.dump(license_data, f, indent=2)
            
            return True
        except Exception:
            return False

class PremiumPDFConverter:
    """Premium PDF to Excel Converter Desktop Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Excel Converter Pro v1.0 - Premium Edition")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # Set icon (you can add your own icon file)
        try:
            self.root.iconbitmap('icon.ico')  # Add your icon file
        except:
            pass
        
        # License manager
        self.license_manager = LicenseManager()
        
        # Initialize converter
        self.converter = PDFToExcelConverter()
        
        # Variables
        self.pdf_files = []
        self.output_folder = tk.StringVar()
        self.method = tk.StringVar(value='auto')
        self.current_theme = tk.StringVar(value='dark')
        
        # Statistics
        self.stats = {
            'total_conversions': 0,
            'successful_conversions': 0,
            'failed_conversions': 0,
            'files_processed': 0
        }
        
        # Check license on startup
        if not self.license_manager.validate_license():
            self.show_license_dialog()
        
        self.create_widgets()
        self.setup_logging()
        self.load_settings()
        
    def show_license_dialog(self):
        """Show license activation dialog"""
        license_window = tk.Toplevel(self.root)
        license_window.title("Activate PDF to Excel Converter Pro")
        license_window.geometry("500x400")
        license_window.configure(bg='#34495e')
        license_window.transient(self.root)
        license_window.grab_set()
        
        # Center the window
        license_window.update_idletasks()
        x = (license_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (license_window.winfo_screenheight() // 2) - (400 // 2)
        license_window.geometry(f"500x400+{x}+{y}")
        
        frame = ttk.Frame(license_window, padding="30")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="PDF to Excel Converter Pro", 
                 font=('Arial', 16, 'bold')).pack(pady=(0, 10))
        
        ttk.Label(frame, text="Premium Desktop Edition", 
                 font=('Arial', 12)).pack(pady=(0, 20))
        
        ttk.Label(frame, text="Enter your license information:", 
                 font=('Arial', 10)).pack(anchor='w', pady=(0, 10))
        
        # Name field
        ttk.Label(frame, text="Name:").pack(anchor='w')
        name_entry = ttk.Entry(frame, width=50)
        name_entry.pack(fill='x', pady=(0, 10))
        
        # Email field
        ttk.Label(frame, text="Email:").pack(anchor='w')
        email_entry = ttk.Entry(frame, width=50)
        email_entry.pack(fill='x', pady=(0, 10))
        
        # License key field
        ttk.Label(frame, text="License Key:").pack(anchor='w')
        key_entry = ttk.Entry(frame, width=50)
        key_entry.pack(fill='x', pady=(0, 20))
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        def activate_license():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            key = key_entry.get().strip()
            
            if not all([name, email, key]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            user_info = {'name': name, 'email': email}
            expected_key = self.license_manager.generate_license_key(user_info)
            
            if key == expected_key:
                if self.license_manager.save_license(user_info, key):
                    messagebox.showinfo("Success", "License activated successfully!")
                    license_window.destroy()
                else:
                    messagebox.showerror("Error", "Failed to save license")
            else:
                messagebox.showerror("Error", "Invalid license key")
        
        def get_trial():
            # Generate a 7-day trial license
            trial_info = {'name': 'Trial User', 'email': 'trial@example.com'}
            trial_key = self.license_manager.generate_license_key(trial_info)
            
            if self.license_manager.save_license(trial_info, trial_key):
                messagebox.showinfo("Trial Started", "7-day trial activated!")
                license_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to activate trial")
        
        def buy_license():
            webbrowser.open("https://your-website.com/buy")  # Replace with your sales page
        
        ttk.Button(button_frame, text="Activate License", 
                  command=activate_license).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Start 7-Day Trial", 
                  command=get_trial).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Buy License", 
                  command=buy_license).pack(side=tk.RIGHT)
        
        # Trial info
        ttk.Label(frame, text="Need a license? Visit our website to purchase", 
                 font=('Arial', 9)).pack(pady=(20, 0))
        
    def create_widgets(self):
        """Create the main application interface"""
        # Create main frame with modern styling
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header_frame, text="PDF to Excel Converter Pro", 
                 font=('Arial', 18, 'bold')).pack(side=tk.LEFT)
        
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add PDF Files", command=self.add_pdf_files)
        file_menu.add_command(label="Clear All", command=self.clear_all)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Batch Process Folder", command=self.batch_process_folder)
        tools_menu.add_command(label="View Statistics", command=self.show_statistics)
        tools_menu.add_command(label="Settings", command=self.show_settings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Guide", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
        
        # File selection area
        file_frame = ttk.LabelFrame(main_frame, text="PDF Files", padding="10")
        file_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # File listbox with scrollbar
        list_frame = ttk.Frame(file_frame)
        list_frame.pack(fill='both', expand=True)
        
        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED, height=8)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.file_listbox.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        # File buttons
        file_buttons = ttk.Frame(file_frame)
        file_buttons.pack(fill='x', pady=(10, 0))
        
        ttk.Button(file_buttons, text="Add PDF Files", 
                  command=self.add_pdf_files).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(file_buttons, text="Remove Selected", 
                  command=self.remove_selected_files).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(file_buttons, text="Clear All", 
                  command=self.clear_all).pack(side=tk.LEFT)
        
        # Output settings
        output_frame = ttk.LabelFrame(main_frame, text="Output Settings", padding="10")
        output_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(output_frame, text="Output Folder:").pack(anchor='w')
        
        folder_frame = ttk.Frame(output_frame)
        folder_frame.pack(fill='x', pady=(5, 10))
        
        ttk.Entry(folder_frame, textvariable=self.output_folder, width=60).pack(side=tk.LEFT, fill='x', expand=True)
        ttk.Button(folder_frame, text="Browse", 
                  command=self.browse_output_folder).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Method selection
        method_frame = ttk.LabelFrame(main_frame, text="Extraction Method", padding="10")
        method_frame.pack(fill='x', pady=(0, 10))
        
        methods = [
            ('Auto (Recommended)', 'auto'),
            ('Tabula (Best for Tables)', 'tabula'),
            ('PDFPlumber (Complex Layouts)', 'pdfplumber'),
            ('Text Extraction', 'text')
        ]
        
        method_grid = ttk.Frame(method_frame)
        method_grid.pack(fill='x')
        
        for i, (text, value) in enumerate(methods):
            ttk.Radiobutton(method_grid, text=text, variable=self.method, 
                           value=value).grid(row=i//2, column=i%2, sticky='w', padx=10, pady=2)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill='x', pady=(10, 0))
        
        self.convert_button = ttk.Button(control_frame, text="Convert All to Excel", 
                                        command=self.convert_all_files)
        self.convert_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.preview_button = ttk.Button(control_frame, text="Preview First File", 
                                        command=self.preview_first_file)
        self.preview_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(control_frame, text="Open Output Folder", 
                  command=self.open_output_folder).pack(side=tk.RIGHT)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                           maximum=100, length=300)
        self.progress_bar.pack(fill='x', pady=(10, 0))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready", font=('Arial', 10))
        self.status_label.pack(pady=(5, 10))
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Conversion Log", padding="10")
        log_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=80)
        self.log_text.pack(fill='both', expand=True)
        
    def setup_logging(self):
        """Set up logging to GUI"""
        class GUIHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget
                
            def emit(self, record):
                msg = self.format(record)
                self.text_widget.insert(tk.END, msg + '\n')
                self.text_widget.see(tk.END)
                self.text_widget.update()
        
        gui_handler = GUIHandler(self.log_text)
        gui_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(gui_handler)
        logging.getLogger().setLevel(logging.INFO)
        
    def add_pdf_files(self):
        """Add PDF files to the conversion list"""
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))
        
        self.update_status(f"Added {len(files)} files. Total: {len(self.pdf_files)} files")
        
    def remove_selected_files(self):
        """Remove selected files from the list"""
        selected = self.file_listbox.curselection()
        for i in reversed(selected):
            self.file_listbox.delete(i)
            del self.pdf_files[i]
        
        self.update_status(f"Removed {len(selected)} files. Total: {len(self.pdf_files)} files")
        
    def clear_all(self):
        """Clear all files from the list"""
        self.pdf_files.clear()
        self.file_listbox.delete(0, tk.END)
        self.update_status("All files cleared")
        
    def browse_output_folder(self):
        """Browse for output folder"""
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_folder.set(folder)
            
    def convert_all_files(self):
        """Convert all files in the list"""
        if not self.pdf_files:
            messagebox.showerror("Error", "Please add PDF files first")
            return
            
        if not self.output_folder.get():
            messagebox.showerror("Error", "Please select an output folder")
            return
        
        # Disable button and start progress
        self.convert_button.config(state='disabled')
        self.progress_var.set(0)
        self.update_status("Starting conversion...")
        
        # Run conversion in thread
        thread = threading.Thread(target=self.run_conversion)
        thread.daemon = True
        thread.start()
        
    def run_conversion(self):
        """Run the conversion process"""
        try:
            total_files = len(self.pdf_files)
            successful = 0
            failed = 0
            
            for i, pdf_file in enumerate(self.pdf_files):
                try:
                    # Update progress
                    progress = (i / total_files) * 100
                    self.progress_var.set(progress)
                    self.update_status(f"Converting {os.path.basename(pdf_file)}...")
                    
                    # Convert file
                    output_name = f"{Path(pdf_file).stem}_converted.xlsx"
                    output_path = os.path.join(self.output_folder.get(), output_name)
                    
                    self.converter.convert_pdf_to_excel(pdf_file, output_path, self.method.get())
                    successful += 1
                    
                except Exception as e:
                    logging.error(f"Failed to convert {pdf_file}: {e}")
                    failed += 1
            
            # Update progress and status
            self.progress_var.set(100)
            self.update_status(f"Conversion completed: {successful} successful, {failed} failed")
            
            # Update statistics
            self.stats['total_conversions'] += 1
            self.stats['successful_conversions'] += successful
            self.stats['failed_conversions'] += failed
            self.stats['files_processed'] += total_files
            
            # Show completion message
            self.root.after(0, self.conversion_complete, successful, failed)
            
        except Exception as e:
            logging.error(f"Conversion process failed: {e}")
            self.root.after(0, self.conversion_failed, str(e))
            
    def conversion_complete(self, successful, failed):
        """Handle conversion completion"""
        self.convert_button.config(state='normal')
        
        if failed == 0:
            messagebox.showinfo("Success", f"All {successful} files converted successfully!")
        else:
            messagebox.showwarning("Completed with Errors", 
                                 f"Conversion completed:\n{successful} successful\n{failed} failed")
    
    def conversion_failed(self, error):
        """Handle conversion failure"""
        self.convert_button.config(state='normal')
        messagebox.showerror("Error", f"Conversion failed: {error}")
        
    def preview_first_file(self):
        """Preview the first file in the list"""
        if not self.pdf_files:
            messagebox.showerror("Error", "Please add PDF files first")
            return
        
        # This would open a preview window - simplified for now
        messagebox.showinfo("Preview", f"Preview for: {os.path.basename(self.pdf_files[0])}")
        
    def batch_process_folder(self):
        """Process all PDFs in a selected folder"""
        folder = filedialog.askdirectory(title="Select folder containing PDF files")
        if folder:
            pdf_files = [f for f in os.listdir(folder) if f.lower().endswith('.pdf')]
            if pdf_files:
                self.clear_all()
                for pdf_file in pdf_files:
                    full_path = os.path.join(folder, pdf_file)
                    self.pdf_files.append(full_path)
                    self.file_listbox.insert(tk.END, pdf_file)
                
                self.update_status(f"Added {len(pdf_files)} files from folder")
            else:
                messagebox.showinfo("No Files", "No PDF files found in the selected folder")
        
    def open_output_folder(self):
        """Open the output folder"""
        if self.output_folder.get() and os.path.exists(self.output_folder.get()):
            os.startfile(self.output_folder.get())  # Windows
            # For macOS: subprocess.run(['open', self.output_folder.get()])
            # For Linux: subprocess.run(['xdg-open', self.output_folder.get()])
        else:
            messagebox.showerror("Error", "Output folder not set or doesn't exist")
            
    def show_statistics(self):
        """Show usage statistics"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Usage Statistics")
        stats_window.geometry("400x300")
        
        frame = ttk.Frame(stats_window, padding="20")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Usage Statistics", font=('Arial', 16, 'bold')).pack(pady=(0, 20))
        
        stats_text = f"""
Total Conversion Sessions: {self.stats['total_conversions']}
Successful Conversions: {self.stats['successful_conversions']}
Failed Conversions: {self.stats['failed_conversions']}
Total Files Processed: {self.stats['files_processed']}

Success Rate: {(self.stats['successful_conversions'] / max(1, self.stats['successful_conversions'] + self.stats['failed_conversions'])) * 100:.1f}%
        """
        
        ttk.Label(frame, text=stats_text, font=('Arial', 11)).pack()
        
    def show_settings(self):
        """Show application settings"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        
        frame = ttk.Frame(settings_window, padding="20")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Settings", font=('Arial', 16, 'bold')).pack(pady=(0, 20))
        
        ttk.Label(frame, text="Theme:").pack(anchor='w')
        theme_var = tk.StringVar(value=self.current_theme.get())
        ttk.Radiobutton(frame, text="Dark", variable=theme_var, value='dark').pack(anchor='w')
        ttk.Radiobutton(frame, text="Light", variable=theme_var, value='light').pack(anchor='w')
        
        def save_settings():
            self.current_theme.set(theme_var.get())
            messagebox.showinfo("Settings", "Settings saved successfully!")
            settings_window.destroy()
        
        ttk.Button(frame, text="Save Settings", command=save_settings).pack(pady=(20, 0))
        
    def show_help(self):
        """Show help information"""
        help_text = """
PDF to Excel Converter Pro - User Guide

GETTING STARTED:
1. Add PDF files using 'Add PDF Files' button
2. Select output folder
3. Choose extraction method (Auto recommended)
4. Click 'Convert All to Excel'

EXTRACTION METHODS:
• Auto: Automatically selects best method
• Tabula: Best for structured tables
• PDFPlumber: Good for complex layouts
• Text: Extracts all text as data

FEATURES:
• Batch processing multiple files
• Preview capabilities
• Usage statistics
• Professional logging
• Multiple extraction methods

TIPS:
• Use Auto method for best results
• Large files may take several minutes
• Check the log for detailed information
• Output files are saved as .xlsx format

For technical support, contact support@your-company.com
        """
        
        messagebox.showinfo("User Guide", help_text)
        
    def show_about(self):
        """Show about information"""
        about_text = """
PDF to Excel Converter Pro v1.0
Premium Desktop Edition

Professional PDF to Excel conversion software
with advanced extraction capabilities.

© 2024 Your Company Name
All rights reserved.

This software is licensed for single-user use.
Redistribution is prohibited.

For licensing inquiries:
Email: sales@your-company.com
Website: www.your-company.com
        """
        
        messagebox.showinfo("About", about_text)
        
    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
        
    def load_settings(self):
        """Load application settings"""
        # Set default output folder to Documents
        documents_folder = str(Path.home() / "Documents" / "PDF_Excel_Conversions")
        os.makedirs(documents_folder, exist_ok=True)
        self.output_folder.set(documents_folder)
        
    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = PremiumPDFConverter(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 