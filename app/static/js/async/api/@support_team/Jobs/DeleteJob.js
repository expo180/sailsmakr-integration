document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-job');

    deleteButtons.forEach(button => {
      button.addEventListener('click', function(event) {
        event.preventDefault();
        const url = this.getAttribute('data-url');

        Swal.fire({
          title: 'Etes vous sûre de vouloir supprimer?',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Oui, supprimer!',
          cancelButtonText: 'Annuler'
        }).then((result) => {
          if (result.isConfirmed) {
            fetch(url, {
              method: 'DELETE',
              headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token() }}'
              }
            })
            .then(response => response.json())
            .then(data => {
              if (data.success) {
                Swal.fire(
                  'Supprimé!',
                  'L\'offre a été supprimée.',
                  'success'
                ).then(() => {
                  window.location.reload();
                });
              } else {
                Swal.fire(
                  'Erreur!',
                  'Une erreur est survenue lors de la suppression.',
                  'error'
                );
              }
            })
            .catch(error => {
              Swal.fire(
                'Erreur!',
                'Une erreur est survenue.',
                'error'
              );
            });
          }
        });
      });
    });
  });