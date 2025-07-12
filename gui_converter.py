import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import threading
import os
from pdf_to_excel_converter import PDFToExcelConverter
import logging

class PDFConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Excel Converter Pro")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize converter
        self.converter = PDFToExcelConverter()
        
        # Variables
        self.pdf_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.method = tk.StringVar(value='auto')
        self.batch_mode = tk.BooleanVar()
        
        self.create_widgets()
        self.setup_logging()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="PDF to Excel Converter Pro", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(input_frame, text="PDF File/Folder:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.pdf_path, width=50).grid(row=0, column=1, padx=(10, 5))
        ttk.Button(input_frame, text="Browse", command=self.browse_input).grid(row=0, column=2)
        
        ttk.Checkbutton(input_frame, text="Batch Mode (Select Folder)", 
                       variable=self.batch_mode).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(output_frame, text="Output Path:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(output_frame, textvariable=self.output_path, width=50).grid(row=0, column=1, padx=(10, 5))
        ttk.Button(output_frame, text="Browse", command=self.browse_output).grid(row=0, column=2)
        
        # Method selection
        method_frame = ttk.LabelFrame(main_frame, text="Extraction Method", padding="10")
        method_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        methods = [
            ('Auto (Recommended)', 'auto'),
            ('Tabula (Best for Tables)', 'tabula'),
            ('PDFPlumber (Complex Layouts)', 'pdfplumber'),
            ('Text Extraction', 'text')
        ]
        
        for i, (text, value) in enumerate(methods):
            ttk.Radiobutton(method_frame, text=text, variable=self.method, 
                           value=value).grid(row=i//2, column=i%2, sticky=tk.W, padx=10, pady=2)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        self.convert_button = ttk.Button(button_frame, text="Convert to Excel", 
                                        command=self.convert_files, style='Accent.TButton')
        self.convert_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Clear", command=self.clear_fields).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Help", command=self.show_help).pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Conversion Log", padding="10")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=80)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
    def setup_logging(self):
        # Create custom handler for GUI
        class GUIHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget
                
            def emit(self, record):
                msg = self.format(record)
                self.text_widget.insert(tk.END, msg + '\n')
                self.text_widget.see(tk.END)
                self.text_widget.update()
        
        # Set up logging
        gui_handler = GUIHandler(self.log_text)
        gui_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(gui_handler)
        logging.getLogger().setLevel(logging.INFO)
        
    def browse_input(self):
        if self.batch_mode.get():
            path = filedialog.askdirectory(title="Select folder containing PDF files")
        else:
            path = filedialog.askopenfilename(
                title="Select PDF file",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
        
        if path:
            self.pdf_path.set(path)
            
    def browse_output(self):
        if self.batch_mode.get():
            path = filedialog.askdirectory(title="Select output folder")
        else:
            path = filedialog.asksaveasfilename(
                title="Save Excel file as",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                defaultextension=".xlsx"
            )
        
        if path:
            self.output_path.set(path)
            
    def clear_fields(self):
        self.pdf_path.set("")
        self.output_path.set("")
        self.method.set("auto")
        self.batch_mode.set(False)
        self.log_text.delete(1.0, tk.END)
        
    def show_help(self):
        help_text = """
PDF to Excel Converter Pro Help

USAGE:
1. Select input PDF file or folder (for batch mode)
2. Choose output location
3. Select extraction method:
   - Auto: Tries multiple methods automatically
   - Tabula: Best for structured tables
   - PDFPlumber: Good for complex layouts
   - Text: Extracts all text as structured data
4. Click Convert to Excel

BATCH MODE:
- Select a folder containing PDF files
- All PDFs will be converted to Excel files
- Output folder will contain all converted files

TIPS:
- Use Auto method for best results
- Some PDFs may require specific methods
- Check the log for detailed information
- Large files may take several minutes

SUPPORTED FORMATS:
- Input: PDF files with selectable text
- Output: Excel (.xlsx) files
        """
        
        messagebox.showinfo("Help", help_text)
        
    def convert_files(self):
        if not self.pdf_path.get():
            messagebox.showerror("Error", "Please select a PDF file or folder")
            return
            
        # Disable convert button and start progress
        self.convert_button.config(state='disabled')
        self.progress.start()
        
        # Run conversion in thread to prevent GUI freezing
        thread = threading.Thread(target=self.run_conversion)
        thread.daemon = True
        thread.start()
        
    def run_conversion(self):
        try:
            if self.batch_mode.get():
                self.converter.batch_convert(
                    self.pdf_path.get(),
                    self.output_path.get() if self.output_path.get() else None,
                    self.method.get()
                )
            else:
                self.converter.convert_pdf_to_excel(
                    self.pdf_path.get(),
                    self.output_path.get() if self.output_path.get() else None,
                    self.method.get()
                )
            
            # Show success message
            self.root.after(0, self.conversion_complete, True)
            
        except Exception as e:
            logging.error(f"Conversion failed: {e}")
            self.root.after(0, self.conversion_complete, False)
            
    def conversion_complete(self, success):
        # Stop progress and enable button
        self.progress.stop()
        self.convert_button.config(state='normal')
        
        if success:
            messagebox.showinfo("Success", "Conversion completed successfully!")
        else:
            messagebox.showerror("Error", "Conversion failed. Check the log for details.")


def main():
    root = tk.Tk()
    app = PDFConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main() 