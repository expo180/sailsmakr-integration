document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('form[id^="editForm"]').forEach(form => {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
  
            const formId = form.id.replace('editForm', '');
            const formData = new FormData(form);
  
            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: formData,
                });
  
                const result = await response.json();
                if (result.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Succès',
                        text: result.message,
                        confirmButtonText: 'OK'
                    }).then(() => {
                        location.reload();
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: result.message,
                    });
                }
            } catch (error) {
                console.error('Error:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: "{{ _('Une erreur s'est produite') }}",
                });
            }
        });
    });
});
