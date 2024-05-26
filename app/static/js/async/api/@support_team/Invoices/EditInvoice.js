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
            Swal.fire(
                'Success!',
                data.message,
                'success'
            );
            $('#editInvoiceModal').modal('hide');
            window.location.reload();
        } else {
            const data = await response.json();
            Swal.fire(
                'Error!',
                data.message || 'An error occurred while editing the invoice.',
                'error'
            );
        }
    } catch (error) {
        Swal.fire(
            'Error!',
            'An error occurred while editing the invoice.',
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

        $('#editInvoiceModal').modal('show');
        $('#editInvoiceSubmit').on('click', function() {
            console.log("Hello world")
            const newData = {
                title: $('#editTitle').val(),
                description: $('#editDescription').val(),
                amount: $('#editAmount').val()
            };
            handleEdit(invoiceId, newData);
        });
    });
});
