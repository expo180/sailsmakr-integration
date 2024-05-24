document.addEventListener('DOMContentLoaded', function () {
    const createInvoiceModal = new bootstrap.Modal(document.getElementById('CreateInvoiceModal'));

    document.getElementById('CreateInvoiceButton').addEventListener('click', function () {
        createInvoiceModal.show();
    });

    document.getElementById('submitInvoice').addEventListener('click', function () {
        const invoiceTitle = document.getElementById('invoiceTitle').value.trim();
        const invoiceAmount = document.getElementById('invoiceAmount').value.trim();
        const invoiceDescription = document.getElementById('invoiceDescription').value.trim();
        const form = document.querySelector('#createInvoiceForm')

        let isValid = true;
        document.getElementById('titleError').style.display = 'none';
        document.getElementById('amountError').style.display = 'none';
        document.getElementById('amountInvalidError').style.display = 'none';

        if (invoiceTitle === '') {
            document.getElementById('titleError').style.display = 'block';
            isValid = false;
        }

        if (invoiceAmount === '') {
            document.getElementById('amountError').style.display = 'block';
            isValid = false;
        } else if (isNaN(invoiceAmount) || Number(invoiceAmount) <= 0) {
            document.getElementById('amountInvalidError').style.display = 'block';
            isValid = false;
        }

        if (isValid) {
            document.getElementById('loadingText').style.display = 'inline';
            document.getElementById('addInvoice').style.display = 'none';
            document.getElementById('loadingSpinner').style.display = 'inline';

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token() }}'
                },
                body: JSON.stringify({
                    title: invoiceTitle,
                    amount: invoiceAmount,
                    description: invoiceDescription
                })
            }).then(response => response.json()).then(data => {
                if (response.ok) {
                    createInvoiceModal.hide();
                    toastr.success(data.message, 'Succès');

                    document.getElementById('loadingText').style.display = 'none';
                    document.getElementById('addInvoice').style.display = 'inline';
                    document.getElementById('loadingSpinner').style.display = 'none';

                    document.getElementById('createInvoiceForm').reset();
                } else {
                    toastr.error(data.message, 'Erreur');
                    document.getElementById('loadingText').style.display = 'none';
                    document.getElementById('addInvoice').style.display = 'inline';
                    document.getElementById('loadingSpinner').style.display = 'none';
                }
            }).catch(error => {
                toastr.error('An error occurred. Please try again.', 'Erreur');
                document.getElementById('loadingText').style.display = 'none';
                document.getElementById('addInvoice').style.display = 'inline';
                document.getElementById('loadingSpinner').style.display = 'none';
            });
        } else {
            toastr.error('Veuillez corriger les erreurs dans le formulaire.', 'Erreur');
        }
    });
});