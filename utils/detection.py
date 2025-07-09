import cv2
import numpy as np
import logging
import os

class YOLODetector:
    """OpenCV-based person detection class"""
    
    def __init__(self, model_name='hog', confidence_threshold=0.5):
        """
        Initialize OpenCV detector
        
        Args:
            model_name: Detection method ('hog' or 'cascade')
            confidence_threshold: Minimum confidence for detections
        """
        self.confidence_threshold = confidence_threshold
        self.model_name = model_name
        
        try:
            if model_name == 'hog':
                # Initialize HOG people detector
                self.hog = cv2.HOGDescriptor()
                self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
                logging.info("HOG people detector initialized successfully")
            else:
                # Initialize cascade classifier as fallback
                self.cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
                if self.cascade.empty():
                    raise RuntimeError("Failed to load cascade classifier")
                logging.info("Cascade classifier initialized successfully")
                
        except Exception as e:
            logging.error(f"Error initializing detector: {str(e)}")
            raise RuntimeError(f"Failed to initialize detector: {str(e)}")
    
    def detect_people(self, frame):
        """
        Detect people in a frame
        
        Args:
            frame: Input frame (numpy array)
            
        Returns:
            List of detection results with bounding boxes and confidence scores
        """
        try:
            detections = []
            
            if self.model_name == 'hog':
                # Use HOG detector
                rects, weights = self.hog.detectMultiScale(
                    frame,
                    winStride=(8, 8),
                    padding=(32, 32),
                    scale=1.05,
                    hitThreshold=0.0
                )
                
                for i, (x, y, w, h) in enumerate(rects):
                    # Calculate confidence from weight
                    confidence = min(abs(weights[i][0]) / 2.0, 1.0)
                    
                    if confidence >= self.confidence_threshold:
                        detections.append({
                            'bbox': [int(x), int(y), int(x + w), int(y + h)],
                            'confidence': float(confidence),
                            'class_id': 0,
                            'class_name': 'person'
                        })
            else:
                # Use cascade classifier
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                rects = self.cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30)
                )
                
                for (x, y, w, h) in rects:
                    detections.append({
                        'bbox': [int(x), int(y), int(x + w), int(y + h)],
                        'confidence': 0.8,  # Fixed confidence for cascade
                        'class_id': 0,
                        'class_name': 'person'
                    })
            
            return detections
            
        except Exception as e:
            logging.error(f"Detection error: {str(e)}")
            return []
    
    def draw_detections(self, frame, detections):
        """
        Draw bounding boxes and labels on frame
        
        Args:
            frame: Input frame
            detections: List of detection results
            
        Returns:
            Frame with drawn detections
        """
        if not detections:
            return frame
        
        # Create a copy to avoid modifying original
        result_frame = frame.copy()
        
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            confidence = detection['confidence']
            
            # Draw bounding box
            cv2.rectangle(result_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw label
            label = f"Person: {confidence:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            
            # Background rectangle for label
            cv2.rectangle(result_frame, (x1, y1 - label_size[1] - 10), 
                         (x1 + label_size[0], y1), (0, 255, 0), -1)
            
            # Label text
            cv2.putText(result_frame, label, (x1, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        return result_frame
    
    def get_person_centers(self, detections):
        """
        Get center points of detected persons
        
        Args:
            detections: List of detection results
            
        Returns:
            List of center points [(x, y), ...]
        """
        centers = []
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            centers.append((center_x, center_y))
        
        return centers
