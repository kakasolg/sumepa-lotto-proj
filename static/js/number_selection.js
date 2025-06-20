document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('number-selection-container');
    if (!container) {
        console.error('Number selection container not found. Aborting script.');
        return;
    }

    // --- State ---
    let selectedMainNumbers = [];
    let selectedSpecialNumber = null;
    let tickets = []; // Array to hold multiple ticket selections for the list

    // --- Constants from Server (injected via data attributes) ---
    const gameId = container.dataset.gameId;
    const mainNumbersCount = parseInt(container.dataset.mainNumbersCount);
    const mainNumbersRange = JSON.parse(container.dataset.mainNumbersRange);
    const specialBallName = container.dataset.specialBallName;
    const specialBallRange = JSON.parse(container.dataset.specialBallRange);
    const ticketPrice = parseFloat(container.dataset.ticketPrice);

    // --- DOM Elements ---
    const quickPickBtn = document.getElementById('quick-pick-btn');
    const clearBtn = document.getElementById('clear-btn');
    const addToListBtn = document.getElementById('add-to-list-btn');
    const addAllToCartBtn = document.getElementById('add-all-to-cart-btn');
    const ticketsListContainer = document.getElementById('tickets-list-container');
    const totalPriceDisplay = document.getElementById('total-price-display');
    const ticketCountDisplay = document.getElementById('ticket-count-display');
    const mainNumberButtons = document.querySelectorAll('.main-number-btn');
    const specialNumberButtons = document.querySelectorAll('.special-number-btn');

    // --- Event Listeners ---
    if (quickPickBtn) quickPickBtn.addEventListener('click', handleQuickPick);
    if (clearBtn) clearBtn.addEventListener('click', () => clearCurrentSelection(true));
    if (addToListBtn) addToListBtn.addEventListener('click', handleAddToList);
    if (addAllToCartBtn) addAllToCartBtn.addEventListener('click', handleAddAllToCart);
    mainNumberButtons.forEach(btn => btn.addEventListener('click', handleMainNumberClick));
    specialNumberButtons.forEach(btn => btn.addEventListener('click', handleSpecialNumberClick));


    // --- Functions ---
    function handleMainNumberClick(event) {
        const number = parseInt(event.target.dataset.number);
        if (selectedMainNumbers.includes(number)) {
            // Deselect
            selectedMainNumbers = selectedMainNumbers.filter(n => n !== number);
        } else if (selectedMainNumbers.length < mainNumbersCount) {
            // Select
            selectedMainNumbers.push(number);
            selectedMainNumbers.sort((a, b) => a - b);
        }
        updateUi();
    }

    function handleSpecialNumberClick(event) {
        const number = parseInt(event.target.dataset.number);
        selectedSpecialNumber = (selectedSpecialNumber === number) ? null : number;
        updateUi();
    }

    function handleQuickPick() {
        clearCurrentSelection(false);
        selectedMainNumbers = generateRandomNumbers(mainNumbersCount, mainNumbersRange[0], mainNumbersRange[1]);
        if (specialBallName) {
            selectedSpecialNumber = generateRandomNumbers(1, specialBallRange[0], specialBallRange[1])[0];
        }
        updateUi();
    }

    function handleAddToList() {
        if (!isSelectionComplete()) return;

        const newTicket = {
            main_numbers: [...selectedMainNumbers],
            special_number: selectedSpecialNumber
        };
        tickets.push(newTicket);
        
        renderTicketsList();
        clearCurrentSelection(true);
    }

    async function handleAddAllToCart() {
        if (tickets.length === 0) return;

        // Prepare tickets in the format expected by the server
        const ticketsForServer = tickets.map(t => ({
            numbers: t.main_numbers,
            [specialBallName.toLowerCase().replace(' ', '_')]: t.special_number
        }));

        try {
            const response = await fetch('/add_to_cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    game_id: gameId, 
                    tickets: ticketsForServer
                })
            });

            if (!response.ok) {
                throw new Error('Server responded with an error.');
            }

            const data = await response.json();

            if (data.success) {
                updateCartCount(data.cart_count);
                tickets = []; // Clear the local list
                renderTicketsList(); // Re-render to show it's empty
                // Optionally, show a success message
                alert('Tickets successfully added to your cart!');
            } else {
                console.error('Failed to add to cart:', data.message);
            }
        } catch (error) {
            console.error('Error adding to cart:', error);
        }
    }

    function updateCartCount(count) {
        const cartCountElement = document.getElementById('cart-count');
        if (cartCountElement) {
            cartCountElement.textContent = count;
            cartCountElement.classList.remove('hidden');
        }
    }

    function clearCurrentSelection(update = true) {
        selectedMainNumbers = [];
        selectedSpecialNumber = null;
        if (update) {
            updateUi();
        }
    }

    function isSelectionComplete() {
        const mainNumbersOk = selectedMainNumbers.length === mainNumbersCount;
        const specialBallOk = specialBallName ? selectedSpecialNumber !== null : true;
        return mainNumbersOk && specialBallOk;
    }

    function updateUi() {
        // Update display for current selection
        updateSelectedNumbersDisplay();
        // Update number grid buttons
        updateNumberGrid();
        // Update button states
        updateButtonStates();
    }

    function updateSelectedNumbersDisplay() {
        for (let i = 0; i < mainNumbersCount; i++) {
            const displayCircle = document.getElementById(`selected-main-${i + 1}`);
            if (displayCircle) {
                displayCircle.textContent = selectedMainNumbers[i] || '-';
                // Add/remove classes for styling
            }
        }
        const specialDisplay = document.getElementById('selected-special');
        if (specialDisplay) {
            specialDisplay.textContent = selectedSpecialNumber || '-';
            // Add/remove classes for styling
        }
    }

    function updateNumberGrid() {
        mainNumberButtons.forEach(btn => {
            const num = parseInt(btn.dataset.number);
            btn.classList.toggle('selected', selectedMainNumbers.includes(num));
        });
        specialNumberButtons.forEach(btn => {
            const num = parseInt(btn.dataset.number);
            btn.classList.toggle('selected', selectedSpecialNumber === num);
        });
    }

    function updateButtonStates() {
        const selectionComplete = isSelectionComplete();
        if (addToListBtn) {
            addToListBtn.disabled = !selectionComplete;
        }
        if (clearBtn) {
            const hasSelection = selectedMainNumbers.length > 0 || selectedSpecialNumber !== null;
            clearBtn.disabled = !hasSelection;
        }
        if (addAllToCartBtn) {
            addAllToCartBtn.disabled = tickets.length === 0;
        }
    }

    function renderTicketsList() {
        if (!ticketsListContainer || !totalPriceDisplay || !ticketCountDisplay) return;

        ticketsListContainer.innerHTML = ''; // Clear previous list
        if (tickets.length > 0) {
            const list = document.createElement('ul');
            list.className = 'space-y-3';
            tickets.forEach((ticket, index) => {
                const listItem = document.createElement('li');
                listItem.className = 'bg-gray-100 p-4 rounded-lg flex items-center justify-between';
                
                let numbersHtml = `<span class="font-mono text-gray-800">${ticket.main_numbers.join(', ')}</span>`;
                if (ticket.special_number) {
                    numbersHtml += ` <span class="font-bold text-lotto-gold">| ${ticket.special_number}</span>`;
                }

                listItem.innerHTML = `
                    <div>
                        <span class="font-semibold text-gray-600 mr-4">Ticket ${index + 1}</span>
                        ${numbersHtml}
                    </div>
                    <button class="remove-ticket-btn text-red-500 hover:text-red-700" data-index="${index}">Remove</button>
                `;
                list.appendChild(listItem);
            });
            ticketsListContainer.appendChild(list);

            // Add event listeners for new remove buttons
            document.querySelectorAll('.remove-ticket-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const indexToRemove = parseInt(e.target.dataset.index);
                    tickets.splice(indexToRemove, 1);
                    renderTicketsList(); // Re-render the list
                });
            });
        }

        // Update total price and count
        const total = tickets.length * ticketPrice;
        totalPriceDisplay.textContent = `$${total.toFixed(2)}`;
        ticketCountDisplay.textContent = `${tickets.length} Tickets Selected`;
        
        // Update button states after rendering
        updateButtonStates();
    }

    function generateRandomNumbers(count, min, max) {
        const numbers = new Set();
        while (numbers.size < count) {
            numbers.add(Math.floor(Math.random() * (max - min + 1)) + min);
        }
        return Array.from(numbers).sort((a, b) => a - b);
    }

    // Initial UI setup
    updateUi();
    renderTicketsList();
});
