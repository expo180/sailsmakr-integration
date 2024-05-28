import UtilApiURLs from "../../../../_globals/UtilApiUrls.js";

const URL = UtilApiURLs.EditInvoiceRequestURL;

async function handleEdit(invoiceId, newData) {
    try {
        const response = await fetch(`${URL}${invoiceId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newData)
        });

        if (response.ok) {
            const data = await response.json();
            Swal.fire({
                title: 'Succès!',
                text: data.message,
                icon: 'success',
                confirmButtonText: 'OK'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.reload();
                }
            });
        } else {
            const data = await response.json();
            Swal.fire(
                'Erreur!',
                data.message || 'Une erreur est survenue lors de la modification de la facture.',
                'error'
            );
        }
    } catch (error) {
        Swal.fire(
            'Erreur!',
            'Une erreur est survenue lors de la modification de la facture.',
            'error'
        );
    }
}

$(document).ready(function() {
    $(document).on('click', '.edit-btn', function() {
        const invoiceId = $(this).data('invoice-id');
        const title = $(this).data('invoice-title');
        const description = $(this).data('invoice-description');
        const amount = $(this).data('invoice-amount');
        
        $('#editTitle').val(title);
        $('#editDescription').val(description);
        $('#editAmount').val(amount);

        $('#editInvoiceModal{{ invoice.id }}').modal('show');
    });

    $(document).on('click', '#editInvoiceSubmit', function() {
        const invoiceId = $(this).data('invoice-id');
        const newData = {
            title: $('#editTitle').val(),
            description: $('#editDescription').val(),
            amount: $('#editAmount').val()
        };
        handleEdit(invoiceId, newData);
    });
});
