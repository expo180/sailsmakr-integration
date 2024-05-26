import UtilApiURLs from "../../../../_globals/UtilApiUrls.js";

const URL = UtilApiURLs.DeletePurchaseRequestURL;

document.addEventListener('DOMContentLoaded', function() {
    const deleteRequestLinks = document.querySelectorAll('.delete-request');
  
    deleteRequestLinks.forEach(link => {
      link.addEventListener('click', function(event) {
        event.preventDefault();
        const id = this.getAttribute('data-id');
        Swal.fire({
          title: 'Êtes-vous sûr de vouloir supprimer cette demande ?',
          text: 'Cette action est irréversible!',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Oui, supprimer!',
          cancelButtonText: 'Annuler'
        }).then((result) => {
          if (result.isConfirmed) {
            fetch(`${URL}${id}`, {
              method: 'DELETE',
              headers: {
                'Content-Type': 'application/json'
              }
            })
            .then(response => {
              if (response.ok) {
                Swal.fire(
                  'Supprimé!',
                  'Votre demande a été supprimée.',
                  'success'
                ).then(() => {
                  location.reload();
                });
              } else {
                Swal.fire(
                  'Erreur!',
                  'Erreur lors de la suppression de la demande.',
                  'error'
                );
              }
            });
          }
        });
      });
    });
});
