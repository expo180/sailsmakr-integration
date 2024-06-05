document.addEventListener('DOMContentLoaded', function () {
    const authorPhoneNumberRaw = document.querySelector('#author_phone_number_raw');
    const authorPhoneNumber = document.querySelector('#author_phone_number');

    const iti = window.intlTelInput(authorPhoneNumberRaw, {
        utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.12/js/utils.js",
        initialCountry: "auto",
        geoIpLookup: function (callback) {
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

    authorPhoneNumberRaw.addEventListener('input', function () {
        authorPhoneNumber.value = iti.getNumber();
    });
});