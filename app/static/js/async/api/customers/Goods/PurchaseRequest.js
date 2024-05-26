import RedirectUrls from '../../../../_globals/RedirectUrls.js';

document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('#PurchaseRequestForm');
  const sendButton = document.querySelector('#SendQuoteRequestButton');
  const spinner = document.querySelector('#spinner');
  const loadingText = document.querySelector('#LoadingText');
  const SendIcon = document.querySelector('#SendIcon');
  const SendText = document.querySelector('#SendText');
  const authorLastName = document.querySelector('#author_last_name');
  const authorFirstName = document.querySelector('#author_first_name');
  const title = document.querySelector('#title');
  const category = document.querySelector('#category');
  const authorPhoneNumberRaw = document.querySelector('#author_phone_number_raw');
  const authorPhoneNumber = document.querySelector('#author_phone_number');
  const authorEmailAddress = document.querySelector('#author_email_address');
  const location = document.querySelector('#AuthorCountry');
  const userAddress = document.querySelector('#author_address');

  const iti = window.intlTelInput(authorPhoneNumberRaw, {
    utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@23.0.10/build/js/utils.js",
    initialCountry: "auto",
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

  function validateInput() {
    let isValid = true;

    if (authorLastName.value.trim() === '') {
      document.querySelector('#LastNameError').style.display = 'block';
      isValid = false;
    } else {
      document.querySelector('#LastNameError').style.display = 'none';
    }

    if (authorFirstName.value.trim() === '') {
      document.querySelector('#FirstNameError').style.display = 'block';
      isValid = false;
    } else {
      document.querySelector('#FirstNameError').style.display = 'none';
    }

    if (title.value.trim() === '') {
      document.querySelector('#ProductNameError').style.display = 'block';
      isValid = false;
    } else {
      document.querySelector('#ProductNameError').style.display = 'none';
    }

    if (category.value.trim() === '') {
      document.querySelector('#ProductCategoryError').style.display = 'block';
      isValid = false;
    } else {
      document.querySelector('#ProductCategoryError').style.display = 'none';
    }

    if (authorPhoneNumberRaw.value.trim() === '') {
      document.querySelector('#AuthorPhoneError').style.display = 'block';
      isValid = false;
    } else {
      document.querySelector('#AuthorPhoneError').style.display = 'none';
    }

    if (authorEmailAddress.value.trim() === '') {
      document.querySelector('#AuthorEmptyEmailError').style.display = 'block';
      isValid = false;
    } else if (!authorEmailAddress.value.includes('@')) {
      document.querySelector('#AuthorInvalidEmailError').style.display = 'block';
      isValid = false;
    } else {
      document.querySelector('#AuthorEmptyEmailError').style.display = 'none';
      document.querySelector('#AuthorInvalidEmailError').style.display = 'none';
    }

    if (location.value.trim() === '') {
      document.querySelector('#AuthorCountryError').style.display = 'block';
      isValid = false;
    } else {
      document.querySelector('#AuthorCountryError').style.display = 'none';
    }

    if (userAddress.value.trim() === '') {
      document.querySelector('#AddressError').style.display = 'block';
      isValid = false;
    } else {
      document.querySelector('#AddressError').style.display = 'none';
    }

    sendButton.disabled = !isValid;
  }

  const inputs = [authorLastName, authorFirstName, title, category, authorPhoneNumberRaw, authorEmailAddress, location, userAddress];
  inputs.forEach(input => input.addEventListener('input', validateInput));

  form.addEventListener('submit', function(event) {
    event.preventDefault();

    const errorMessages = document.querySelectorAll('.text-danger.my-1');
    errorMessages.forEach(function(msg) {
      msg.style.display = 'none';
    });

    validateInput();

    if (sendButton.disabled) {
      return;
    }

    spinner.style.display = 'inline-block';
    loadingText.style.display = 'inline-block';
    SendIcon.style.display = 'none';
    SendText.style.display = 'none';

    authorPhoneNumber.value = iti.getNumber();

    const formData = new FormData(form);

    formData.set('product_picture_url', JSON.stringify([]));
    formData.set('doc_url', JSON.stringify([]));

    fetch(form.action, {
      method: 'POST',
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      if (data.errors) {
        for (const key in data.errors) {
          document.querySelector(`#${key}Error`).textContent = data.errors[key];
          document.querySelector(`#${key}Error`).style.display = 'block';
        }
      } else {
        Swal.fire({
          icon: 'success',
          title: data.title,
          text: data.message,
          confirmButtonText: 'OK'
        }).then(() => {
          window.location.href = RedirectUrls.PurchaseRequestSendSuccess;
        });
      }
    })
    .catch(error => {
      Swal.fire({
        icon: 'error',
        title: 'Erreur',
        text: error.error,
      });
    })
    .finally(() => {
      spinner.style.display = 'none';
      loadingText.style.display = 'none';
      SendIcon.style.display = 'inline-block';
      SendText.style.display = 'inline-block';
    });
  });

  validateInput();
});
