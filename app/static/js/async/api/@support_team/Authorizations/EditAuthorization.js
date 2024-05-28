import UtilApiURLs from "../../../../_globals/UtilApiUrls.js";

const URL = UtilApiURLs.checkValidityQuoteURL

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('#editQuoteSubmit').forEach(button => {
        button.addEventListener('click', function () {
            const quoteId = this.getAttribute('data-quote-id');
            const form = document.querySelector(`#editQuoteForm`);

            if (form.checkValidity()) {
                const formData = new FormData(form);
                const jsonData = {};

                formData.forEach((value, key) => {
                    jsonData[key] = value;
                });

                fetch(`${URL}${quoteId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(jsonData)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire(
                            'Mis à jour !',
                            'La demande été mise à jour avec succès.',
                            'success'
                        ).then(() => {
                            location.reload();
                        });
                    } else {
                        Swal.fire(
                            'Erreur',
                            'Une erreur s\'est produite lors de la mise à jour',
                            'error'
                        );
                    }
                });
            } else {
                form.reportValidity();
            }
        });
    });
});
