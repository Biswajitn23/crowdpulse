import os
import logging
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, jsonify, session
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import cv2
import numpy as np
from utils.detection import YOLODetector
from utils.video_processor import VideoProcessor
from utils.heatmap import HeatmapGenerator
import uuid
import json
from datetime import datetime
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "crowd_detection_secret_key_2024")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
CORS(app, origins=[
    "https://stirring-douhua-7a0209.netlify.app",
    "https://lucky-brioche-59abc6.netlify.app"
])

# Configuration
UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'}
MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25MB max file size (reduced for stability)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['UPLOAD_EXTENSIONS'] = ALLOWED_EXTENSIONS

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Initialize components
detector = YOLODetector()
processor = VideoProcessor(detector)
heatmap_gen = HeatmapGenerator()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with upload form"""
    return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def test_upload():
    """Test upload endpoint"""
    if request.method == 'POST':
        try:
            file = request.files.get('video')
            if file:
                return jsonify({
                    'status': 'success',
                    'filename': file.filename,
                    'size': len(file.read()),
                    'content_type': file.content_type
                })
            else:
                return jsonify({'status': 'error', 'message': 'No file received'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    return '''
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="video" accept="video/*">
        <button type="submit">Test Upload</button>
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_video():
    """Handle video upload and start processing"""
    try:
        # Check if request has file part
        if 'video' not in request.files:
            flash('No file part', 'error')
            return redirect(url_for('index'))
        
        file = request.files['video']
        
        # Check if file is selected
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        # Validate file type
        if file and allowed_file(file.filename):
            # Generate unique filename
            file_id = str(uuid.uuid4())
            filename = secure_filename(file.filename)
            file_extension = filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{file_id}.{file_extension}"
            
            # Save file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            # Store in session
            session['file_id'] = file_id
            session['original_filename'] = filename
            session['upload_time'] = datetime.now().isoformat()
            
            logging.info(f"File uploaded: {filename}")
            
            # Redirect to processing
            return redirect(url_for('process_video', file_id=file_id))
        else:
            flash('Invalid file type', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        logging.error(f"Upload error: {str(e)}")
        flash(f'Upload failed: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/process/<file_id>')
def process_video(file_id):
    """Process video and show results"""
    try:
        # Validate file_id
        if 'file_id' not in session or session['file_id'] != file_id:
            flash('Invalid session or file ID', 'error')
            return redirect(url_for('index'))
        
        # Find input file
        input_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.startswith(file_id)]
        if not input_files:
            flash('Input file not found', 'error')
            return redirect(url_for('index'))
        
        input_filename = input_files[0]
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        
        # Generate output filename
        output_filename = f"processed_{file_id}.mp4"
        output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
        
        # Process video
        logging.info(f"Starting video processing for {input_filename}")
        results = processor.process_video(input_path, output_path, heatmap_gen)
        
        # Store results in session
        session['results'] = results
        session['output_filename'] = output_filename
        
        logging.info(f"Video processing completed: {results}")
        return render_template('results.html', 
                             results=results, 
                             file_id=file_id,
                             original_filename=session.get('original_filename', 'Unknown'),
                             output_filename=output_filename)
        
    except Exception as e:
        logging.error(f"Processing error: {str(e)}")
        flash(f'Processing failed: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<file_id>')
def download_video(file_id):
    """Download processed video"""
    try:
        # Validate session
        if 'file_id' not in session or session['file_id'] != file_id:
            flash('Invalid session or file ID', 'error')
            return redirect(url_for('index'))
        
        output_filename = session.get('output_filename')
        if not output_filename:
            flash('No processed video available', 'error')
            return redirect(url_for('index'))
        
        output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
        
        if not os.path.exists(output_path):
            flash('Processed video file not found', 'error')
            return redirect(url_for('index'))
        
        return send_file(output_path, as_attachment=True, 
                        download_name=f"crowd_detection_{session.get('original_filename', 'video.mp4')}")
        
    except Exception as e:
        logging.error(f"Download error: {str(e)}")
        flash(f'Download failed: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/progress/<file_id>')
def get_progress(file_id):
    """Get processing progress (for future real-time updates)"""
    # This endpoint can be used for real-time progress updates
    # For now, we'll return a simple status
    return jsonify({'status': 'processing', 'progress': 50})

@app.errorhandler(413)
def file_too_large(e):
    """Handle file too large error"""
    flash('File is too large. Maximum size is 100MB.', 'error')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    logging.error(f"Internal server error: {str(e)}")
    flash('An internal error occurred. Please try again.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
