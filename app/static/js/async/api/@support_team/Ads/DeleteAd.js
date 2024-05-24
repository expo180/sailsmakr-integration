import UtilApiURLs from "../../../../_globals/UtilApiUrls.js";
const URL = UtilApiURLs.DeleteAdURL

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', function () {
            const adId = this.getAttribute('data-ad-id');
            Swal.fire({
                title: 'Etes-vous sûre?',
                text: 'Vous allez supprimer cette campagne',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Oui, Supprimer'
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`${URL}${adId}`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            Swal.fire({
                                icon: 'success',
                                title: data.message
                            }).then(() => {
                                location.reload()
                            });
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: 'Erreur',
                                text: data.message || 'An error occurred while deleting the ad.'
                            });
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: 'An error occurred while deleting the ad.'
                        });
                    });
                }
            });
        });
    });
});
