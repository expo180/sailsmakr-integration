import RedirectURLs from "../../../../_globals/RedirectUrls.js";

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const submitButton = form.querySelector('button[type="submit"]');
    const loadingText = document.getElementById('LoadingText');
    const spinner = document.querySelector('.spinner-border');
    
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(form);

        submitButton.disabled = true;
        loadingText.style.display = 'inline';
        spinner.style.display = 'inline-block';

        fetch(form.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    title: 'Succès!',
                    text: data.message,
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then(() => {
                    window.location.href = RedirectURLs.JobCreationSuccessURL;
                });
            } else {
                Swal.fire({
                    title: 'Erreur!',
                    text: data.message,
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                title: 'Erreur!',
                text: 'Une erreur s\'est produite lors de la modification',
                icon: 'error',
                confirmButtonText: 'OK'
            });
        })
        .finally(() => {
            submitButton.disabled = false;
            loadingText.style.display = 'none';
            spinner.style.display = 'none';
        });
    });
});
