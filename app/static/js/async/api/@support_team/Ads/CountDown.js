document.addEventListener('DOMContentLoaded', function() {
    const viewDetailButtons = document.querySelectorAll('.view-detail-btn');

    viewDetailButtons.forEach(button => {
        button.addEventListener('click', function() {
            const adId = button.dataset.adId;
            const adModal = document.querySelector(`#viewAdModal${adId}`);

            const modal = new bootstrap.Modal(adModal);
            modal.show();

            const adEndAt = new Date(button.dataset.adEndAt);
            const countdownElement = adModal.querySelector('#countdown');

            setInterval(() => {
                const now = new Date();
                const timeDifference = adEndAt - now;

                const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
                const hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);

                countdownElement.value = `${days}d ${hours}h ${minutes}m ${seconds}s`;
            }, 1000);
        });
    });
});
