// Upload functionality and UI interactions for Crowd Density Detection System

// Global utility functions
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'check-circle'}"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert alert at the top of the container
    const container = document.querySelector('.container');
    const firstChild = container.firstElementChild;
    container.insertBefore(alertDiv, firstChild.nextSibling);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const uploadBtn = document.getElementById('uploadBtn');
    const uploadProgress = document.getElementById('uploadProgress');
    const progressBar = document.getElementById('progressBar');
    const videoFile = document.getElementById('videoFile');
    
    // File size limit (50MB)
    const MAX_FILE_SIZE = 50 * 1024 * 1024;
    
    // Supported video formats
    const SUPPORTED_FORMATS = [
        'video/mp4',
        'video/avi',
        'video/quicktime',
        'video/x-msvideo',
        'video/x-ms-wmv',
        'video/x-flv',
        'video/x-matroska'
    ];
    
    // Initialize drag and drop functionality
    initializeDragDrop();
    
    // Form validation and submission
    uploadForm.addEventListener('submit', function(e) {
        // Allow form to submit normally for demo mode
        startUpload();
    });
    
    // File input change handler
    videoFile.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            validateFile(file);
            updateFileInfo(file);
        }
    });
    
    function validateFile(file) {
        // Check file size
        if (file.size > MAX_FILE_SIZE) {
            showAlert('File size exceeds 50MB limit. Please choose a smaller file.', 'error');
            return false;
        }
        
        // Check file type
        if (!SUPPORTED_FORMATS.includes(file.type)) {
            showAlert('Unsupported file format. Please use MP4, AVI, MOV, MKV, FLV, or WMV.', 'error');
            return false;
        }
        
        return true;
    }
    
    function updateFileInfo(file) {
        const fileSize = formatFileSize(file.size);
        const fileName = file.name;
        
        // Update UI with file information
        const fileInfo = document.createElement('div');
        fileInfo.className = 'alert alert-info mt-3';
        fileInfo.innerHTML = `
            <i class="fas fa-file-video"></i>
            <strong>Selected:</strong> ${fileName} (${fileSize})
        `;
        
        // Remove existing file info
        const existingInfo = document.querySelector('.file-info');
        if (existingInfo) {
            existingInfo.remove();
        }
        
        fileInfo.className += ' file-info';
        videoFile.parentNode.appendChild(fileInfo);
    }
    
    function startUpload() {
        // Disable form and show progress
        uploadBtn.disabled = true;
        uploadBtn.innerHTML = '<span class="loading-spinner"></span> Starting Demo...';
        uploadProgress.style.display = 'block';
        
        // Simulate progress
        simulateProgress();
    }
    
    function simulateProgress() {
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 10;
            if (progress > 90) {
                progress = 90;
            }
            
            progressBar.style.width = progress + '%';
            
            if (progress >= 90) {
                clearInterval(interval);
                progressBar.className += ' progress-bar-striped progress-bar-animated';
            }
        }, 200);
    }
    
    function initializeDragDrop() {
        const dropZone = document.querySelector('.card-body');
        
        if (!dropZone) return;
        
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });
        
        // Highlight drop zone when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });
        
        // Handle dropped files
        dropZone.addEventListener('drop', handleDrop, false);
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        function highlight(e) {
            dropZone.classList.add('dragover');
        }
        
        function unhighlight(e) {
            dropZone.classList.remove('dragover');
        }
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length > 0) {
                const file = files[0];
                
                // Update file input
                const fileInput = document.getElementById('videoFile');
                fileInput.files = files;
                
                // Validate and update UI
                if (validateFile(file)) {
                    updateFileInfo(file);
                }
            }
        }
    }
    
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // showAlert function moved to global scope above
    
    // Real-time file validation
    videoFile.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            // Show file preview/info
            const preview = document.createElement('div');
            preview.className = 'mt-3 p-3 bg-light rounded';
            preview.innerHTML = `
                <h6>File Selected:</h6>
                <p class="mb-1"><strong>Name:</strong> ${file.name}</p>
                <p class="mb-1"><strong>Size:</strong> ${formatFileSize(file.size)}</p>
                <p class="mb-0"><strong>Type:</strong> ${file.type}</p>
            `;
            
            // Remove existing preview
            const existingPreview = document.querySelector('.file-preview');
            if (existingPreview) {
                existingPreview.remove();
            }
            
            preview.className += ' file-preview';
            this.parentNode.appendChild(preview);
        }
    });
    
    // Progress tracking for results page
    if (window.location.pathname.includes('/process/')) {
        // Show processing status
        const processingStatus = document.createElement('div');
        processingStatus.className = 'alert alert-info text-center';
        processingStatus.innerHTML = `
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2 mb-0">Processing video... This may take a few minutes.</p>
        `;
        
        // Add to page if we're on processing page
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(processingStatus, container.firstElementChild);
        }
    }
    
    // Auto-refresh for processing status (if needed)
    function checkProcessingStatus() {
        // This function can be enhanced to check processing status via AJAX
        // For now, it's a placeholder for future real-time updates
        console.log('Checking processing status...');
    }
    
    // Initialize tooltips (if Bootstrap tooltips are used)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Utility functions for enhanced user experience
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showToast('Copied to clipboard!', 'success');
    }).catch(function() {
        showToast('Failed to copy to clipboard', 'error');
    });
}

function showToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : 'success'} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    // Add to page
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    toastContainer.appendChild(toast);
    
    // Show toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove after hiding
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
}

// Export functions for use in other scripts
window.CrowdDetectionUI = {
    showAlert: showAlert,
    showToast: showToast,
    copyToClipboard: copyToClipboard
};
