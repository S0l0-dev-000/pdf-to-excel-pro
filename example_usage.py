#!/usr/bin/env python3
"""
Sample usage script for the PDF to Excel Converter Pro
Demonstrates various ways to use the converter programmatically
"""

from pdf_to_excel_converter import PDFToExcelConverter
import os

def main():
    """
    Examples of how to use the PDF to Excel converter
    """
    # Initialize the converter
    converter = PDFToExcelConverter()
    
    print("🚀 PDF to Excel Converter Pro - Sample Usage")
    print("=" * 50)
    
    # Example 1: Basic conversion
    print("\n1. Basic PDF to Excel conversion:")
    print("   converter.convert_pdf_to_excel('sample.pdf')")
    
    # Example 2: Convert with specific method
    print("\n2. Convert with specific extraction method:")
    print("   converter.convert_pdf_to_excel('sample.pdf', 'output.xlsx', 'tabula')")
    
    # Example 3: Batch conversion
    print("\n3. Batch convert all PDFs in a folder:")
    print("   converter.batch_convert('/path/to/pdf/folder')")
    
    # Example 4: Convert with custom output location
    print("\n4. Convert with custom output location:")
    print("   converter.convert_pdf_to_excel('input.pdf', '/custom/path/output.xlsx')")
    
    # Demonstration (uncomment to run with actual files)
    """
    try:
        # Make sure you have a sample PDF file
        sample_pdf = "sample.pdf"
        
        if os.path.exists(sample_pdf):
            print(f"\n✅ Converting {sample_pdf}...")
            
            # Convert using auto method
            result = converter.convert_pdf_to_excel(sample_pdf, method='auto')
            print(f"✅ Conversion completed! Output saved to: {result}")
            
            # Try different methods
            methods = ['tabula', 'pdfplumber', 'text']
            for method in methods:
                try:
                    output_file = f"output_{method}.xlsx"
                    result = converter.convert_pdf_to_excel(sample_pdf, output_file, method)
                    print(f"✅ {method} method completed: {result}")
                except Exception as e:
                    print(f"❌ {method} method failed: {e}")
        else:
            print(f"❌ Sample PDF file '{sample_pdf}' not found")
            print("   Please add a PDF file to test the converter")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    """
    
    print("\n" + "=" * 50)
    print("💡 Monetization Ideas:")
    print("   • Create a SaaS platform with subscription tiers")
    print("   • Offer freelance PDF conversion services")
    print("   • Build a desktop application for one-time purchase")
    print("   • Develop an API service for developers")
    print("   • Create WordPress plugins for website integration")
    
    print("\n📊 Business Use Cases:")
    print("   • Accounting firms: Convert financial reports")
    print("   • Real estate: Extract property data")
    print("   • Legal firms: Process legal documents")
    print("   • Consultants: Convert client reports")
    print("   • Data entry services: Automate PDF processing")
    
    print("\n🎯 Target Customers:")
    print("   • Small businesses needing data extraction")
    print("   • Freelancers offering conversion services")
    print("   • Developers integrating PDF features")
    print("   • Agencies adding automation to workflows")
    
    print("\n💰 Pricing Strategies:")
    print("   • Pay-per-conversion: $0.10 - $1.00")
    print("   • Monthly subscriptions: $19 - $199")
    print("   • One-time software: $29 - $499")
    print("   • Custom enterprise solutions: $500+")

if __name__ == "__main__":
    main() 