from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
import os
import tempfile
import shutil
from werkzeug.utils import secure_filename
from pdf_to_excel_converter import PDFToExcelConverter
import logging
import uuid
from datetime import datetime
import io

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Initialize converter
converter = PDFToExcelConverter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    method = request.form.get('method', 'auto')
    
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and file.filename and allowed_file(file.filename):
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
        
        try:
            # Save uploaded file
            file.save(pdf_path)
            
            # Convert to Excel
            output_filename = f"{unique_id}_{filename.rsplit('.', 1)[0]}_converted.xlsx"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            
            converter.convert_pdf_to_excel(pdf_path, output_path, method)
            
            # Clean up uploaded file
            os.remove(pdf_path)
            
            # Return success with download link
            return jsonify({
                'success': True,
                'message': 'Conversion completed successfully!',
                'download_url': url_for('download_file', filename=output_filename)
            })
            
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            # Clean up files on error
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            if os.path.exists(output_path):
                os.remove(output_path)
            
            return jsonify({
                'success': False,
                'message': f'Conversion failed: {str(e)}'
            })
    
    else:
        flash('Please upload a valid PDF file')
        return redirect(request.url)

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            flash('File not found')
            return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Download failed: {e}")
        flash('Download failed')
        return redirect(url_for('index'))

@app.route('/api/convert', methods=['POST'])
def api_convert():
    """API endpoint for programmatic access"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    method = request.form.get('method', 'auto')
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400
    
    try:
        # Create temporary files
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_input:
            file.save(tmp_input.name)
            input_path = tmp_input.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_output:
            output_path = tmp_output.name
        
        # Convert
        converter.convert_pdf_to_excel(input_path, output_path, method)
        
        # Read the output file
        with open(output_path, 'rb') as f:
            excel_data = f.read()
        
        # Clean up temporary files
        os.unlink(input_path)
        os.unlink(output_path)
        
                          return send_file(
             io.BytesIO(excel_data),
             mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
             as_attachment=True,
             download_name=f"{file.filename.rsplit('.', 1)[0] if file.filename else 'converted'}_converted.xlsx"
         )
        
    except Exception as e:
        logger.error(f"API conversion failed: {e}")
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500

# Clean up old files periodically (simple implementation)
@app.route('/cleanup')
def cleanup_files():
    """Clean up old files (call this via cron job in production)"""
    try:
        now = datetime.now()
        for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    # Delete files older than 1 hour
                    if (now.timestamp() - os.path.getctime(file_path)) > 3600:
                        os.remove(file_path)
        
        return jsonify({'message': 'Cleanup completed'})
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        return jsonify({'error': 'Cleanup failed'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 