/**
 * Servers page functionality
 */

// Cache DOM elements
let serversTable = null;
let updateInterval = null;
let addServerModal = null;
let addServerForm = null;

// Fetch servers from the API
async function fetchServers() {
  try {
    const response = await fetch('/servers_api/list');
    
    // Check if response is JSON
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      throw new Error('Server returned an invalid response format. Please ensure the server is running and properly configured to return JSON.');
    }

    if (!response.ok) {
      throw new Error(`Server responded with status: ${response.status}`);
    }

    const servers = await response.json();
    updateServersTable(servers);
  } catch (error) {
    console.error('Error fetching servers:', error);
    
    // Show more user-friendly error in the table
    if (serversTable) {
      const tbody = serversTable.querySelector('tbody');
      tbody.innerHTML = `
        <tr>
          <td colspan="4" class="error-message">
            ${error.message.includes('fetch') ? 
              'Unable to connect to the server. Please ensure the server is running and accessible.' :
              error.message}
          </td>
        </tr>
      `;
    }
    
    // If we get a connection error, slow down the polling to reduce console spam
    if (updateInterval) {
      clearInterval(updateInterval);
      updateInterval = setInterval(fetchServers, 10000); // Increase to 10 seconds when errors occur
    }
  }
}

// Update the servers table with new data
function updateServersTable(servers) {
  if (!serversTable) return;
  
  const tbody = serversTable.querySelector('tbody');
  tbody.innerHTML = '';
  
  servers.forEach(server => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${server.hostname}</td>
      <td>${server.name}</td>
      <td class="ping-cell">${server.ping}</td>
      <td class="actions-cell">
        <button class="action-btn update-btn" data-server-id="${server.id}">
          <span class="material-symbols-outlined">sync</span>
        </button>
        <button class="action-btn delete-btn" data-server-id="${server.id}">
          <span class="material-symbols-outlined">delete</span>
        </button>
      </td>
    `;
    tbody.appendChild(row);
  });
}

// Delete a server
async function deleteServer(serverId) {
  try {
    const response = await fetch('/servers_api/delete_server', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ server_id: serverId }),
    });
    
    if (response.ok) {
      await fetchServers(); // Refresh the table
    } else {
      throw new Error(`Failed to delete server: ${response.status}`);
    }
  } catch (error) {
    console.error('Error deleting server:', error);
    alert('Failed to delete server. Please try again.');
  }
}

// Update a server
async function updateServer(serverId) {
  try {
    const response = await fetch('/servers_api/update_server', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ server_id: serverId }),
    });
    
    if (response.ok) {
      await fetchServers(); // Refresh the table
    } else {
      throw new Error(`Failed to update server: ${response.status}`);
    }
  } catch (error) {
    console.error('Error updating server:', error);
    alert('Failed to update server. Please try again.');
  }
}

// Add a new server
async function addServer(formData) {
  try {
    const response = await fetch('/servers_api/add_server', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });
    
    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized. Please check your credentials.');
      }
      throw new Error(`Failed to add server: ${response.status}`);
    }
    
    await fetchServers(); // Refresh the table
    closeAddServerModal();
  } catch (error) {
    console.error('Error adding server:', error);
    showModalError(error.message);
  }
}

// Show error message in modal
function showModalError(message) {
  const errorDiv = addServerModal.querySelector('.error-message');
  if (!errorDiv) {
    const modalContent = addServerModal.querySelector('.modal-content');
    const newErrorDiv = document.createElement('div');
    newErrorDiv.className = 'error-message';
    modalContent.insertBefore(newErrorDiv, modalContent.firstChild);
  }
  addServerModal.querySelector('.error-message').textContent = message;
}

// Modal functions
function openAddServerModal() {
  addServerModal.classList.add('active');
  addServerForm.reset();
  const errorDiv = addServerModal.querySelector('.error-message');
  if (errorDiv) {
    errorDiv.remove();
  }
}

function closeAddServerModal() {
  addServerModal.classList.remove('active');
}

// Initialize servers page
export function initializeServersPage() {
  serversTable = document.querySelector('.servers-table');
  addServerModal = document.getElementById('add-server-modal');
  addServerForm = document.getElementById('add-server-form');
  
  if (!serversTable || !addServerModal || !addServerForm) return;
  
  // Initial fetch
  fetchServers();
  
  // Set up auto-refresh interval (every 5 seconds)
  updateInterval = setInterval(fetchServers, 5000);
  
  // Add server button click
  const addServerBtn = document.querySelector('.add-server-btn');
  addServerBtn.addEventListener('click', openAddServerModal);
  
  // Close modal button click
  const closeModalBtn = addServerModal.querySelector('.close-modal');
  closeModalBtn.addEventListener('click', closeAddServerModal);
  
  // Cancel button click
  const cancelBtn = addServerModal.querySelector('.btn-cancel');
  cancelBtn.addEventListener('click', closeAddServerModal);
  
  // Form submission
  addServerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = {
      hostname: addServerForm.hostname.value,
      server_name: addServerForm.server_name.value,
      port: addServerForm.port.value,
      basepath: addServerForm.basepath.value,
      login: addServerForm.login.value,
      password: addServerForm.password.value
    };
    await addServer(formData);
  });
  
  // Event delegation for button clicks
  serversTable.addEventListener('click', async (e) => {
    const btn = e.target.closest('.action-btn');
    if (!btn) return;
    
    const serverId = btn.dataset.serverId;
    
    if (btn.classList.contains('delete-btn')) {
      if (confirm('Are you sure you want to delete this server?')) {
        await deleteServer(serverId);
      }
    } else if (btn.classList.contains('update-btn')) {
      await updateServer(serverId);
    }
  });
}

// Cleanup function
export function cleanupServersPage() {
  if (updateInterval) {
    clearInterval(updateInterval);
    updateInterval = null;
  }
}