document.addEventListener('DOMContentLoaded', () =>{
    document.getElementById('get-rates').addEventListener('click', function() {
        const departPort = document.getElementById('DepartPort').value;
        const arrival = document.getElementById('Arrival').value;
        const cargoType = document.getElementById('type-of-cargo').value;
        const date = document.getElementById('Date').value;
      
        fetch('/get-rates', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            DepartPort: departPort,
            Arrival: arrival,
            CargoType: cargoType,
            Date: date
          })
        })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          window.location.href = '/display-rates?rates=' + encodeURIComponent(JSON.stringify(data));
        })
        .catch(error => console.error('Error:', error));
    });
})
  