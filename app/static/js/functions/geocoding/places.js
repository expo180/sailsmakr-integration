import UtilApiURLs from '../../_globals/UtilApiUrls.js';

const APiURL = UtilApiURLs.AddressAutoCompleteURL;

document.addEventListener('DOMContentLoaded', function() {
    const departPortInput = document.getElementById('DepartPort');
    const suggestionsList = document.getElementById('suggestions');
    const arrivalInput = document.getElementById('Arrival');
    const suggestionsListArrival = document.getElementById('suggestions-arrival');

    let debounceTimer;

    const handleInput = async (input, suggestions) => {
        const query = input.value;

        if (query.length > 2) {
            suggestions.innerHTML = '<li class="p-2 text-gray-500">Loading...</li>';
            suggestions.classList.remove('hidden');

            try {
                const response = await fetch(`${APiURL}?query=${query}`);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();

                suggestions.innerHTML = '';
                if (data.length > 0) {
                    data.forEach(item => {
                        const li = document.createElement('li');
                        li.textContent = item;
                        li.classList.add('p-2', 'hover:bg-gray-200', 'cursor-pointer');
                        li.addEventListener('click', function() {
                            input.value = item;
                            suggestions.innerHTML = '';
                            suggestions.classList.add('hidden');
                        });
                        suggestions.appendChild(li);
                    });
                } else {
                    const li = document.createElement('li');
                    li.textContent = 'No data found';
                    li.classList.add('p-2', 'text-red-500');
                    suggestions.appendChild(li);
                }
            } catch (error) {
                console.error('Error fetching data:', error);
                suggestions.innerHTML = '<li class="p-2 text-red-500">Error fetching data</li>';
            }
        } else {
            suggestions.innerHTML = '';
            suggestions.classList.add('hidden');
        }
    };

    const debounce = (func, delay) => {
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => func.apply(context, args), delay);
        };
    };

    departPortInput.addEventListener('input', debounce(() => handleInput(departPortInput, suggestionsList), 300));
    arrivalInput.addEventListener('input', debounce(() => handleInput(arrivalInput, suggestionsListArrival), 300));
});
