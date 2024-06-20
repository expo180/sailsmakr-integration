import UtilApiURLs from "../../../../_globals/UtilApiUrls";

document.getElementById('productForm').addEventListener('submit', function(event) {
    event.preventDefault();

    let formData = new FormData();
    formData.append('title', document.getElementById('NewProductTitle').value);
    formData.append('cost', document.getElementById('NewProductCost').value);
    formData.append('stock', document.getElementById('NewProductStock').value);
    formData.append('provider', document.getElementById('NewProductProvider').value);
    formData.append('provider_location', document.getElementById('NewProductProviderLocation').value);
    formData.append('category', document.getElementById('NewProductCategory').value);
    formData.append('publish', document.getElementById('NewProductPublish').checked);
    formData.append('product_img_url', document.getElementById('product_img_url').files[0]);

    fetch(UtilApiURLs.ManageProductURL, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        Swal.fire({
            icon: 'success',
            title: 'Produit ajouté avec succès!',
            showConfirmButton: false,
            timer: 1500
        });
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire({
            icon: 'error',
            title: 'Erreur!',
            text: 'Une erreur est survenue lors de l\'ajout du produit.',
        });
    });
});
