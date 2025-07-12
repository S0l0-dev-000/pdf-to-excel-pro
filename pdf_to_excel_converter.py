import pandas as pd
import pdfplumber
import tabula
import os
import sys
from pathlib import Path
import argparse
from typing import List, Dict, Any, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFToExcelConverter:
    """
    A comprehensive PDF to Excel converter that supports multiple extraction methods
    """
    
    def __init__(self):
        self.supported_formats = ['.pdf']
        
    def extract_tables_with_tabula(self, pdf_path: str) -> List[pd.DataFrame]:
        """
        Extract tables from PDF using tabula-py (best for structured tables)
        """
        try:
            logger.info(f"Extracting tables from {pdf_path} using tabula...")
            # Extract all tables from PDF
            tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
            logger.info(f"Found {len(tables)} tables using tabula")
            return tables
        except Exception as e:
            logger.error(f"Error with tabula extraction: {e}")
            return []
    
    def extract_tables_with_pdfplumber(self, pdf_path: str) -> List[pd.DataFrame]:
        """
        Extract tables from PDF using pdfplumber (good for complex layouts)
        """
        tables = []
        try:
            logger.info(f"Extracting tables from {pdf_path} using pdfplumber...")
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Extract tables from each page
                    page_tables = page.extract_tables()
                    for table_num, table in enumerate(page_tables):
                        if table:  # Check if table is not empty
                            # Convert table to DataFrame
                            df = pd.DataFrame(table[1:], columns=table[0])  # First row as headers
                            df.name = f"Page_{page_num + 1}_Table_{table_num + 1}"
                            tables.append(df)
            logger.info(f"Found {len(tables)} tables using pdfplumber")
        except Exception as e:
            logger.error(f"Error with pdfplumber extraction: {e}")
        return tables
    
    def extract_text_as_data(self, pdf_path: str) -> pd.DataFrame:
        """
        Extract all text from PDF and structure it as data
        """
        try:
            logger.info(f"Extracting text from {pdf_path}...")
            text_data = []
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        lines = text.split('\n')
                        for line_num, line in enumerate(lines):
                            if line.strip():  # Skip empty lines
                                text_data.append({
                                    'Page': page_num + 1,
                                    'Line': line_num + 1,
                                    'Content': line.strip()
                                })
            
            df = pd.DataFrame(text_data)
            logger.info(f"Extracted {len(text_data)} lines of text")
            return df
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return pd.DataFrame()
    
    def convert_pdf_to_excel(self, pdf_path: str, output_path: Optional[str] = None, method: str = 'auto') -> str:
        """
        Convert PDF to Excel using specified method
        
        Args:
            pdf_path: Path to the PDF file
            output_path: Path for the output Excel file (optional)
            method: 'tabula', 'pdfplumber', 'text', or 'auto'
        
        Returns:
            Path to the created Excel file
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Generate output path if not provided
        if output_path is None:
            pdf_name = Path(pdf_path).stem
            output_path = f"{pdf_name}_converted.xlsx"
        
        # Ensure output has .xlsx extension
        if not output_path.endswith('.xlsx'):
            output_path += '.xlsx'
        
        tables = []
        text_df = pd.DataFrame()
        
        # Extract data based on method
        if method == 'auto' or method == 'tabula':
            tables.extend(self.extract_tables_with_tabula(pdf_path))
        
        if method == 'auto' or method == 'pdfplumber':
            if not tables:  # Only try pdfplumber if tabula didn't find tables
                tables.extend(self.extract_tables_with_pdfplumber(pdf_path))
        
        if method == 'auto' or method == 'text':
            if not tables:  # Only extract text if no tables found
                text_df = self.extract_text_as_data(pdf_path)
        
        # Create Excel file
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            if tables:
                # Write each table to a separate sheet
                for i, table in enumerate(tables):
                    sheet_name = getattr(table, 'name', f'Table_{i+1}')
                    # Clean sheet name (Excel sheet names have restrictions)
                    sheet_name = sheet_name.replace('/', '_').replace('\\', '_')[:31]
                    table.to_excel(writer, sheet_name=sheet_name, index=False)
                    logger.info(f"Wrote table to sheet: {sheet_name}")
            
            if not text_df.empty:
                text_df.to_excel(writer, sheet_name='Text_Content', index=False)
                logger.info("Wrote text content to sheet: Text_Content")
            
            # If no data was extracted, create a summary sheet
            if not tables and text_df.empty:
                summary_df = pd.DataFrame({
                    'Status': ['No Data Found'],
                    'Message': ['No tables or structured data could be extracted from the PDF'],
                    'Suggestions': ['Try a different extraction method or check if the PDF contains selectable text']
                })
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                logger.warning("No data extracted - created summary sheet")
        
        logger.info(f"Conversion completed! Excel file saved as: {output_path}")
        return output_path
    
    def batch_convert(self, input_folder: str, output_folder: Optional[str] = None, method: str = 'auto'):
        """
        Convert multiple PDF files in a folder to Excel
        """
        if output_folder is None:
            output_folder = os.path.join(input_folder, 'converted_excel')
        
        os.makedirs(output_folder, exist_ok=True)
        
        pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {input_folder}")
            return
        
        logger.info(f"Found {len(pdf_files)} PDF files to convert")
        
        for pdf_file in pdf_files:
            try:
                pdf_path = os.path.join(input_folder, pdf_file)
                output_name = f"{Path(pdf_file).stem}_converted.xlsx"
                output_path = os.path.join(output_folder, output_name)
                
                logger.info(f"Converting {pdf_file}...")
                self.convert_pdf_to_excel(pdf_path, output_path, method)
                
            except Exception as e:
                logger.error(f"Error converting {pdf_file}: {e}")
        
        logger.info(f"Batch conversion completed! Files saved in: {output_folder}")


def main():
    """
    Command-line interface for the PDF to Excel converter
    """
    parser = argparse.ArgumentParser(description='Convert PDF files to Excel format')
    parser.add_argument('input', help='Input PDF file or folder path')
    parser.add_argument('-o', '--output', help='Output Excel file or folder path')
    parser.add_argument('-m', '--method', choices=['auto', 'tabula', 'pdfplumber', 'text'], 
                       default='auto', help='Extraction method (default: auto)')
    parser.add_argument('-b', '--batch', action='store_true', 
                       help='Batch convert all PDFs in input folder')
    
    args = parser.parse_args()
    
    converter = PDFToExcelConverter()
    
    try:
        if args.batch:
            converter.batch_convert(args.input, args.output, args.method)
        else:
            converter.convert_pdf_to_excel(args.input, args.output, args.method)
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 