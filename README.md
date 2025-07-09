# Crowd Density Detection System

A Flask-based web application that uses YOLOv5 and OpenCV to detect and analyze crowd density in video files. The system provides real-time people counting, heatmap visualization, and comprehensive analytics.

## Features

### 🔹 Backend Capabilities
- **YOLOv5 Person Detection**: Uses state-of-the-art YOLO model for accurate person detection
- **Video Processing**: Frame-by-frame analysis with OpenCV
- **Heatmap Generation**: Visual representation of crowd density patterns
- **Real-time Analytics**: People counting, peak detection, and statistical analysis
- **Multi-format Support**: Handles MP4, AVI, MOV, MKV, FLV, and WMV files

### 🔹 Frontend Features
- **Responsive Web Interface**: Clean, Bootstrap-based design
- **Drag & Drop Upload**: Intuitive file upload with validation
- **Real-time Progress**: Processing status and progress tracking
- **Comprehensive Results**: Detailed analytics and visualizations
- **Download Functionality**: Get processed videos with overlays

### 🔹 Technical Highlights
- **Cloud-Ready**: Optimized for deployment on Render, Railway, or Heroku
- **Lightweight**: No heavy GPU dependencies for easy deployment
- **Scalable Architecture**: Modular design with separate utilities
- **Error Handling**: Comprehensive error handling and user feedback
- **Security**: File validation and secure upload handling

## Project Structure

```
crowd-density-detection/
├── static/
│   ├── css/
│   │   └── style.css           # Custom styling
│   ├── js/
│   │   └── upload.js           # Frontend interactions
│   ├── uploads/                # Uploaded video files
│   └── processed/              # Processed video outputs
├── templates/
│   ├── index.html              # Main upload page
│   └── results.html            # Results page
├── utils/
│   ├── detection.py            # YOLOv5 detection logic
│   ├── heatmap.py              # Heatmap generation
│   └── video_processor.py      # Video processing pipeline
├── app.py                      # Flask application
├── main.py                     # Entry point
├── Procfile                    # Heroku/Railway deployment
└── README.md                   # This file
```

## Installation & Setup

### Prerequisites
- Python 3.11+
- pip package manager

### Local Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/crowd-density-detection.git
cd crowd-density-detection
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export SESSION_SECRET="your-secret-key-here"
```

4. Run the application:
```bash
python main.py
```

5. Open browser to `http://localhost:5000`

### Cloud Deployment

#### Render Deployment
1. Push code to GitHub
2. Connect Render to your repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn --bind 0.0.0.0:$PORT main:app`
5. Add environment variable: `SESSION_SECRET`

#### Railway Deployment
1. Push code to GitHub
2. Import project in Railway
3. Railway will auto-detect Python and use the Procfile
4. Add environment variable: `SESSION_SECRET`

## Usage

1. **Upload Video**: Navigate to the home page and upload a video file
2. **Processing**: The system will analyze the video frame by frame
3. **Results**: View comprehensive analytics including:
   - Total people detected
   - Peak crowd count and timing
   - Average people per frame
   - Density heatmap visualization
4. **Download**: Get the processed video with bounding boxes and overlays

## Supported Video Formats
- MP4 (recommended)
- AVI
- MOV
- MKV
- FLV
- WMV

Maximum file size: 100MB

## Technical Details

### AI Model
- **YOLOv5**: Loaded from PyTorch Hub for person detection
- **Confidence Threshold**: 0.5 (configurable)
- **CPU Optimized**: Works without GPU requirements

### Video Processing
- **OpenCV**: Frame-by-frame processing
- **Real-time Analysis**: People counting and tracking
- **Heatmap Generation**: Grid-based density visualization

### Web Framework
- **Flask**: Python web framework
- **Bootstrap**: Responsive UI components
- **Gunicorn**: WSGI server for production

## Configuration

Key settings in `app.py`:
- `MAX_CONTENT_LENGTH`: File size limit (100MB)
- `ALLOWED_EXTENSIONS`: Supported video formats
- `UPLOAD_FOLDER`: Upload directory
- `PROCESSED_FOLDER`: Output directory

## Development

### Adding New Features
1. Detection logic: Modify `utils/detection.py`
2. Video processing: Update `utils/video_processor.py`
3. Heatmap generation: Edit `utils/heatmap.py`
4. Frontend: Update templates and static files

### API Endpoints
- `GET /`: Main upload page
- `POST /upload`: Handle video upload
- `GET /process/<file_id>`: Process video and show results
- `GET /download/<file_id>`: Download processed video

## Troubleshooting

### Common Issues
1. **Model Loading**: First run downloads YOLOv5 model (may take time)
2. **Memory**: Large videos may require more RAM
3. **Processing Time**: Depends on video length and resolution

### Performance Tips
- Use MP4 format for best compatibility
- Keep videos under 10 minutes for faster processing
- Lower resolution videos process faster

## License
MIT License - feel free to use and modify

## Contributing
1. Fork the repository
2. Create feature branch
3. Submit pull request

## Support
For issues and questions, please open a GitHub issue or contact the maintainers.

