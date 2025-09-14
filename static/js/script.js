let currentSort = { column: -1, direction: 'asc' };

function sortTable(columnIndex, sortType) {
    const table = document.getElementById('resultsTable');
    const tbody = document.getElementById('tableBody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    // Toggle sort direction if clicking same column
    if (currentSort.column === columnIndex) {
        currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
    } else {
        currentSort.direction = 'asc';
        currentSort.column = columnIndex;
    }

    // Clear all sort indicators
    for (let i = 0; i < 5; i++) {
        const indicator = document.getElementById(`sort-${i}`);
        indicator.textContent = '↕';
        indicator.classList.remove('active');
    }

    // Set active sort indicator
    const activeIndicator = document.getElementById(`sort-${columnIndex}`);
    activeIndicator.textContent = currentSort.direction === 'asc' ? '↑' : '↓';
    activeIndicator.classList.add('active');

    // Sort rows
    rows.sort((a, b) => {
        let valueA, valueB;

        if (sortType === 'price') {
            // For price columns, use the data-price attribute
            valueA = parseFloat(a.cells[columnIndex].getAttribute('data-price'));
            valueB = parseFloat(b.cells[columnIndex].getAttribute('data-price'));
        } else {
            // For text columns
            valueA = a.cells[columnIndex].textContent.trim().toLowerCase();
            valueB = b.cells[columnIndex].textContent.trim().toLowerCase();
        }

        if (currentSort.direction === 'asc') {
            return valueA > valueB ? 1 : -1;
        } else {
            return valueA < valueB ? 1 : -1;
        }
    });

    // Rebuild table body
    tbody.innerHTML = '';
    rows.forEach(row => tbody.appendChild(row));
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effect to sortable headers
    document.querySelectorAll('.sortable').forEach(header => {
        header.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f3f4f6';
        });
        header.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
});
