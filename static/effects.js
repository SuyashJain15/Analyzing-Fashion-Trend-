// Fashion Trend Analyzer - Clean Interactive Effects

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all premium effects
    initLoadingOverlay();
    initProgressBarAnimation();
    initFileUpload();
    initComparisonForm();
    initFloatingParticles();
});

// Loading overlay for form submission
function initLoadingOverlay() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            showLoadingOverlay();
        });
    });
}

function showLoadingOverlay() {
    let overlay = document.querySelector('.loading-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.innerHTML = '<div class="loader"></div>';
        document.body.appendChild(overlay);
    }
    setTimeout(() => overlay.classList.add('active'), 10);
}

function hideLoadingOverlay() {
    const overlay = document.querySelector('.loading-overlay');
    if (overlay) {
        overlay.classList.remove('active');
        setTimeout(() => overlay.remove(), 300);
    }
}

// Animate progress bars when they come into view (subtle)
function initProgressBarAnimation() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {
                    bar.style.transition = 'width 0.8s ease-out';
                    bar.style.width = width;
                }, 50);
                observer.unobserve(bar);
            }
        });
    }, { threshold: 0.1 });

    progressBars.forEach(bar => observer.observe(bar));
}

// File Upload Functionality
function initFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const fileUploadArea = document.getElementById('fileUploadArea');
    const filePreview = document.getElementById('filePreview');
    const uploadContent = document.querySelector('.file-upload-content');
    const analyzeBtn = document.getElementById('analyzeBtn');
    
    if (!fileInput || !fileUploadArea) return;
    
    // Click to upload
    fileUploadArea.addEventListener('click', function(e) {
        if (!filePreview.style.display || filePreview.style.display === 'none') {
            fileInput.click();
        }
    });
    
    // File input change
    fileInput.addEventListener('change', function(e) {
        handleFileSelect(e.target.files[0]);
    });
    
    // Drag and drop
    fileUploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        fileUploadArea.classList.add('dragover');
    });
    
    fileUploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        fileUploadArea.classList.remove('dragover');
    });
    
    fileUploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        fileUploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });
    
    function handleFileSelect(file) {
        if (!file) return;
        
        // Check if image
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file (JPG, PNG, JPEG)');
            return;
        }
        
        // Check file size (10MB limit)
        if (file.size > 10 * 1024 * 1024) {
            alert('File size must be less than 10MB');
            return;
        }
        
        // Show preview
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('previewImage').src = e.target.result;
            document.getElementById('fileName').textContent = file.name;
            document.getElementById('fileSize').textContent = formatFileSize(file.size);
            
            uploadContent.style.display = 'none';
            filePreview.style.display = 'flex';
            analyzeBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }
}

