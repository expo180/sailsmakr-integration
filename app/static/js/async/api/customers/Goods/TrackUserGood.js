import UtilApiURLs from "../../../../_globals/UtilApiUrls.js";

document.getElementById('tokenForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const token = document.getElementById('tokenInput').value;
    const iframeContainer = document.getElementById('iframeContainer');

    const iframeSrc = `/api/product-location/${token}`;

    iframeContainer.innerHTML = `
        <iframe src="${iframeSrc}" width="100%" height="600" frameborder="0" allowfullscreen></iframe>
    `;

    function populatePurchaseDatalist() {
        fetch(UtilApiURLs.PopulatePurchaseDataListURL, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                const purchasesDatalist = document.getElementById('purchases');
                purchasesDatalist.innerHTML = '';
                data.forEach(purchase => {
                    const option = document.createElement('option');
                    option.value = purchase.token;
                    option.textContent = purchase.title;
                    purchasesDatalist.appendChild(option);
                });
            })
        .catch(error => {
            console.error('Error fetching purchases:', error);
        });
    }

    populatePurchaseDatalist()
});