import UtilApiURLs from "../../../../_globals/UtilApiUrls.js";

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.delete-store').forEach(button => {
        button.addEventListener('click', async (event) => {
            const storeId = event.currentTarget.getAttribute('data-store-id');
            Swal.fire({
                title: 'Etes-vous sûre de vouloir continuer',
                text: 'Cette action est irréversible',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Oui, supprimer!'
            }).then(async (result) => {
                if (result.isConfirmed) {
                    try {
                        const formData = new FormData();
                        formData.append('id', storeId);

                        const response = await fetch(UtilApiURLs.DeleteStoreURL, {
                            method: 'DELETE',
                            body: formData,
                        });

                        const result = await response.json();
                        if (response.ok) {
                            Swal.fire({
                                icon: 'success',
                                title: 'Supprimé!',
                                text: result.message,
                            }).then(() => {
                                location.reload();
                            });
                        } else {
                            throw new Error(result.message);
                        }
                    } catch (error) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: error.message,
                        });
                    }
                }
            });
        });
    });
});
