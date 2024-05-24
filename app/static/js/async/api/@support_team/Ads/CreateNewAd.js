import RedirectURLs from "../../../../_globals/RedirectUrls.js";

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#createAdForm');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Network response was not ok');
            }
        })
        .then(data => {
            Swal.fire({
                icon: 'success',
                title: 'Campagne créee avec succès!',
                text: data.message,
                confirmButtonText: 'OK'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = RedirectURLs.CreateAdSuccessURL;
                }
            });
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                icon: 'error',
                title: 'Erreur!',
                text: 'Une erreur s\'est produite. Veuillez réessayer plus tard.',
                confirmButtonText: 'OK'
            });
        });
    });
});
