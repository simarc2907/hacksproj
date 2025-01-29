// Initialize Lucide icons
lucide.createIcons();

// DOM Elements
const authContainer = document.getElementById('authContainer');
const appContainer = document.getElementById('appContainer');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const authTabs = document.querySelectorAll('.auth-tab');
const roleSelect = document.getElementById('roleSelect');
const workerSkills = document.getElementById('workerSkills');
const navLinks = document.querySelectorAll('.nav-link');
const featureLinks = document.querySelectorAll('.feature-link');
const logoutBtn = document.getElementById('logoutBtn');
const pages = document.querySelectorAll('.page');

// Auth Tab Switching
authTabs.forEach(tab => {
  tab.addEventListener('click', () => {
    const formType = tab.dataset.form;
    authTabs.forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    
    if (formType === 'login') {
      loginForm.classList.remove('hidden');
      registerForm.classList.add('hidden');
    } else {
      loginForm.classList.add('hidden');
      registerForm.classList.remove('hidden');
    }
  });
});

// Show/Hide Worker Skills based on role
roleSelect.addEventListener('change', (e) => {
  if (e.target.value === 'worker') {
    workerSkills.classList.remove('hidden');
  } else {
    workerSkills.classList.add('hidden');
  }
});

// Form Submissions
loginForm.addEventListener('submit', (e) => {
  e.preventDefault();
  // Mock successful login
  authContainer.classList.add('hidden');
  appContainer.classList.remove('hidden');
});

registerForm.addEventListener('submit', (e) => {
  e.preventDefault();
  // Mock successful registration
  authContainer.classList.add('hidden');
  appContainer.classList.remove('hidden');
});

// Navigation
function navigateToPage(pageId) {
  // Update active states
  navLinks.forEach(l => l.classList.remove('active'));
  document.querySelector(`[data-page="${pageId}"]`)?.classList.add('active');
  
  pages.forEach(page => {
    page.classList.remove('active');
    if (page.id === `${pageId}Page`) {
      page.classList.add('active');
    }
  });
}

navLinks.forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    navigateToPage(link.dataset.page);
  });
});

featureLinks.forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    navigateToPage(link.dataset.page);
  });
});

// Logout
logoutBtn.addEventListener('click', () => {
  appContainer.classList.add('hidden');
  authContainer.classList.remove('hidden');
  // Reset forms
  loginForm.reset();
  registerForm.reset();
  // Reset active tab to login
  authTabs[0].click();
});

// Initialize icons for dynamic content
document.addEventListener('DOMContentLoaded', () => {
  lucide.createIcons();
});