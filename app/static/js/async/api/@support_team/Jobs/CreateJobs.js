import RedirectURLs from "../../../../_globals/RedirectUrls.js";
import { quill } from './text_editor.js';

document.addEventListener('DOMContentLoaded', function () {
    const jobForm = document.getElementById('jobForm');
    const createJobButton = document.getElementById('CreateJobButton');
    const loadingText = document.getElementById('LoadingText');
    const spinner = createJobButton.querySelector('.spinner-border');

    const showError = (elementId, message) => {
        const errorElement = document.getElementById(elementId);
        errorElement.style.display = 'block';
        errorElement.textContent = message;
    };

    const hideErrors = () => {
        const errorElements = document.querySelectorAll('.text-danger');
        errorElements.forEach(element => {
            element.style.display = 'none';
            element.textContent = '';
        });
    };

    const toggleLoadingState = (isLoading) => {
        if (isLoading) {
            loadingText.style.display = 'inline-block';
            spinner.style.display = 'inline-block';
            createJobButton.disabled = true;
        } else {
            loadingText.style.display = 'none';
            spinner.style.display = 'none';
            createJobButton.disabled = false;
        }
    };

    createJobButton.addEventListener('click', async function (event) {
        event.preventDefault();
        hideErrors();
        toggleLoadingState(true);

        const formData = new FormData(jobForm);
        const data = {
            title: formData.get('title'),
            description: quill.root.innerHTML,
            location: formData.get('location'),
            salary: formData.get('salary'),
            posted_date: formData.get('posted_date'),
            closing_date: formData.get('closing_date')
        };

        try {
            const response = await fetch(jobForm.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                Swal.fire({
                    icon: 'success',
                    title: 'Succès',
                    text: result.message,
                    confirmButtonText: 'OK'
                }).then(() => {
                    window.location.href = RedirectURLs.JobCreationSuccessURL;
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Erreur',
                    text: result.message,
                    confirmButtonText: 'OK'
                });

                if (result.errors) {
                    result.errors.forEach(error => {
                        if (error.includes('titre')) showError('JobTitleError', error);
                        if (error.includes('description')) showError('JobDescriptionError', error);
                        if (error.includes('lieu')) showError('JobLocationError', error);
                        if (error.includes('salaire')) showError('JobWageError', error);
                        if (error.includes('publication')) showError('JobPuclicationDateError', error);
                        if (error.includes('clôture')) showError('JobClosingDateError', error);
                    });
                }
            }
        } catch (error) {
            console.error('Error:', error);
            Swal.fire({
                icon: 'error',
                title: 'Erreur',
                text: 'Une erreur est survenue. Veuillez réessayer.',
                confirmButtonText: 'OK'
            });
        } finally {
            toggleLoadingState(false);
        }
    });
});
