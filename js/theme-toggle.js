// Theme toggle functionality
(function() {
  const themeToggle = document.getElementById('theme-toggle');
  const themeIcon = document.querySelector('.theme-icon');
  const htmlElement = document.documentElement;

  // Check for saved theme preference or default to system preference
  function getPreferredTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      return savedTheme;
    }
    
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  // Set theme
  function setTheme(theme) {
    htmlElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    updateIcon(theme);
  }

  // Update icon based on theme
  function updateIcon(theme) {
    themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
  }

  // Toggle theme
  function toggleTheme() {
    const currentTheme = htmlElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
  }

  // Initialize theme
  const initialTheme = getPreferredTheme();
  setTheme(initialTheme);

  // Add event listener
  if (themeToggle) {
    themeToggle.addEventListener('click', toggleTheme);
  }

  // Listen for system theme changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
      setTheme(e.matches ? 'dark' : 'light');
    }
  });
})();
