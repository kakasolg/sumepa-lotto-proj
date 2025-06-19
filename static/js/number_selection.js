
document.addEventListener('DOMContentLoaded', function() {
    // --- State ---
    let selectedMainNumbers = [];
    let selectedSpecialNumber = null;

    // --- Constants from Server (injected via data attributes) ---
    const numberSelectionCard = document.getElementById('number-selection-card');
    const maxMainNumbers = parseInt(numberSelectionCard.dataset.mainNumbersCount);
    const gamePrice = parseFloat(numberSelectionCard.dataset.ticketPrice);
    const mainRange = JSON.parse(numberSelectionCard.dataset.mainNumbersRange);
    const specialRange = JSON.parse(numberSelectionCard.dataset.specialRange);
    const favoritesData = JSON.parse(numberSelectionCard.dataset.favorites || 'null');

    // --- DOM Elements ---
    const mainNumberButtons = document.querySelectorAll('.main-number-btn');
    const specialNumberButtons = document.querySelectorAll('.special-number-btn');
    const quickPickBtn = document.getElementById('quick-pick-btn');
    const favoritesBtn = document.getElementById('favorites-btn');
    const clearBtn = document.getElementById('clear-btn');
    const addToCartBtn = document.getElementById('add-to-cart-btn');

    // --- Event Listeners ---
    mainNumberButtons.forEach(btn => btn.addEventListener('click', handleMainNumberClick));
    specialNumberButtons.forEach(btn => btn.addEventListener('click', handleSpecialNumberClick));
    quickPickBtn.addEventListener('click', handleQuickPick);
    clearBtn.addEventListener('click', () => clearSelection(true));
    if (favoritesBtn) {
        favoritesBtn.addEventListener('click', handleFavorites);
    }
    addToCartBtn.addEventListener('click', handleAddToCart);


    // --- Event Handlers ---
    function handleMainNumberClick(event) {
        const number = parseInt(event.target.dataset.number);
        if (selectedMainNumbers.includes(number)) {
            // Deselect
            selectedMainNumbers = selectedMainNumbers.filter(n => n !== number);
        } else if (selectedMainNumbers.length < maxMainNumbers) {
            // Select
            selectedMainNumbers.push(number);
            selectedMainNumbers.sort((a, b) => a - b);
        }
        updateUI();
    }

    function handleSpecialNumberClick(event) {
        const number = parseInt(event.target.dataset.number);
        if (selectedSpecialNumber === number) {
            // Deselect
            selectedSpecialNumber = null;
        } else {
            // Select
            selectedSpecialNumber = number;
        }
        updateUI();
    }

    function handleQuickPick() {
        clearSelection(false); // Clear previous selection without UI update
        
        // Pick main numbers
        while (selectedMainNumbers.length < maxMainNumbers) {
            const randomNumber = getRandomNumber(mainRange[0], mainRange[1]);
            if (!selectedMainNumbers.includes(randomNumber)) {
                selectedMainNumbers.push(randomNumber);
            }
        }
        selectedMainNumbers.sort((a, b) => a - b);

        // Pick special number
        selectedSpecialNumber = getRandomNumber(specialRange[0], specialRange[1]);

        updateUI();
    }

    function handleFavorites() {
        if (favoritesData) {
            clearSelection(false);
            selectedMainNumbers = [...favoritesData.main_numbers].sort((a, b) => a - b);
            selectedSpecialNumber = favoritesData.special_number;
            updateUI();
        }
    }

    function handleAddToCart() {
        if (selectedMainNumbers.length === maxMainNumbers && selectedSpecialNumber !== null) {
            console.log('Adding to cart:', {
                main_numbers: selectedMainNumbers,
                special_number: selectedSpecialNumber,
                price: gamePrice
            });
            // Here you would typically send this data to the server
            // For now, we can just show an alert
            alert(`Ticket added to cart!\nNumbers: ${selectedMainNumbers.join(', ')} + ${selectedSpecialNumber}`);
            
            // Optional: Clear selection after adding to cart
            clearSelection(true);
        }
    }

    // --- UI Update Functions ---
    function updateUI() {
        updateMainNumberSelection();
        updateSpecialNumberSelection();
        updateButtonStates();
        updateAddToCartButton();
    }

    function updateMainNumberSelection() {
        // Update the selected number display circles
        for (let i = 0; i < maxMainNumbers; i++) {
            const displayCircle = document.getElementById(`selected-main-${i + 1}`);
            if (selectedMainNumbers[i] !== undefined) {
                displayCircle.textContent = selectedMainNumbers[i];
                displayCircle.classList.remove('text-gray-400', 'bg-white');
                displayCircle.classList.add('text-lotto-blue', 'bg-blue-100', 'border-lotto-blue');
            } else {
                displayCircle.textContent = '-';
                displayCircle.classList.add('text-gray-400', 'bg-white');
                displayCircle.classList.remove('text-lotto-blue', 'bg-blue-100', 'border-lotto-blue');
            }
        }

        // Update the grid buttons
        mainNumberButtons.forEach(btn => {
            const number = parseInt(btn.dataset.number);
            if (selectedMainNumbers.includes(number)) {
                btn.classList.add('bg-lotto-blue', 'text-white');
                btn.classList.remove('hover:bg-lotto-blue');
            } else {
                btn.classList.remove('bg-lotto-blue', 'text-white');
                btn.classList.add('hover:bg-lotto-blue');
            }
        });
    }

    function updateSpecialNumberSelection() {
        const displayCircle = document.getElementById('selected-special');
        if (selectedSpecialNumber !== null) {
            displayCircle.textContent = selectedSpecialNumber;
            displayCircle.classList.remove('text-gray-400', 'bg-red-50');
            displayCircle.classList.add('text-red-600', 'bg-red-100', 'border-red-600');
        } else {
            displayCircle.textContent = '-';
            displayCircle.classList.add('text-gray-400', 'bg-red-50');
            displayCircle.classList.remove('text-red-600', 'bg-red-100', 'border-red-600');
        }

        specialNumberButtons.forEach(btn => {
            const number = parseInt(btn.dataset.number);
            if (selectedSpecialNumber === number) {
                btn.classList.add('bg-red-600', 'text-white');
                btn.classList.remove('hover:bg-red-600');
            } else {
                btn.classList.remove('bg-red-600', 'text-white');
                btn.classList.add('hover:bg-red-600');
            }
        });
    }
    
    function updateButtonStates() {
        const hasSelection = selectedMainNumbers.length > 0 || selectedSpecialNumber !== null;
        if (hasSelection) {
            clearBtn.classList.remove('bg-gray-300', 'cursor-not-allowed');
            clearBtn.classList.add('bg-gray-500', 'hover:bg-gray-600');
            clearBtn.disabled = false;
        } else {
            clearBtn.classList.add('bg-gray-300', 'cursor-not-allowed');
            clearBtn.classList.remove('bg-gray-500', 'hover:bg-gray-600');
            clearBtn.disabled = true;
        }
    }

    function updateAddToCartButton() {
        const isSelectionComplete = selectedMainNumbers.length === maxMainNumbers && selectedSpecialNumber !== null;
        if (isSelectionComplete) {
            addToCartBtn.disabled = false;
            addToCartBtn.classList.remove('bg-gray-400', 'cursor-not-allowed');
            addToCartBtn.classList.add('bg-lotto-blue', 'hover:bg-blue-800');
            addToCartBtn.textContent = `Add 1 Ticket to Cart ($${gamePrice.toFixed(2)})`;
        } else {
            addToCartBtn.disabled = true;
            addToCartBtn.classList.add('bg-gray-400', 'cursor-not-allowed');
            addToCartBtn.classList.remove('bg-lotto-blue', 'hover:bg-blue-800');
            const remaining = maxMainNumbers - selectedMainNumbers.length + (selectedSpecialNumber === null ? 1 : 0);
            addToCartBtn.textContent = `Select ${remaining} more number${remaining > 1 ? 's' : ''}`;
        }
    }

    // --- Utility Functions ---
    function clearSelection(update = true) {
        selectedMainNumbers = [];
        selectedSpecialNumber = null;
        if (update) {
            updateUI();
        }
    }

    function getRandomNumber(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    // --- Initial State ---
    updateUI(); // Set initial button states
});
