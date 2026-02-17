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

        fetch('/api/set-theme', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ theme: newTheme })
        });
    });
}

function initFileUpload() {
    const fileInput = document.getElementById('file');
    if (!fileInput) return;

    const fileWrapper = document.querySelector('.file-input-wrapper');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const fileError = document.getElementById('fileError');
    const allowedExts = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'zip'];

    fileWrapper.addEventListener('click', () => fileInput.click());
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

const form = document.getElementById('contactForm');
const nameInput = document.getElementById('name');
const contactInput = document.getElementById('contact');
const messageInput = document.getElementById('message');
const submitBtn = form ? form.querySelector('button[type="submit"]') : null;
const charCount = document.getElementById('charCount');

if (messageInput) {
    messageInput.addEventListener('input', () => {
        charCount.textContent = messageInput.value.length;
        if (messageInput.value.length > 500) {
            messageInput.value = messageInput.value.substring(0, 500);
            charCount.textContent = 500;
        }
    });
}

function validateName() {
    if (!nameInput) return true;
    const nameError = document.getElementById('nameError');
    const value = nameInput.value.trim();

    if (value.length < 2) {
        nameError.textContent = 'Name must be at least 2 characters';
        return false;
    }

    nameError.textContent = '';
    return true;
}

function validateContact() {
    if (!contactInput) return true;
    const contactError = document.getElementById('emailError');
    const value = contactInput.value.trim();

    if (value.length < 3) {
        contactError.textContent = 'Please enter where we should reach out';
        return false;
    }

    contactError.textContent = '';
    return true;
}

function validateMessage() {
    if (!messageInput) return true;
    const messageError = document.getElementById('messageError');
    const value = messageInput.value.trim();

    if (value.length < 10) {
        messageError.textContent = 'Message must be at least 10 characters';
        return false;
    }

    if (value.length > 500) {
        messageError.textContent = 'Message cannot exceed 500 characters';
        return false;
    }

    messageError.textContent = '';
    return true;
}

if (nameInput) {
    nameInput.addEventListener('blur', validateName);
}

if (contactInput) {
    contactInput.addEventListener('blur', validateContact);
}

if (messageInput) {
    messageInput.addEventListener('blur', validateMessage);
}

function validateForm(event) {
    if (!form) return false;
    event.preventDefault();

    const isNameValid = validateName();
    const isContactValid = validateContact();
    const isMessageValid = validateMessage();

    if (!isNameValid || !isContactValid || !isMessageValid) {
        return false;
    }

    if (submitBtn) {
        submitBtn.classList.add('loading');
        submitBtn.querySelector('span').textContent = 'Sending...';
        submitBtn.disabled = true;
    }

    setTimeout(() => {
        form.submit();
    }, 250);

    return false;
}

window.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initFileUpload();
});
