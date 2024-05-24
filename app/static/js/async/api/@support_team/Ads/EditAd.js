document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.modal form').forEach(form => {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const adId = this.getAttribute('id').replace('editAdForm', '');
            const formData = new FormData(this);
            const saveButton = document.getElementById(`SaveEditButton${adId}`);
            const loadingText = document.getElementById(`LoadingText${adId}`);
            const saveEditText = document.getElementById(`SaveEdit${adId}`);
            const spinner = document.getElementById(`EditSpinner${adId}`);
            
            saveButton.disabled = true;
            loadingText.style.display = 'inline';
            saveEditText.style.display = 'none';
            spinner.style.display = 'inline-block';

            fetch(this.action, {
                method: 'POST',
                body: JSON.stringify(Object.fromEntries(formData)),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                saveButton.disabled = false;
                loadingText.style.display = 'none';
                saveEditText.style.display = 'inline';
                spinner.style.display = 'none';

                if (data.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Succès!',
                        text: data.message,
                        confirmButtonText: 'OK'
                    }).then(() => {
                        location.reload();
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Erreur!',
                        text: data.message || 'Une erreur s\'est produite lors de la mise à jour de la campagne.',
                        confirmButtonText: 'OK'
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                saveButton.disabled = false;
                loadingText.style.display = 'none';
                saveEditText.style.display = 'inline';
                spinner.style.display = 'none';
                
                Swal.fire({
                    icon: 'error',
                    title: 'Erreur!',
                    text: 'Une erreur s\'est produite lors de la mise à jour de la campagne.',
                    confirmButtonText: 'OK'
                });
            });
        });
    });
});
