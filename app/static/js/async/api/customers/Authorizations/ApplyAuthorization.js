import RedirectURLs from "../../../../_globals/RedirectUrls.js";

document.addEventListener('DOMContentLoaded', function() {
    const sendQuoteRequestButton = document.getElementById('SendQuoteRequestButton');
    const spinner = document.getElementById('spinner');
    const loadingText = document.getElementById('LoadingText');
    const SendIcon = document.getElementById('SendIcon');
    const sendText = document.getElementById('sendText');
    const AuthorizationApplyForm = document.querySelector('#AuthorizationApplyForm');

    sendQuoteRequestButton.addEventListener('click', function(event) {
        event.preventDefault();

        document.querySelectorAll('.text-danger').forEach(el => el.style.display = 'none');

        const clientFirstName = document.getElementById('ClientFirstName').value.trim();
        const clientLastName = document.getElementById('ClientLastName').value.trim();
        const clientPhoneNumber = document.getElementById('ClientPhone').value.trim();
        const clientSignatureFile = document.getElementById('ClientSignatureFile').files[0];
        const clientLocation = document.getElementById('ClientLocation').value.trim();
        const ladingNumber = document.getElementById('LaddingNumber').value.trim();
        const agentFirstName = document.getElementById('AgentFirstName').value.trim();
        const agentLastName = document.getElementById('AgentLastName').value.trim();
        const shippingCompanyTitle = document.getElementById('ShippingCompanyTitle').value.trim();
        const clientIdFile = document.getElementById('ClientIdFile').files[0];

        let hasError = false;

        // Validate inputs
        if (!/^[a-zA-Z]+$/.test(clientFirstName)) {
            document.getElementById('FirstNameError').style.display = 'block';
            hasError = true;
        }

        if (!/^[a-zA-Z]+$/.test(clientLastName)) {
            document.getElementById('LastNameError').style.display = 'block';
            hasError = true;
        }

        if (!/^\d+$/.test(clientPhoneNumber)) {
            document.getElementById('PhoneError').style.display = 'block';
            hasError = true;
        }

        if (!clientSignatureFile) {
            document.getElementById('ClientSignatureIdFileError').style.display = 'block';
            hasError = true;
        }

        if (!clientLocation) {
            document.getElementById('AdresseError').style.display = 'block';
            hasError = true;
        }

        if (!/^[a-zA-Z]+$/.test(agentFirstName)) {
            document.getElementById('AgentFirstNameError').style.display = 'block';
            hasError = true;
        }

        if (!/^[a-zA-Z]+$/.test(agentLastName)) {
            document.getElementById('AgentLastNameError').style.display = 'block';
            hasError = true;
        }

        if (!shippingCompanyTitle) {
            document.getElementById('ShippingCompanyTitleError').style.display = 'block';
            hasError = true;
        }

        if (!clientIdFile) {
            document.getElementById('ClientIdFileError').style.display = 'block';
            hasError = true;
        }

        if (hasError) {
            return;
        }

        spinner.style.display = 'inline-block';
        loadingText.style.display = 'inline';
        sendText.style.display = 'none';
        SendIcon.style.display = 'none';

        const formData = new FormData();
        formData.append('client_first_name', clientFirstName);
        formData.append('client_last_name', clientLastName);
        formData.append('client_phone_number', clientPhoneNumber);
        formData.append('client_signature_url', clientSignatureFile);
        formData.append('client_location', clientLocation);
        formData.append('lading_number', ladingNumber);
        formData.append('agent_first_name', agentFirstName);
        formData.append('agent_last_name', agentLastName);
        formData.append('shipping_company_title', shippingCompanyTitle);
        formData.append('client_id_card_url', clientIdFile);

        fetch(AuthorizationApplyForm.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            spinner.style.display = 'none';
            loadingText.style.display = 'none';
            sendText.style.display = 'inline-block';
            SendIcon.style.display = 'inline-block';

            if (data.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Envoyé',
                    text: data.message,
                    confirmButtonText: 'OK'
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = RedirectURLs.AuthorizationSuccessRedirectURL;
                    }
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: data.message || 'Failed to submit authorization request.'
                });
            }
        })
        .catch(error => {
            spinner.style.display = 'none';
            loadingText.style.display = 'none';
            sendText.style.display = 'inline-block';
            SendIcon.style.display = 'inline-block';

            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'An error occurred while submitting your request. Please try again later.'
            });
            console.error('Error:', error);
        });
    });
});
