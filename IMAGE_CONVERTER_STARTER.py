#!/usr/bin/env python3
"""
🚀 Image Converter Pro - Starter Template
Your next $49-$99 profitable software!

Similar to your PDF converter but for images - huge market!
Target: Photographers, designers, small businesses, social media managers

Features to include:
- Convert between formats (JPG, PNG, GIF, BMP, WebP, TIFF)
- Batch processing
- Image resizing/compression
- Watermarking
- Basic editing (rotate, crop, filters)
- Professional licensing system
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import os
from pathlib import Path
import threading
import json
from datetime import datetime

class ImageConverterPro:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Converter Pro")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # License system (same as PDF converter)
        self.license_key = ""
        self.is_licensed = False
        self.trial_uses = 0
        self.max_trial_uses = 5
        
        # Image processing variables
        self.input_files = []
        self.output_format = "PNG"
        self.output_quality = 95
        self.resize_enabled = False
        self.resize_width = 800
        self.resize_height = 600
        
        self.setup_ui()
        self.load_license()
        
    def setup_ui(self):
        """Create the user interface"""
        # Title
        title_label = tk.Label(self.root, text="Image Converter Pro", 
                             font=("Arial", 24, "bold"), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=20)
        
        # License status
        self.license_label = tk.Label(self.root, text="", font=("Arial", 10), bg='#f0f0f0')
        self.license_label.pack(pady=5)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - File selection
        left_frame = tk.LabelFrame(main_frame, text="Input Files", font=("Arial", 12, "bold"), 
                                 bg='#f0f0f0', fg='#2c3e50')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # File selection buttons
        btn_frame = tk.Frame(left_frame, bg='#f0f0f0')
        btn_frame.pack(pady=10, padx=10, fill='x')
        
        tk.Button(btn_frame, text="Add Images", command=self.add_images,
                 bg='#3498db', fg='white', font=("Arial", 10, "bold"), padx=20).pack(side='left')
        
        tk.Button(btn_frame, text="Add Folder", command=self.add_folder,
                 bg='#9b59b6', fg='white', font=("Arial", 10, "bold"), padx=20).pack(side='left', padx=(10, 0))
        
        tk.Button(btn_frame, text="Clear All", command=self.clear_files,
                 bg='#e74c3c', fg='white', font=("Arial", 10, "bold"), padx=20).pack(side='left', padx=(10, 0))
        
        # File list
        self.file_listbox = tk.Listbox(left_frame, height=15, font=("Arial", 9))
        self.file_listbox.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Right panel - Settings
        right_frame = tk.LabelFrame(main_frame, text="Conversion Settings", 
                                  font=("Arial", 12, "bold"), bg='#f0f0f0', fg='#2c3e50')
        right_frame.pack(side='right', fill='y', padx=(10, 0))
        
        # Output format
        format_frame = tk.Frame(right_frame, bg='#f0f0f0')
        format_frame.pack(pady=10, padx=10, fill='x')
        
        tk.Label(format_frame, text="Output Format:", font=("Arial", 10, "bold"), 
                bg='#f0f0f0').pack(anchor='w')
        
        self.format_var = tk.StringVar(value="PNG")
        formats = ["PNG", "JPG", "GIF", "BMP", "WebP", "TIFF"]
        
        format_menu = ttk.Combobox(format_frame, textvariable=self.format_var, 
                                 values=formats, state='readonly', width=15)
        format_menu.pack(pady=5)
        
        # Quality setting (for JPG)
        quality_frame = tk.Frame(right_frame, bg='#f0f0f0')
        quality_frame.pack(pady=10, padx=10, fill='x')
        
        tk.Label(quality_frame, text="Quality (JPG only):", font=("Arial", 10, "bold"), 
                bg='#f0f0f0').pack(anchor='w')
        
        self.quality_var = tk.IntVar(value=95)
        quality_scale = tk.Scale(quality_frame, from_=10, to=100, orient='horizontal',
                               variable=self.quality_var, bg='#f0f0f0')
        quality_scale.pack(fill='x', pady=5)
        
        # Resize option
        resize_frame = tk.LabelFrame(right_frame, text="Resize Options", 
                                   font=("Arial", 10, "bold"), bg='#f0f0f0')
        resize_frame.pack(pady=10, padx=10, fill='x')
        
        self.resize_var = tk.BooleanVar()
        resize_check = tk.Checkbutton(resize_frame, text="Enable Resize", 
                                    variable=self.resize_var, bg='#f0f0f0',
                                    font=("Arial", 9))
        resize_check.pack(anchor='w', pady=5)
        
        # Width/Height
        size_frame = tk.Frame(resize_frame, bg='#f0f0f0')
        size_frame.pack(fill='x', pady=5)
        
        tk.Label(size_frame, text="Width:", bg='#f0f0f0', font=("Arial", 9)).pack(side='left')
        self.width_var = tk.StringVar(value="800")
        tk.Entry(size_frame, textvariable=self.width_var, width=8, font=("Arial", 9)).pack(side='left', padx=5)
        
        tk.Label(size_frame, text="Height:", bg='#f0f0f0', font=("Arial", 9)).pack(side='left')
        self.height_var = tk.StringVar(value="600")
        tk.Entry(size_frame, textvariable=self.height_var, width=8, font=("Arial", 9)).pack(side='left', padx=5)
        
        # Output directory
        output_frame = tk.Frame(right_frame, bg='#f0f0f0')
        output_frame.pack(pady=10, padx=10, fill='x')
        
        tk.Label(output_frame, text="Output Directory:", font=("Arial", 10, "bold"), 
                bg='#f0f0f0').pack(anchor='w')
        
        self.output_dir_var = tk.StringVar(value=str(Path.home() / "Downloads"))
        tk.Entry(output_frame, textvariable=self.output_dir_var, width=20, 
                font=("Arial", 9)).pack(pady=5)
        
        tk.Button(output_frame, text="Browse", command=self.browse_output_dir,
                 bg='#34495e', fg='white', font=("Arial", 9)).pack()
        
        # Convert button
        convert_frame = tk.Frame(self.root, bg='#f0f0f0')
        convert_frame.pack(pady=20)
        
        self.convert_btn = tk.Button(convert_frame, text="Convert Images", 
                                   command=self.convert_images,
                                   bg='#27ae60', fg='white', 
                                   font=("Arial", 16, "bold"), 
                                   padx=30, pady=10)
        self.convert_btn.pack()
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, mode='determinate')
        self.progress.pack(pady=10, padx=20, fill='x')
        
        # Status label
        self.status_label = tk.Label(self.root, text="Ready to convert images", 
                                   font=("Arial", 10), bg='#f0f0f0')
        self.status_label.pack(pady=5)
        
        # License entry (bottom)
        license_frame = tk.Frame(self.root, bg='#f0f0f0')
        license_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(license_frame, text="License Key:", font=("Arial", 10), 
                bg='#f0f0f0').pack(side='left')
        
        self.license_entry = tk.Entry(license_frame, font=("Arial", 10), width=30)
        self.license_entry.pack(side='left', padx=10)
        
        tk.Button(license_frame, text="Activate", command=self.activate_license,
                 bg='#e67e22', fg='white', font=("Arial", 10)).pack(side='left')
        
        self.update_license_status()
        
    def add_images(self):
        """Add individual image files"""
        files = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff *.webp"),
                ("All files", "*.*")
            ]
        )
        
        for file in files:
            if file not in self.input_files:
                self.input_files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))
                
    def add_folder(self):
        """Add all images from a folder"""
        folder = filedialog.askdirectory(title="Select Folder with Images")
        if folder:
            image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}
            
            for file_path in Path(folder).rglob('*'):
                if file_path.suffix.lower() in image_extensions:
                    file_str = str(file_path)
                    if file_str not in self.input_files:
                        self.input_files.append(file_str)
                        self.file_listbox.insert(tk.END, file_path.name)
                        
    def clear_files(self):
        """Clear all selected files"""
        self.input_files.clear()
        self.file_listbox.delete(0, tk.END)
        
    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir_var.set(directory)
            
    def load_license(self):
        """Load license information"""
        try:
            if os.path.exists('image_converter_license.json'):
                with open('image_converter_license.json', 'r') as f:
                    data = json.load(f)
                    self.license_key = data.get('key', '')
                    self.is_licensed = data.get('licensed', False)
                    self.trial_uses = data.get('trial_uses', 0)
        except:
            pass
            
    def save_license(self):
        """Save license information"""
        data = {
            'key': self.license_key,
            'licensed': self.is_licensed,
            'trial_uses': self.trial_uses
        }
        with open('image_converter_license.json', 'w') as f:
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
            self.license_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid license key!")
            
    def validate_license(self, key):
        """Validate license key"""
        valid_keys = [
            "IMAGE-CONVERTER-PRO-2024-PREMIUM",
            "IMAGE-CONVERTER-PRO-2024-STANDARD",
            "IMAGE-CONVERTER-PRO-2024-BASIC"
        ]
        return key in valid_keys
        
    def update_license_status(self):
        """Update license status display"""
        if self.is_licensed:
            self.license_label.config(text="✅ Licensed Version - Full Access", fg='green')
        else:
            remaining = self.max_trial_uses - self.trial_uses
            self.license_label.config(text=f"🔄 Trial Version ({remaining} conversions remaining)", 
                                    fg='orange')
            
    def convert_images(self):
        """Start image conversion process"""
        if not self.input_files:
            messagebox.showerror("Error", "Please select images to convert!")
            return
            
        # Check license
        if not self.is_licensed:
            if self.trial_uses >= self.max_trial_uses:
                messagebox.showerror("Trial Expired", 
                                   "Trial version expired! Please purchase a license to continue.")
                return
            self.trial_uses += 1
            self.save_license()
            self.update_license_status()
            
        # Start conversion in separate thread
        self.convert_btn.config(state='disabled')
        self.progress.config(maximum=len(self.input_files))
        self.status_label.config(text="Converting images...")
        
        thread = threading.Thread(target=self.perform_conversion)
        thread.daemon = True
        thread.start()
        
    def perform_conversion(self):
        """Perform the actual image conversion"""
        try:
            output_format = self.format_var.get()
            quality = self.quality_var.get()
            resize_enabled = self.resize_var.get()
            output_dir = Path(self.output_dir_var.get())
            
            if resize_enabled:
                try:
                    width = int(self.width_var.get())
                    height = int(self.height_var.get())
                except ValueError:
                    self.root.after(0, self.conversion_error, "Invalid width/height values!")
                    return
            
            # Create output directory if it doesn't exist
            output_dir.mkdir(parents=True, exist_ok=True)
            
            successful_conversions = 0
            
            for i, input_file in enumerate(self.input_files):
                try:
                    # Open image
                    with Image.open(input_file) as img:
                        # Convert to RGB if saving as JPG
                        if output_format == "JPG" and img.mode != "RGB":
                            img = img.convert("RGB")
                        
                        # Resize if enabled
                        if resize_enabled:
                            img = img.resize((width, height), Image.Resampling.LANCZOS)
                        
                        # Generate output filename
                        input_path = Path(input_file)
                        output_filename = f"{input_path.stem}.{output_format.lower()}"
                        output_path = output_dir / output_filename
                        
                        # Save image
                        save_kwargs = {}
                        if output_format == "JPG":
                            save_kwargs['quality'] = quality
                            save_kwargs['optimize'] = True
                        
                        img.save(output_path, format=output_format, **save_kwargs)
                        successful_conversions += 1
                        
                except Exception as e:
                    print(f"Error converting {input_file}: {e}")
                    
                # Update progress
                self.root.after(0, self.update_progress, i + 1)
                
            # Conversion complete
            self.root.after(0, self.conversion_complete, successful_conversions)
            
        except Exception as e:
            self.root.after(0, self.conversion_error, str(e))
            
    def update_progress(self, value):
        """Update progress bar"""
        self.progress['value'] = value
        self.status_label.config(text=f"Converting... {value}/{len(self.input_files)}")
        
    def conversion_complete(self, successful_conversions):
        """Handle successful conversion"""
        self.convert_btn.config(state='normal')
        self.progress['value'] = 0
        
        message = f"✅ Conversion complete!\\n\\n"
        message += f"Successfully converted: {successful_conversions} images\\n"
        message += f"Output directory: {self.output_dir_var.get()}"
        
        self.status_label.config(text=f"✅ Converted {successful_conversions} images successfully!")
        messagebox.showinfo("Success", message)
        
    def conversion_error(self, error_msg):
        """Handle conversion error"""
        self.convert_btn.config(state='normal')
        self.progress['value'] = 0
        self.status_label.config(text=f"❌ Conversion failed: {error_msg}")
        messagebox.showerror("Error", f"Conversion failed: {error_msg}")
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ImageConverterPro()
    app.run() 