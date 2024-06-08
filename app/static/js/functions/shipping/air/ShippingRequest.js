import UtilApiURLs from '../../_globals/UtilApiUrls.js';

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('get-rates').addEventListener('click', async () => {
      console.log("Hello world");
      const DepartPort = document.getElementById('DepartPort').value;
      const Arrival = document.getElementById('Arrival').value;
      const Date = document.getElementById('Date').value;
      const Weight = document.getElementById('Weight') ? document.getElementById('Weight').value : null;
      const Volume = document.getElementById('Volume') ? document.getElementById('Volume').value : null;
      const Length = document.getElementById('Length') ? document.getElementById('Length').value : null;
      const Width = document.getElementById('width') ? document.getElementById('width').value : null;
      const Height = document.getElementById('height') ? document.getElementById('height').value : null;

      const payload = {
        DepartPort,
        Arrival,
        Date,
        Weight,
        Volume,
        Length,
        Width,
        Height
      };

      try {
        const response = await fetch(UtilApiURLs.GetAirFreightRatesURL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
          console.log(data);
          document.getElementById('results').innerHTML = JSON.stringify(data, null, 2);
        } else {
          console.error('Error fetching freight rates:', data.details);
          document.getElementById('results').innerHTML = 'Error fetching freight rates: ' + data.details;
        }
      } catch (error) {
        console.error('Error fetching freight rates:', error);
        document.getElementById('results').innerHTML = 'Error fetching freight rates';
      }
    });
  });