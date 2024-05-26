import UtilApiURLs from "../../../../_globals/UtilApiUrls.js";

const URL = UtilApiURLs.DeletePurchaseRequestURLSales;

async function handleDelete(purchaseId) {
    const result = await Swal.fire({
        title: 'Êtes-vous sûr?',
        text: "Cette action est irréversible!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Oui, supprimer!'
    });

    if (result.isConfirmed) {
        try {
            const response = await fetch(`${URL}${purchaseId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();
            if (response.ok) {
                Swal.fire(
                    'Supprimé!',
                    data.message,
                    'success'
                ).then(() => {
                    location.reload();
                });
            } else {
                Swal.fire(
                    'Erreur!',
                    data.message || 'Une erreur est survenue lors de la suppression de l\'achat.',
                    'error'
                );
            }
        } catch (error) {
            Swal.fire(
                'Erreur!',
                'Une erreur est survenue lors de la suppression de l\'achat.',
                'error'
            );
        }
    }
}

$(document).ready(function() {
    $(document).on('click', '.delete-btn', function() {
        const purchaseId = $(this).data('purchase-id');
        handleDelete(purchaseId);
    });
});
