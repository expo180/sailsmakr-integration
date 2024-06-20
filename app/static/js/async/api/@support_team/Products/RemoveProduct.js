import UtilApiURLs from '../../../../_globals/UtilApiUrls.js';

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.removeProductBtn').forEach(btn => {
        btn.addEventListener('click', function () {
            var productId = document.getElementById('productId').value;

            Swal.fire({
                title: 'Êtes-vous sûr?',
                text: 'Vous ne pourrez pas récupérer ce produit une fois supprimé!',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Oui, supprimer!',
                cancelButtonText: 'Annuler'
            }).then((result) => {
                if (result.isConfirmed) {
                    try {
                        const formData = new FormData();
                        formData.append('id', productId);

                        fetch(UtilApiURLs.ManageProductURL, {
                            method: 'DELETE',
                            body: formData,
                        })
                        .then(response => {
                            if (!response.ok) {
                                throw new Error('Network response was not ok');
                            }
                            return response.json();
                        })
                        .then(data => {
                            Swal.fire({
                                icon: 'success',
                                title: 'Supprimé!',
                                text: 'Le produit a été supprimé.',
                            }).then(() => {
                                location.reload();
                            });
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            Swal.fire({
                                icon: 'error',
                                title: 'Erreur!',
                                text: 'Échec de la suppression du produit. Veuillez réessayer.',
                                showConfirmButton: false,
                                timer: 1500
                            });
                        });
                    } catch (error) {
                        console.error('Error:', error);
                        Swal.fire({
                            icon: 'error',
                            title: 'Erreur!',
                            text: 'Échec de la suppression du produit. Veuillez réessayer.',
                            showConfirmButton: false,
                            timer: 1500
                        });
                    }
                }
            });
        });
    });
});
