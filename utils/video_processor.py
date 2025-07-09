import cv2
import numpy as np
import logging
import os
from datetime import datetime

class VideoProcessor:
    """Process videos for crowd density detection"""
    
    def __init__(self, detector):
        """
        Initialize video processor
        
        Args:
            detector: YOLODetector instance
        """
        self.detector = detector
        self.frame_stats = []
        
    def process_video(self, input_path, output_path, heatmap_generator):
        """
        Process video file for crowd density detection
        
        Args:
            input_path: Path to input video
            output_path: Path to save processed video
            heatmap_generator: HeatmapGenerator instance
            
        Returns:
            Dictionary with processing results
        """
        try:
            # Open input video
            cap = cv2.VideoCapture(input_path)
            if not cap.isOpened():
                raise ValueError(f"Cannot open video file: {input_path}")
            
            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            logging.info(f"Processing video: {width}x{height} @ {fps}fps, {total_frames} frames")
            
            # Initialize video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            # Initialize heatmap
            heatmap_generator.initialize_heatmap((height, width, 3))
            
            # Processing variables
            frame_count = 0
            total_people_detected = 0
            max_people_frame = 0
            max_people_count = 0
            self.frame_stats = []
            
            # Process frames
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Detect people in frame
                detections = self.detector.detect_people(frame)
                people_count = len(detections)
                total_people_detected += people_count
                
                # Update statistics
                if people_count > max_people_count:
                    max_people_count = people_count
                    max_people_frame = frame_count
                
                # Get person centers for heatmap
                person_centers = self.detector.get_person_centers(detections)
                
                # Update heatmap
                heatmap_generator.update_heatmap(person_centers)
                
                # Draw detections on frame
                frame_with_detections = self.detector.draw_detections(frame, detections)
                
                # Add heatmap overlay
                frame_with_heatmap = heatmap_generator.generate_heatmap_overlay(
                    frame_with_detections, alpha=0.3
                )
                
                # Add frame information
                self._add_frame_info(frame_with_heatmap, frame_count, people_count, 
                                   total_people_detected, max_people_count)
                
                # Write frame
                out.write(frame_with_heatmap)
                
                # Store frame statistics
                self.frame_stats.append({
                    'frame': frame_count,
                    'people_count': people_count,
                    'timestamp': frame_count / fps
                })
                
                # Log progress
                if frame_count % 30 == 0:
                    progress = (frame_count / total_frames) * 100
                    logging.info(f"Processing progress: {progress:.1f}% ({frame_count}/{total_frames})")
            
            # Cleanup
            cap.release()
            out.release()
            
            # Calculate final statistics
            avg_people_per_frame = total_people_detected / frame_count if frame_count > 0 else 0
            density_stats = heatmap_generator.get_density_stats()
            
            # Create results dictionary
            results = {
                'total_frames': frame_count,
                'total_people_detected': total_people_detected,
                'avg_people_per_frame': round(avg_people_per_frame, 2),
                'max_people_count': max_people_count,
                'max_people_frame': max_people_frame,
                'max_people_timestamp': round(max_people_frame / fps, 2),
                'video_duration': round(frame_count / fps, 2),
                'fps': fps,
                'resolution': f"{width}x{height}",
                'density_stats': density_stats,
                'processing_time': datetime.now().isoformat()
            }
            
            logging.info(f"Video processing completed: {results}")
            return results
            
        except Exception as e:
            logging.error(f"Video processing error: {str(e)}")
            raise RuntimeError(f"Video processing failed: {str(e)}")
    
    def _add_frame_info(self, frame, frame_number, people_count, total_people, max_people):
        """
        Add information overlay to frame
        
        Args:
            frame: Frame to add information to
            frame_number: Current frame number
            people_count: People count in current frame
            total_people: Total people detected so far
            max_people: Maximum people in any frame so far
        """
        # Prepare text information
        info_lines = [
            f"Frame: {frame_number}",
            f"People: {people_count}",
            f"Total: {total_people}",
            f"Max: {max_people}"
        ]
        
        # Text settings
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        font_thickness = 2
        line_height = 25
        
        # Background rectangle
        bg_height = len(info_lines) * line_height + 10
        bg_width = 150
        
        # Draw background
        cv2.rectangle(frame, (10, 10), (10 + bg_width, 10 + bg_height), 
                     (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (10 + bg_width, 10 + bg_height), 
                     (255, 255, 255), 2)
        
        # Draw text
        for i, line in enumerate(info_lines):
            y_position = 35 + i * line_height
            cv2.putText(frame, line, (15, y_position), font, font_scale, 
                       (255, 255, 255), font_thickness)
    
    def get_frame_statistics(self):
        """
        Get detailed frame statistics
        
        Returns:
            List of frame statistics
        """
        return self.frame_stats
    
    def export_statistics(self, output_path):
        """
        Export frame statistics to JSON file
        
        Args:
            output_path: Path to save statistics JSON
        """
        try:
            import json
            
            stats_data = {
                'frame_statistics': self.frame_stats,
                'export_time': datetime.now().isoformat()
            }
            
            with open(output_path, 'w') as f:
                json.dump(stats_data, f, indent=2)
            
            logging.info(f"Statistics exported to: {output_path}")
            
        except Exception as e:
            logging.error(f"Error exporting statistics: {str(e)}")
