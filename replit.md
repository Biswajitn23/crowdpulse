# Crowd Density Detection System

## Overview

This is a Flask-based web application that provides crowd density analysis using AI-powered person detection. The system processes uploaded video files to detect people, generate heatmaps, and provide comprehensive analytics about crowd patterns. It uses YOLOv8 for object detection and OpenCV for video processing.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework with Python
- **Detection Engine**: YOLOv8 (Ultralytics) for person detection
- **Video Processing**: OpenCV for frame-by-frame analysis
- **File Handling**: Werkzeug for secure file uploads
- **Session Management**: Flask sessions with configurable secret key

### Frontend Architecture
- **UI Framework**: Bootstrap with dark theme
- **JavaScript**: Vanilla JS for upload handling and drag-drop functionality
- **CSS**: Custom styling with responsive design
- **Icons**: Font Awesome for visual elements

### Key Components

1. **YOLODetector** (`utils/detection.py`): Handles person detection using YOLOv8 model
2. **VideoProcessor** (`utils/video_processor.py`): Processes video files frame by frame
3. **HeatmapGenerator** (`utils/heatmap.py`): Creates density heatmaps and visualizations
4. **Flask App** (`app.py`): Main web application with upload and result endpoints

## Data Flow

1. **Upload Phase**: User uploads video file through web interface
2. **Validation**: File type, size, and format validation
3. **Processing**: Video is processed frame by frame for person detection
4. **Analysis**: Statistical analysis and heatmap generation
5. **Output**: Processed video with overlays and analytics dashboard

## Key Features

- **Video Upload**: Supports MP4, AVI, MOV, MKV, FLV, WMV formats (max 100MB)
- **Real-time Processing**: Frame-by-frame analysis with progress tracking
- **Person Detection**: YOLOv8-based detection with configurable confidence threshold
- **Heatmap Generation**: Grid-based density visualization with temporal decay
- **Analytics Dashboard**: Comprehensive statistics and visualizations
- **Download Capability**: Processed videos with detection overlays

## External Dependencies

- **YOLOv8**: Ultralytics YOLO model for object detection
- **OpenCV**: Video processing and computer vision operations
- **PyTorch**: Deep learning framework for YOLO model
- **NumPy**: Numerical computing for array operations
- **Matplotlib**: Plotting and visualization for heatmaps
- **Bootstrap**: Frontend UI framework
- **Font Awesome**: Icon library

## Deployment Strategy

### Cloud-Ready Design
- **Platform Support**: Optimized for Render, Railway, or Heroku
- **Lightweight**: No heavy GPU dependencies for easy deployment
- **Environment Variables**: Configurable session secret and settings
- **Static File Handling**: Organized static assets (uploads, processed videos)

### Configuration
- **File Limits**: 100MB maximum file size
- **Storage**: Local file system for uploads and processed videos
- **Logging**: Comprehensive logging for debugging and monitoring
- **Security**: Secure filename handling and file validation

### Directory Structure
```
/static/uploads/     # Uploaded video files
/static/processed/   # Processed video outputs
/static/css/        # Custom stylesheets
/static/js/         # JavaScript files
/templates/         # HTML templates
/utils/            # Core processing utilities
```

## Technical Highlights

- **Modular Design**: Separate utilities for detection, processing, and visualization
- **Error Handling**: Comprehensive error handling throughout the pipeline
- **Progress Tracking**: Real-time processing status updates
- **Responsive UI**: Mobile-friendly interface with drag-drop upload
- **Statistical Analysis**: Detailed crowd metrics and peak detection