function removeFile() {
    const fileInput = document.getElementById('fileInput');
    const filePreview = document.getElementById('filePreview');
    const uploadContent = document.querySelector('.file-upload-content');
    const analyzeBtn = document.getElementById('analyzeBtn');
    
    fileInput.value = '';
    filePreview.style.display = 'none';
    uploadContent.style.display = 'block';
    analyzeBtn.disabled = true;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Comparison form handlers
function initComparisonForm() {
    const fileInput1 = document.getElementById('fileInput1');
    const fileInput2 = document.getElementById('fileInput2');
    const fileUploadArea1 = document.getElementById('fileUploadArea1');
    const fileUploadArea2 = document.getElementById('fileUploadArea2');
    const filePreview1 = document.getElementById('filePreview1');
    const filePreview2 = document.getElementById('filePreview2');
    const uploadContent1 = document.querySelector('#fileUploadArea1 .file-upload-content');
    const uploadContent2 = document.querySelector('#fileUploadArea2 .file-upload-content');
    const compareBtn = document.getElementById('compareBtn');
    
    if (!fileInput1 || !fileInput2) return;
    
    // Click to upload
    fileUploadArea1.addEventListener('click', function(e) {
        if (!filePreview1.style.display || filePreview1.style.display === 'none') {
            fileInput1.click();
        }
    });
    
    fileUploadArea2.addEventListener('click', function(e) {
        if (!filePreview2.style.display || filePreview2.style.display === 'none') {
            fileInput2.click();
        }
    });
    
    // File input changes
    fileInput1.addEventListener('change', function(e) {
        handleFileSelect(e.target.files[0], '1');
    });
    
    fileInput2.addEventListener('change', function(e) {
        handleFileSelect(e.target.files[0], '2');
    });
    
    function handleFileSelect(file, num) {
        if (!file) return;
        
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file');
            return;
        }
        
        if (file.size > 10 * 1024 * 1024) {
            alert('File size must be less than 10MB');
            return;
        }
        
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById(`previewImage${num}`).src = e.target.result;
            document.getElementById(`fileName${num}`).textContent = file.name;
            document.getElementById(`fileSize${num}`).textContent = formatFileSize(file.size);
            
            const uploadContent = document.querySelector(`#fileUploadArea${num} .file-upload-content`);
            const filePreview = document.getElementById(`filePreview${num}`);
            
            uploadContent.style.display = 'none';
            filePreview.style.display = 'flex';
            
            // Enable compare button if both files selected
            if (filePreview1.style.display === 'flex' && filePreview2.style.display === 'flex') {
                compareBtn.disabled = false;
            }
        };
        reader.readAsDataURL(file);
    }
}

function removeFile1() {
    const fileInput = document.getElementById('fileInput1');
    const filePreview = document.getElementById('filePreview1');
    const uploadContent = document.querySelector('#fileUploadArea1 .file-upload-content');
    const compareBtn = document.getElementById('compareBtn');
    
    fileInput.value = '';
    filePreview.style.display = 'none';
    uploadContent.style.display = 'block';
    compareBtn.disabled = true;
}

function removeFile2() {
    const fileInput = document.getElementById('fileInput2');
    const filePreview = document.getElementById('filePreview2');
    const uploadContent = document.querySelector('#fileUploadArea2 .file-upload-content');
    const compareBtn = document.getElementById('compareBtn');
    
    fileInput.value = '';
    filePreview.style.display = 'none';
    uploadContent.style.display = 'block';
    compareBtn.disabled = true;
}

// Premium Floating Particles Effect
function initFloatingParticles() {
    const canvas = document.createElement('canvas');
    canvas.id = 'particles-canvas';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '0';
    canvas.style.opacity = '0.4';
    document.body.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    let particles = [];
    const particleCount = 30;
    let animationId;

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Create floating particles
    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 4 + 2;
            this.speedX = Math.random() * 0.5 - 0.25;
            this.speedY = Math.random() * 0.5 - 0.25;
            this.opacity = Math.random() * 0.3 + 0.2;
            this.color = Math.random() > 0.5 ? 'rgba(255, 255, 255, ' + this.opacity + ')' : 
                        Math.random() > 0.5 ? 'rgba(99, 102, 241, ' + this.opacity + ')' : 
                        'rgba(236, 72, 153, ' + this.opacity + ')';
        }

        update() {
            this.x += this.speedX;
            this.y += this.speedY;

            if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
            if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;

            // Gentle floating motion
            this.x += Math.sin(Date.now() * 0.001 + this.y) * 0.1;
            this.y += Math.cos(Date.now() * 0.001 + this.x) * 0.1;
        }

        draw() {
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
            
            // Add glow effect
            ctx.shadowBlur = 10;
            ctx.shadowColor = this.color;
        }
    }

    // Initialize particles
    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }

    // Animation loop
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach(particle => {
            particle.update();
            particle.draw();
        });

        // Draw connections between nearby particles
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 150) {
                    ctx.strokeStyle = `rgba(255, 255, 255, ${0.1 * (1 - distance / 150)})`;
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }

        animationId = requestAnimationFrame(animate);
    }

    animate();
}
