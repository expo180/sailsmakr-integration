import UtilApiURLs from "../../../../_globals/UtilApiUrls.js";

const URL = UtilApiURLs.DeleteInvoiceRequestURL;

async function handleDelete(invoiceId) {
    try {
        const response = await fetch(`${URL}${invoiceId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            const data = await response.json();
            Swal.fire({
                title : 'Success!',
                icon: 'success',
                text: data.message,
                confirmButtonText: 'OK'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.reload();
                }
            });
        } else {
            const data = await response.json();
            Swal.fire(
                'Error!',
                data.message || 'An error occurred while deleting the invoice.',
                'error'
            );
        }
    } catch (error) {
        Swal.fire(
            'Error!',
            'An error occurred while deleting the invoice.',
            'error'
        );
    }
}

$(document).ready(function() {
    $(document).on('click', '.delete-btn', function() {
        const invoiceId = $(this).data('invoice-id');
        Swal.fire({
            title: 'Êtes-vous sûr?',
            text: 'Vous ne pourrez pas revenir en arrière après cette action!',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Oui, supprimer!',
            cancelButtonText: 'Annuler'
        }).then((result) => {
            if (result.isConfirmed) {
                handleDelete(invoiceId);
            }
        });
    });
});
