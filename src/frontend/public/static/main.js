// Import modules
import { setupSidebar } from './sidebar.js';
import { setupPages } from './pages.js';
import { initializeServersPage, cleanupServersPage } from './servers.js';

// Initialize the application when DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
  // Initialize sidebar functionality
  setupSidebar();
  
  // Initialize page switching functionality with cleanup handlers
  setupPages({
    onPageChange: (oldPage, newPage) => {
      // Cleanup handlers
      if (oldPage === 'servers') {
        cleanupServersPage();
      }
      
      // Initialization handlers
      if (newPage === 'servers') {
        initializeServersPage();
      }
    }
  });
  
  console.log('Admin panel initialized');
});