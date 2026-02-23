document.addEventListener('DOMContentLoaded', () => {
    
    const themeToggler = document.getElementById('themeToggler');
    const moonIcon = document.getElementById('moonIcon');
    const sunIcon = document.getElementById('sunIcon');
    const htmlElement = document.documentElement;

    // Load saved theme or default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    htmlElement.setAttribute('data-bs-theme', savedTheme);
    updateIcon(savedTheme);

    if (themeToggler) {
        themeToggler.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            htmlElement.setAttribute('data-bs-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateIcon(newTheme);
        });
    }

    function updateIcon(theme) {
        if (!moonIcon || !sunIcon) return;
        if (theme === 'dark') {
            moonIcon.classList.add('d-none');
            sunIcon.classList.remove('d-none');
            sunIcon.classList.add('text-warning'); // yellow sun
        } else {
            sunIcon.classList.add('d-none');
            moonIcon.classList.remove('d-none');
            moonIcon.classList.add('text-dark');
        }
    }
});
