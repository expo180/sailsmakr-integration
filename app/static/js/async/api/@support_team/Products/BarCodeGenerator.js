import UtilApiURLs from "../../../../_globals/UtilApiUrls.js";

document.addEventListener('DOMContentLoaded', () => {
    const downloadButtons = document.querySelectorAll('.download-barcode-btn');
    
    downloadButtons.forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.getAttribute('data-product-id');
            fetch(`${UtilApiURLs.GetProductBarCodeURL}/${productId}`)
                .then(response => response.blob())
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = `${productId}_barcode.pdf`;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                })
                .catch(error => console.error('Error downloading the barcode:', error));
        });
    });
});
