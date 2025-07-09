import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.backends.backend_agg import FigureCanvasAgg
import logging

class HeatmapGenerator:
    """Generate heatmaps for crowd density visualization"""
    
    def __init__(self, grid_size=50, decay_factor=0.95):
        """
        Initialize heatmap generator
        
        Args:
            grid_size: Size of grid cells for heatmap
            decay_factor: Temporal decay factor for heatmap
        """
        self.grid_size = grid_size
        self.decay_factor = decay_factor
        self.heatmap_data = None
        self.frame_shape = None
        
    def initialize_heatmap(self, frame_shape):
        """
        Initialize heatmap data structure
        
        Args:
            frame_shape: Shape of video frames (height, width, channels)
        """
        self.frame_shape = frame_shape
        height, width = frame_shape[:2]
        
        # Calculate grid dimensions
        self.grid_height = (height + self.grid_size - 1) // self.grid_size
        self.grid_width = (width + self.grid_size - 1) // self.grid_size
        
        # Initialize heatmap data
        self.heatmap_data = np.zeros((self.grid_height, self.grid_width), dtype=np.float32)
        
        logging.info(f"Heatmap initialized: {self.grid_height}x{self.grid_width} grid")
    
    def update_heatmap(self, person_centers):
        """
        Update heatmap with new person detections
        
        Args:
            person_centers: List of person center points [(x, y), ...]
        """
        if self.heatmap_data is None:
            logging.warning("Heatmap not initialized")
            return
        
        # Apply temporal decay
        self.heatmap_data *= self.decay_factor
        
        # Add new detections
        for center_x, center_y in person_centers:
            # Convert to grid coordinates
            grid_x = min(center_x // self.grid_size, self.grid_width - 1)
            grid_y = min(center_y // self.grid_size, self.grid_height - 1)
            
            # Increment heatmap value
            self.heatmap_data[grid_y, grid_x] += 1.0
            
            # Apply Gaussian blur for smooth transitions
            self._apply_gaussian_around_point(grid_y, grid_x)
    
    def _apply_gaussian_around_point(self, grid_y, grid_x, radius=2):
        """
        Apply Gaussian blur around a specific grid point
        
        Args:
            grid_y: Y coordinate in grid
            grid_x: X coordinate in grid
            radius: Radius of Gaussian effect
        """
        # Define Gaussian kernel
        kernel_size = 2 * radius + 1
        kernel = np.zeros((kernel_size, kernel_size))
        
        center = radius
        sigma = radius / 3.0
        
        for i in range(kernel_size):
            for j in range(kernel_size):
                x, y = i - center, j - center
                kernel[i, j] = np.exp(-(x*x + y*y) / (2 * sigma * sigma))
        
        # Normalize kernel
        kernel = kernel / np.sum(kernel) * 0.5
        
        # Apply kernel to heatmap
        for i in range(kernel_size):
            for j in range(kernel_size):
                target_y = grid_y + i - center
                target_x = grid_x + j - center
                
                if (0 <= target_y < self.grid_height and 
                    0 <= target_x < self.grid_width):
                    self.heatmap_data[target_y, target_x] += kernel[i, j]
    
    def generate_heatmap_overlay(self, frame, alpha=0.4):
        """
        Generate heatmap overlay on frame
        
        Args:
            frame: Input frame
            alpha: Transparency of heatmap overlay
            
        Returns:
            Frame with heatmap overlay
        """
        if self.heatmap_data is None:
            return frame
        
        try:
            # Resize heatmap to match frame dimensions
            frame_height, frame_width = frame.shape[:2]
            heatmap_resized = cv2.resize(self.heatmap_data, (frame_width, frame_height))
            
            # Normalize heatmap values
            if np.max(heatmap_resized) > 0:
                heatmap_normalized = heatmap_resized / np.max(heatmap_resized)
            else:
                heatmap_normalized = heatmap_resized
            
            # Create colormap
            colormap = plt.get_cmap('hot')
            heatmap_colored = colormap(heatmap_normalized)
            
            # Convert to BGR format
            heatmap_bgr = (heatmap_colored[:, :, :3] * 255).astype(np.uint8)
            heatmap_bgr = cv2.cvtColor(heatmap_bgr, cv2.COLOR_RGB2BGR)
            
            # Create overlay
            overlay = cv2.addWeighted(frame, 1 - alpha, heatmap_bgr, alpha, 0)
            
            return overlay
            
        except Exception as e:
            logging.error(f"Heatmap overlay error: {str(e)}")
            return frame
    
    def get_density_stats(self):
        """
        Get density statistics from current heatmap
        
        Returns:
            Dictionary with density statistics
        """
        if self.heatmap_data is None:
            return {'max_density': 0, 'avg_density': 0, 'total_activity': 0}
        
        max_density = np.max(self.heatmap_data)
        avg_density = np.mean(self.heatmap_data)
        total_activity = np.sum(self.heatmap_data)
        
        return {
            'max_density': float(max_density),
            'avg_density': float(avg_density),
            'total_activity': float(total_activity)
        }
    
    def save_heatmap_image(self, output_path):
        """
        Save current heatmap as image
        
        Args:
            output_path: Path to save heatmap image
        """
        if self.heatmap_data is None:
            logging.warning("No heatmap data to save")
            return
        
        try:
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Create heatmap plot
            im = ax.imshow(self.heatmap_data, cmap='hot', interpolation='bilinear')
            
            # Add colorbar
            plt.colorbar(im, ax=ax, label='Density')
            
            # Set title and labels
            ax.set_title('Crowd Density Heatmap')
            ax.set_xlabel('Grid X')
            ax.set_ylabel('Grid Y')
            
            # Save figure
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            logging.info(f"Heatmap saved to: {output_path}")
            
        except Exception as e:
            logging.error(f"Error saving heatmap: {str(e)}")
    
    def reset_heatmap(self):
        """Reset heatmap data"""
        if self.heatmap_data is not None:
            self.heatmap_data.fill(0)
