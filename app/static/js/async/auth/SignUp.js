import RedirectURLs from "../../_globals/RedirectUrls.js";

document.addEventListener('DOMContentLoaded', function(){
    const SignUpForm = document.querySelector('#SignUpForm');
    const emailAddress = document.querySelector('#email');
    const passWord = document.querySelector('#password');
    const ConfirmPassword = document.querySelector('#confirm_password');
    const SubmitButton = document.querySelector('#SubmitButton');
    const invalidEmailAdress = document.querySelector('#invalidEmailAdress');
    const invalidPassword = document.querySelector('#invalidPassword');
    const passwordNotMatch = document.querySelector('#passwordNotMatch');
    const spinner = document.querySelector('.animate-spin');
    const buttonText = document.querySelector('#buttonText');
    const accountAlreadyExist = document.querySelector('#accountAlreadyExists')

    emailAddress.addEventListener('input', () => {
        const emailValue = emailAddress.value.trim();
        const emailValid = validateEmail(emailValue);
        
        if (!emailValid) {
            invalidEmailAdress.classList.remove('hidden');
            SubmitButton.disabled = true;
            SubmitButton.style.cursor = 'not-allowed';
        } else {
            invalidEmailAdress.classList.add('hidden');
            SubmitButton.disabled = false;
            SubmitButton.style.cursor = 'pointer';
        }
    });

    passWord.addEventListener('input', () => {
        const passwordValue = passWord.value.trim();
        
        if (passwordValue.length < 8) {
            invalidPassword.classList.remove('hidden');
            SubmitButton.disabled = true;
            SubmitButton.style.cursor = 'not-allowed';
        } else {
            invalidPassword.classList.add('hidden');
            SubmitButton.disabled = false;
            SubmitButton.style.cursor = 'pointer';
        }
    });

    SubmitButton.addEventListener('click', () => {
        const emailValue = emailAddress.value.trim();
        const passwordValue = passWord.value.trim();
        const confirmPasswordValue = ConfirmPassword.value.trim();


        if (passwordValue !== confirmPasswordValue) {
            passwordNotMatch.classList.remove('hidden');
            SubmitButton.disabled = true;
            SubmitButton.style.cursor = 'not-allowed';
            return;
        } else {
            passwordNotMatch.classList.add('hidden');
            SubmitButton.disabled = false;
            SubmitButton.style.cursor = 'pointer';
        }

        if (!emailValue || !passwordValue || !confirmPasswordValue) {
            if (!emailValue) {
                document.getElementById('emptyEmailAdress').classList.remove('hidden');
                setTimeout(() => {
                    document.getElementById('emptyEmailAdress').classList.add('hidden');
                }, 3000);
            } else {
                document.getElementById('emptyEmailAdress').classList.add('hidden');
            }
    
            if (!passwordValue) {
                document.getElementById('emptyPassword').classList.remove('hidden');
                setTimeout(() => {
                    document.getElementById('emptyPassword').classList.add('hidden');
                }, 3000);
            } else {
                document.getElementById('emptyPassword').classList.add('hidden');
            }
    
            if (!confirmPasswordValue) {
                document.getElementById('emptyConfirmPassword').classList.remove('hidden');
                setTimeout(() => {
                    document.getElementById('emptyConfirmPassword').classList.add('hidden');
                }, 3000);
            } else {
                document.getElementById('emptyConfirmPassword').classList.add('hidden');
            }
    
            SubmitButton.disabled = true;
            SubmitButton.style.cursor = 'not-allowed';
            return;
        }

        SubmitButton.disabled = true;
        SubmitButton.style.cursor = 'not-allowed';
        spinner.classList.remove('hidden');
        buttonText.textContent = 'Loading...';

        const SignUpData = {
            email : emailValue,
            password : passwordValue
        }

        fetch(SignUpForm.action, {
            method: 'POST',
            body: JSON.stringify(SignUpData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
                SubmitButton.disabled = false;
                SubmitButton.style.cursor = 'pointer';
                spinner.classList.add('hidden');
                buttonText.textContent = 'Continuer';
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            if(data.success){
                window.location.href = RedirectURLs.SignupSuccessRedirectURL;
                accountAlreadyExist.classList.add('hidden');
                SubmitButton.disabled = false;
                SubmitButton.style.cursor = 'pointer';
                spinner.classList.add('hidden');
                buttonText.textContent = 'Continuer';

            }
            else{
                accountAlreadyExist.classList.remove('hidden')
                SubmitButton.disabled = false;
                SubmitButton.style.cursor = 'pointer';
                spinner.classList.add('hidden');
                buttonText.textContent = 'Continuer';
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            SubmitButton.disabled = false;
            SubmitButton.style.cursor = 'pointer';
            spinner.classList.add('hidden');
            buttonText.textContent = 'Continuer';
        })
    });

    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
});
