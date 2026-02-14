// Theme toggle
function initThemeToggle() {
    const themeBtn = document.getElementById('themeToggle');
    if (!themeBtn) return;

    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.style.colorScheme = savedTheme;
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
        themeBtn.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
        themeBtn.innerHTML = '<i class="fas fa-moon"></i>';
    }

    themeBtn.addEventListener('click', () => {
        const currentTheme = document.body.classList.contains('light-theme') ? 'light' : 'dark';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';

        document.body.classList.toggle('light-theme');
        document.documentElement.style.colorScheme = newTheme;
        localStorage.setItem('theme', newTheme);

        themeBtn.innerHTML = newTheme === 'light'
            ? '<i class="fas fa-sun"></i>'
            : '<i class="fas fa-moon"></i>';

        // Send to server
        fetch('/api/set-theme', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ theme: newTheme })
        });
    });
}

// File upload handler
function initFileUpload() {
    const fileInput = document.getElementById('file');
    if (!fileInput) return;

    const fileWrapper = document.querySelector('.file-input-wrapper');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const fileError = document.getElementById('fileError');
    const allowedExts = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'zip'];

    fileWrapper.addEventListener('click', () => fileInput.click());
    fileWrapper.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileWrapper.style.borderColor = '#38bdf8';
        fileWrapper.style.background = 'rgba(56, 189, 248, 0.1)';
    });
    fileWrapper.addEventListener('dragleave', () => {
        fileWrapper.style.borderColor = '';
        fileWrapper.style.background = '';
    });
    fileWrapper.addEventListener('drop', (e) => {
        e.preventDefault();
        fileWrapper.style.borderColor = '';
        fileWrapper.style.background = '';
        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            updateFileDisplay();
        }
    });

    fileInput.addEventListener('change', updateFileDisplay);

    function updateFileDisplay() {
        if (!fileInput.files.length) {
            fileName.textContent = 'No file chosen';
            fileSize.textContent = '';
            fileError.textContent = '';
            return;
        }

        const file = fileInput.files[0];
        const ext = file.name.split('.').pop().toLowerCase();

        if (!allowedExts.includes(ext)) {
            fileError.textContent = `File type .${ext} not allowed`;
            fileInput.value = '';
            fileName.textContent = 'No file chosen';
            return;
        }

        if (file.size > 16 * 1024 * 1024) {
            fileError.textContent = 'File size exceeds 16MB limit';
            fileInput.value = '';
            fileName.textContent = 'No file chosen';
            return;
        }

        fileError.textContent = '';
        fileName.textContent = file.name;
        fileSize.textContent = `(${(file.size / 1024).toFixed(2)} KB)`;
    }
}

// Form elements
const form = document.getElementById('contactForm');
const nameInput = document.getElementById('name');
const emailInput = document.getElementById('email');
const messageInput = document.getElementById('message');
const submitBtn = form ? form.querySelector('button[type="submit"]') : null;
const successMessage = document.getElementById('successMessage');
const charCount = document.getElementById('charCount');

// Real-time character counter
if (messageInput) {
    messageInput.addEventListener('input', () => {
        charCount.textContent = messageInput.value.length;
        if (messageInput.value.length > 500) {
            messageInput.value = messageInput.value.substring(0, 500);
            charCount.textContent = 500;
        }
    });
}

// Validate individual fields
function validateName() {
    if (!nameInput) return true;
    const nameError = document.getElementById('nameError');
    const value = nameInput.value.trim();

    if (value.length === 0) {
        nameError.textContent = 'Name is required';
        return false;
    } else if (value.length < 2) {
        nameError.textContent = 'Name must be at least 2 characters';
        return false;
    } else if (!/^[a-zA-Z\s'-]+$/.test(value)) {
        nameError.textContent = 'Name can only contain letters, spaces, hyphens, and apostrophes';
        return false;
    } else {
        nameError.textContent = '';
        return true;
    }
}

function validateEmail() {
    if (!emailInput) return true;
    const emailError = document.getElementById('emailError');
    const value = emailInput.value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (value.length === 0) {
        emailError.textContent = 'Email is required';
        return false;
    } else if (!emailRegex.test(value)) {
        emailError.textContent = 'Please enter a valid email address';
        return false;
    } else {
        emailError.textContent = '';
        return true;
    }
}

function validateMessage() {
    if (!messageInput) return true;
    const messageError = document.getElementById('messageError');
    const value = messageInput.value.trim();

    if (value.length === 0) {
        messageError.textContent = 'Message is required';
        return false;
    } else if (value.length < 10) {
        messageError.textContent = 'Message must be at least 10 characters';
        return false;
    } else if (value.length > 500) {
        messageError.textContent = 'Message cannot exceed 500 characters';
        return false;
    } else {
        messageError.textContent = '';
        return true;
    }
}

// Real-time validation on input
if (nameInput) {
    nameInput.addEventListener('blur', validateName);
    nameInput.addEventListener('input', () => {
        if (document.getElementById('nameError').textContent) {
            validateName();
        }
    });
}

if (emailInput) {
    emailInput.addEventListener('blur', validateEmail);
    emailInput.addEventListener('input', () => {
        if (document.getElementById('emailError').textContent) {
            validateEmail();
        }
    });
}

if (messageInput) {
    messageInput.addEventListener('blur', validateMessage);
    messageInput.addEventListener('input', () => {
        if (document.getElementById('messageError').textContent) {
            validateMessage();
        }
    });
}

// Main form validation and submission
function validateForm(event) {
    if (!form) return false;
    event.preventDefault();

    // Validate all fields
    const isNameValid = validateName();
    const isEmailValid = validateEmail();
    const isMessageValid = validateMessage();

    if (!isNameValid || !isEmailValid || !isMessageValid) {
        return false;
    }

    // Show loading state
    if (submitBtn) {
        submitBtn.classList.add('loading');
        submitBtn.querySelector('span').textContent = 'Sending...';
        submitBtn.disabled = true;
    }

    // Simulate sending (submit the form)
    setTimeout(() => {
        form.submit();
    }, 500);

    return false;
}

// Show success message and reset form
window.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initFileUpload();

    if (successMessage) {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('sent') === 'true') {
            successMessage.classList.add('show');
            if (form) {
                form.reset();
                charCount.textContent = '0';
            }

            setTimeout(() => {
                successMessage.classList.remove('show');
                // Don't replace URL to preserve message token link
            }, 4000);
        }
    }
});
