/**
 * Flask CRUD Engine - Frontend Application Script
 * Communicates asynchronously with the Flask REST API backed by In-Memory Hashmap.
 */

document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const itemsContainer = document.getElementById('items-container');
    const emptyState = document.getElementById('empty-state');
    
    // Stats Elements
    const statTotal = document.getElementById('stat-total');
    const statPending = document.getElementById('stat-pending');
    const statProgress = document.getElementById('stat-progress');
    const statCompleted = document.getElementById('stat-completed');
    
    // Control Elements
    const searchInput = document.getElementById('search-input');
    const clearSearchBtn = document.getElementById('clear-search');
    const filterStatus = document.getElementById('filter-status');
    const filterPriority = document.getElementById('filter-priority');
    const filterCategory = document.getElementById('filter-category');
    const btnSeed = document.getElementById('btn-seed');
    
    // Modal Elements
    const itemModal = document.getElementById('item-modal');
    const modalTitle = document.getElementById('modal-title');
    const itemForm = document.getElementById('item-form');
    const formItemId = document.getElementById('form-item-id');
    const formTitle = document.getElementById('form-title');
    const formDescription = document.getElementById('form-description');
    const formCategory = document.getElementById('form-category');
    const formPriority = document.getElementById('form-priority');
    const formStatus = document.getElementById('form-status');
    
    const btnOpenCreate = document.getElementById('btn-open-create');
    const btnEmptyCreate = document.getElementById('btn-empty-create');
    const btnCloseModal = document.getElementById('btn-close-modal');
    const btnCancelModal = document.getElementById('btn-cancel-modal');
    
    const toastContainer = document.getElementById('toast-container');

    // --- State ---
    let searchDebounceTimer = null;

    // --- Initial Load ---
    loadItems();
    loadStats();

    // --- Event Listeners ---

    // Search input with debounce
    searchInput.addEventListener('input', (e) => {
        const val = e.target.value.trim();
        clearSearchBtn.classList.toggle('hidden', val === '');

        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = setTimeout(() => {
            loadItems();
        }, 250);
    });

    clearSearchBtn.addEventListener('click', () => {
        searchInput.value = '';
        clearSearchBtn.classList.add('hidden');
        loadItems();
    });

    // Filters
    filterStatus.addEventListener('change', loadItems);
    filterPriority.addEventListener('change', loadItems);
    filterCategory.addEventListener('change', loadItems);

    // Reset Sample Data
    btnSeed.addEventListener('click', async () => {
        try {
            const res = await fetch('/api/reset', { method: 'POST' });
            const data = await res.json();
            if (data.success) {
                showToast('Sample data loaded into Hashmap store!', 'success');
                loadItems();
                loadStats();
            }
        } catch (err) {
            showToast('Failed to reset sample data.', 'error');
        }
    });

    // Modal Triggers
    btnOpenCreate.addEventListener('click', () => openModal());
    btnEmptyCreate.addEventListener('click', () => openModal());
    btnCloseModal.addEventListener('click', closeModal);
    btnCancelModal.addEventListener('click', closeModal);

    itemModal.addEventListener('click', (e) => {
        if (e.target === itemModal) closeModal();
    });

    // Form Submit (Create / Update)
    itemForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const payload = {
            title: formTitle.value.trim(),
            description: formDescription.value.trim(),
            category: formCategory.value,
            priority: formPriority.value,
            status: formStatus.value
        };

        const id = formItemId.value;
        const isEdit = Boolean(id);
        const url = isEdit ? `/api/items/${id}` : '/api/items';
        const method = isEdit ? 'PUT' : 'POST';

        try {
            const res = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await res.json();

            if (res.ok && data.success) {
                showToast(isEdit ? 'Item updated successfully!' : 'New item added to Hashmap!', 'success');
                closeModal();
                loadItems();
                loadStats();
            } else {
                showToast(data.message || 'Validation error', 'error');
            }
        } catch (err) {
            showToast('Network error while saving item.', 'error');
        }
    });

    // --- Core Data API Operations ---

    async function loadItems() {
        const query = searchInput.value.trim();
        const status = filterStatus.value;
        const priority = filterPriority.value;
        const category = filterCategory.value;

        const params = new URLSearchParams();
        if (query) params.append('search', query);
        if (status !== 'All') params.append('status', status);
        if (priority !== 'All') params.append('priority', priority);
        if (category !== 'All') params.append('category', category);

        try {
            const res = await fetch(`/api/items?${params.toString()}`);
            const result = await res.json();

            if (result.success) {
                renderItems(result.data);
            }
        } catch (err) {
            showToast('Failed to fetch items from server.', 'error');
        }
    }

    async function loadStats() {
        try {
            const res = await fetch('/api/stats');
            const result = await res.json();
            if (result.success) {
                const s = result.data;
                statTotal.textContent = s.total;
                statPending.textContent = s.pending;
                statProgress.textContent = s.in_progress;
                statCompleted.textContent = s.completed;
            }
        } catch (err) {
            console.error('Stats loading error:', err);
        }
    }

    // --- UI Render Functions ---

    function renderItems(items) {
        itemsContainer.innerHTML = '';

        if (!items || items.length === 0) {
            emptyState.classList.remove('hidden');
            return;
        }

        emptyState.classList.add('hidden');

        items.forEach(item => {
            const card = document.createElement('div');
            card.className = `item-card ${item.status.toLowerCase().replace(' ', '-')} ${item.status === 'Completed' ? 'completed' : ''}`;
            card.setAttribute('data-priority', item.priority);

            const createdDate = new Date(item.created_at).toLocaleDateString(undefined, {
                month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
            });

            card.innerHTML = `
                <div class="item-header">
                    <div>
                        <div class="item-title">${escapeHtml(item.title)}</div>
                        <span class="item-id">${item.id}</span>
                    </div>
                </div>

                <div class="item-description">
                    ${escapeHtml(item.description || 'No description provided.')}
                </div>

                <div class="item-meta">
                    <span class="badge badge-category">
                        <i class="fa-solid fa-tag"></i> ${escapeHtml(item.category)}
                    </span>
                    <span class="badge badge-priority ${item.priority.toLowerCase()}">
                        <i class="fa-solid fa-flag"></i> ${item.priority}
                    </span>
                    <span class="badge badge-status ${item.status.toLowerCase().replace(' ', '-')}" title="Click to cycle status" data-id="${item.id}" data-status="${item.status}">
                        <i class="${getStatusIcon(item.status)}"></i> ${item.status}
                    </span>
                </div>

                <div class="item-footer">
                    <span class="item-timestamp">Updated ${createdDate}</span>
                    <div class="item-actions">
                        <button class="btn-icon btn-edit" title="Edit Item" data-id="${item.id}">
                            <i class="fa-solid fa-pen-to-square"></i>
                        </button>
                        <button class="btn-icon btn-delete" title="Delete Item" data-id="${item.id}">
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                    </div>
                </div>
            `;

            // Attach event listeners for card actions
            const statusBadge = card.querySelector('.badge-status');
            statusBadge.addEventListener('click', () => cycleStatus(item.id, item.status));

            const editBtn = card.querySelector('.btn-edit');
            editBtn.addEventListener('click', () => editItem(item));

            const deleteBtn = card.querySelector('.btn-delete');
            deleteBtn.addEventListener('click', () => deleteItem(item.id));

            itemsContainer.appendChild(card);
        });
    }

    // Cycle Status on Badge Click (Pending -> In Progress -> Completed -> Pending)
    async function cycleStatus(id, currentStatus) {
        const nextMap = {
            'Pending': 'In Progress',
            'In Progress': 'Completed',
            'Completed': 'Pending'
        };
        const nextStatus = nextMap[currentStatus] || 'Pending';

        try {
            const res = await fetch(`/api/items/${id}/status`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ status: nextStatus })
            });
            const data = await res.json();

            if (data.success) {
                showToast(`Status updated to '${nextStatus}'`, 'info');
                loadItems();
                loadStats();
            }
        } catch (err) {
            showToast('Failed to update status', 'error');
        }
    }

    async function deleteItem(id) {
        if (!confirm(`Are you sure you want to delete item ${id}?`)) return;

        try {
            const res = await fetch(`/api/items/${id}`, { method: 'DELETE' });
            const data = await res.json();

            if (data.success) {
                showToast(`Item ${id} deleted`, 'success');
                loadItems();
                loadStats();
            }
        } catch (err) {
            showToast('Failed to delete item', 'error');
        }
    }

    function editItem(item) {
        openModal(item);
    }

    // Modal Helpers
    function openModal(item = null) {
        if (item) {
            modalTitle.innerHTML = `<i class="fa-solid fa-pen-to-square"></i> Edit Item (${item.id})`;
            formItemId.value = item.id;
            formTitle.value = item.title;
            formDescription.value = item.description || '';
            formCategory.value = item.category;
            formPriority.value = item.priority;
            formStatus.value = item.status;
        } else {
            modalTitle.innerHTML = `<i class="fa-solid fa-plus-circle"></i> Create New Item`;
            itemForm.reset();
            formItemId.value = '';
            formCategory.value = 'General';
            formPriority.value = 'Medium';
            formStatus.value = 'Pending';
        }
        itemModal.classList.remove('hidden');
        formTitle.focus();
    }

    function closeModal() {
        itemModal.classList.add('hidden');
        itemForm.reset();
    }

    // Helper utilities
    function getStatusIcon(status) {
        switch (status) {
            case 'Completed': return 'fa-regular fa-circle-check';
            case 'In Progress': return 'fa-solid fa-spinner';
            default: return 'fa-regular fa-clock';
        }
    }

    function escapeHtml(str) {
        return str.replace(/[&<>"']/g, function(m) {
            return {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#039;'
            }[m];
        });
    }

    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        let icon = 'fa-info-circle';
        if (type === 'success') icon = 'fa-check-circle';
        if (type === 'error') icon = 'fa-exclamation-circle';

        toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${escapeHtml(message)}</span>`;
        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(50px)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3200);
    }
});
