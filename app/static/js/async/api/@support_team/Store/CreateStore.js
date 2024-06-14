document.addEventListener('DOMContentLoaded', () => {
    const addStoreForm = document.getElementById('addStoreForm');
    const addStoreButton = document.getElementById('addStoreButton');
    const addStoreText = document.getElementById('AddStoreText');
    const loadingText = document.getElementById('LoadingText');

    addStoreForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        addStoreButton.disabled = true;
        addStoreText.classList.add('d-none');
        loadingText.classList.remove('d-none');

        const formData = new FormData(addStoreForm);
        try {
            const response = await fetch(addStoreForm.action, {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();
            if (response.ok) {
                Swal.fire({
                    icon: 'success',
                    title: 'Magasin ajouté',
                    text: result.message,
                }).then(() => {
                    location.reload();
                });
            } else {
                throw new Error(result.message);
            }
        } catch (error) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: error.message,
            });
        } finally {
            addStoreButton.disabled = false;
            addStoreText.classList.remove('d-none');
            loadingText.classList.add('d-none');
        }
    });
});
