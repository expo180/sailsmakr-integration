document.addEventListener('DOMContentLoaded', function () {
    const createInvoiceModal = new bootstrap.Modal(document.getElementById('CreateInvoiceModal'));

    document.getElementById('CreateInvoiceButton').addEventListener('click', function () {
        createInvoiceModal.show();
    });

    const form = document.querySelector('#createInvoiceForm')

    async function handleCreate(newInvoiceData) {
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newInvoiceData)
            });

            if (response.ok) {
                const data = await response.json();
                Swal.fire(
                    'Success!',
                    data.message,
                    'success'
                ).then((result) => {
                    if (result.isConfirmed) {
                        window.location.reload();
                    }
                });
            } else {
                const data = await response.json();
                Swal.fire(
                    'Error!',
                    data.message || 'An error occurred while creating the invoice.',
                    'error'
                );
            }
        } catch (error) {
            Swal.fire(
                'Error!',
                'An error occurred while creating the invoice.',
                'error'
            );
        }
    }

    $(document).ready(function() {
        $('#submitInvoice').on('click', function() {
            const newInvoiceData = {
                title: $('#invoiceTitle').val(),
                description: $('#invoiceDescription').val(),
                amount: $('#invoiceAmount').val()
            };
            handleCreate(newInvoiceData);
        });
    });

});