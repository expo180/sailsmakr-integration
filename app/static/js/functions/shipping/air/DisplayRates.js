document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const rates = JSON.parse(decodeURIComponent(urlParams.get('rates')));
  
  const ratesList = document.getElementById('rates-list');
  rates.forEach(rate => {
    const li = document.createElement('li');
    li.className = 'py-2 px-4 border-b border-gray-300';
    li.textContent = `Service: ${rate.serviceType}, Rate: ${rate.totalNetCharge}`;
    ratesList.appendChild(li);
  });

});