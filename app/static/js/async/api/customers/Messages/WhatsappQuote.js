import UtilApiURLs from '../../../../_globals/UtilApiUrls.js'

document.addEventListener("DOMContentLoaded", function() {
    var input = document.querySelector("#phone");

    var iti = window.intlTelInput(input, {
        initialCountry: "auto",
        separateDialCode: true,
        placeholderNumberType: "MOBILE",
        utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.min.js",
        geoIpLookup: function(callback) {
            fetch('https://ipinfo.io?token=5f5bb72138c665')
                .then(response => response.json())
                .then(data => {
                    const countryCode = (data && data.country) ? data.country : "us";
                    callback(countryCode);
                })
                .catch(() => {
                    callback("us");
                });
        },
    });

    function getFormattedPhoneNumber() {
        let phoneNumber = input.value.trim();
        let countryData = iti.getSelectedCountryData()
        let FormattedPhoneNumber = "+" + countryData.dialCode + phoneNumber
        return FormattedPhoneNumber;
    }

    var continueBtn = document.querySelector("#continueBtn");
    var errorMessage = document.querySelector("#errorMessage");
    var modal = document.getElementById("myModal");
    var closeModal = document.getElementById("closeModal");
    var submitModal = document.getElementById("submitModal");
    var modalForm = document.getElementById("modalForm");
    var spinner = document.getElementById("spinner");
    var loadingText = document.getElementById("loadingText");
    var buttonContent = document.getElementById("buttonContent");
    var firstNameError = document.getElementById("firstNameError");
    var lastNameError = document.getElementById("lastNameError");
    var messageError = document.getElementById("messageError");

    function hideErrorMessage() {
        errorMessage.classList.add("hidden");
    }

    input.addEventListener("input", hideErrorMessage);

    continueBtn.addEventListener("click", function() {
        var phoneNumber = input.value.trim();
        if (!phoneNumber) {
            errorMessage.classList.remove("hidden");
        } else {
            errorMessage.classList.add("hidden");
            showModal('myModal');
        }
    });

    closeModal.addEventListener("click", function() {
        modal.classList.add("hidden");
    });

    submitModal.addEventListener("click", function() {
        var firstName = document.getElementById("first_name").value.trim();
        var lastName = document.getElementById("last_name").value.trim();
        var message = document.getElementById("message").value.trim();

        var hasError = false;

        if (!firstName) {
            if (firstNameError) { 
                firstNameError.classList.remove("hidden");
            } else {
                console.error("firstNameError element not found");
            }
            hasError = true;
        } else {
            if (firstNameError) { 
                firstNameError.classList.add("hidden");
            } else {
                console.error("firstNameError element not found");
            }
        }

        if (!lastName) {
            if (lastNameError) { 
                lastNameError.classList.remove("hidden");
            } else {
                console.error("lastNameError element not found");
            }
            hasError = true;
        } else {
            if (lastNameError) { 
                lastNameError.classList.add("hidden");
            } else {
                console.error("lastNameError element not found");
            }
        }

        if (!message) {
            if (messageError) { 
                messageError.classList.remove("hidden");
            } else {
                console.error("messageError element not found");
            }
            hasError = true;
        } else {
            if (messageError) { 
                messageError.classList.add("hidden");
            } else {
                console.error("messageError element not found");
            }
        }

        if (!hasError) {
            spinner.classList.remove("hidden");
            loadingText.classList.remove("hidden");
            buttonContent.classList.add("hidden");


            var data = {
                first_name: firstName,
                last_name: lastName,
                message: message,
                phone: getFormattedPhoneNumber()
            };

            fetch(UtilApiURLs.SendWhatsappMassageURL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                modal.classList.add("hidden");
                spinner.classList.add("hidden");
                loadingText.classList.add("hidden");
                buttonContent.classList.remove("hidden");

                document.getElementById("successMessage").textContent = `Merci de nous avoir contacté, notre équipe vous répondra ${firstName}`;
                showModal('successModal');
            })
            .catch((error) => {
                console.error('Error:', error);
                spinner.classList.add("hidden");
                loadingText.classList.add("hidden");
                buttonContent.classList.remove("hidden");

                showModal('failureModal');
            });
        }
    });

    modalForm.addEventListener("input", function() {
        if (firstNameError) { 
            firstNameError.classList.add("hidden");
        }
        if (lastNameError) { 
            lastNameError.classList.add("hidden");
        }
        if (messageError) {
            messageError.classList.add("hidden");
        }
    });

    function showModal(modalId) {
        document.getElementById(modalId).classList.remove("hidden");
    }

    window.hideModal = function(modalId) {
        document.getElementById(modalId).classList.add("hidden");
    };
});
