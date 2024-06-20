import UtilApiURLs from "../../../../_globals/UtilApiUrls.js";

document.addEventListener('DOMContentLoaded', function () {
    const authorPhoneNumberRaw = document.querySelector('#author_phone_number_raw');
    const authorPhoneNumber = document.querySelector('#author_phone_number');
    const submitButton = document.querySelector('#submitButton');
    const submitButtonText = document.querySelector('#submitButtonText');
    const submitButtonSpinner = document.querySelector('#submitButtonSpinner');
  
    const formAlertSuccess = document.getElementById('form-alert-success');
    const formAlertError = document.getElementById('form-alert-error');
    const formAlertNetworkError = document.getElementById('form-alert-network-error');
  
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
  
    document.getElementById('contactForm').addEventListener('submit', function(event) {
      event.preventDefault();
  
      const formData = new FormData(this);
  
      formAlertSuccess.classList.add('hidden');
      formAlertError.classList.add('hidden');
      formAlertNetworkError.classList.add('hidden');
  
      submitButton.disabled = true;
      submitButtonText.classList.add('hidden');
      submitButtonSpinner.classList.remove('hidden');
  
      fetch(UtilApiURLs.SendQuoteRequestURL, {
        method: 'POST',
        body: formData,
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        if (data.success) {
          formAlertSuccess.classList.remove('hidden');
          this.reset();
        } else {
          formAlertError.classList.remove('hidden');
        }
      })
      .catch(error => {
        formAlertNetworkError.classList.remove('hidden');
        console.error('Error:', error);
      })
      .finally(() => {
        submitButton.disabled = false;
        submitButtonText.classList.remove('hidden');
        submitButtonSpinner.classList.add('hidden');
      });
    });
  
  });
  