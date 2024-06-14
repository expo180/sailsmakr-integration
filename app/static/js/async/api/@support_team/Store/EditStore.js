import UtilApiURLs from "../../../../_globals/UtilApiUrls.js";

document.addEventListener('DOMContentLoaded', () => {
    const editStoreForm = document.getElementById('editStoreForm');
    const editStoreButton = document.getElementById('editStoreButton');
    const editStoreText = document.getElementById('EditStoreText');
    const editLoadingText = document.getElementById('EditLoadingText');

    document.querySelectorAll('.edit-store').forEach(button => {
        button.addEventListener('click', async (event) => {
            const storeId = event.currentTarget.getAttribute('data-store-id');
            try {
                const response = await fetch(`${UtilApiURLs.GetStoreDetailsURL}/${storeId}`);
                if (!response.ok) {
                    throw new Error('Failed to fetch store details');
                }
                const store = await response.json();

                editStoreForm.setAttribute('data-store-id', store.id);
                document.getElementById('EditStoreName').value = store.name;
                document.getElementById('EditStoreLocation').value = store.location;
                document.getElementById('EditStoreEmail').value = store.email;
                document.getElementById('EditStorePhone').value = store.phone;
            } catch (error) {
                console.error('Error fetching store details:', error);
            }
        });
    });

    editStoreForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        editStoreButton.disabled = true;
        editStoreText.classList.add('d-none');
        editLoadingText.classList.remove('d-none');

        const storeId = editStoreForm.getAttribute('data-store-id');
        const formData = new FormData(editStoreForm);
        
        formData.append('id', storeId);

        try {
            const response = await fetch(UtilApiURLs.EditStoreURL, {
                method: 'PUT',
                body: formData,
            });

            const result = await response.json();
            if (response.ok) {
                Swal.fire({
                    icon: 'success',
                    title: 'Infos mises à jour',
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
            editStoreButton.disabled = false;
            editStoreText.classList.remove('d-none');
            editLoadingText.classList.add('d-none');
        }
    });
});
