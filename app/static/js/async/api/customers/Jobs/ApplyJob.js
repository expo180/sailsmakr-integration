import UtilApiURLs from "../../../../_globals/UtilApiUrls.js";
import RedirectURLs from "../../../../_globals/RedirectUrls.js";

    document.getElementById('submit-application').addEventListener('click', function() {
        const form = document.getElementById('application-form');
        const formData = new FormData(form);
        const errorMessageDiv = document.getElementById('error-message');
        const jobId = form.getAttribute('data-job-id');
        const URL = UtilApiURLs.ApplyJobURL;

        errorMessageDiv.textContent = '';

        fetch(`${URL}${jobId}`, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.message || 'An error occurred while submitting the form.');
                });
            }
            return response.json();
        })
        .then(data => {
            Swal.fire({
                icon: 'success',
                title: 'Succès',
                text: data.message
            }).then(() => {
                window.location.href = RedirectURLs.ApplyJobSuccessRedirectURL ;
            });
        })
        .catch(error => {
            errorMessageDiv.textContent = error.message;
        });
});