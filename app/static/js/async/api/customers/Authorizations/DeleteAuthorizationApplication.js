import UtilApiURLs from "../../../../_globals/UtilApiUrls.js";

const URL = UtilApiURLs.DeleteAuthorizationRequestURL

async function deleteRequest(requestId) {
  try {
    const response = await fetch(`${URL}/${requestId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    const result = await response.json();

    if (result.success) {
      Swal.fire({
        icon: 'success',
        title: 'Supprimé!',
        text: result.message,
        showConfirmButton: false,
        timer: 1500,
      }).then(() => {
        location.reload();
      });
    } else {
      Swal.fire({
        icon: 'error',
        title: 'Erreur',
        text: result.message,
      });
    }
  } catch (error) {
    Swal.fire({
      icon: 'error',
      title: 'Erreur',
      text: 'Une erreur s\'est produite lors de la suppression de la demande.',
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.dropdown-item.text-danger').forEach(button => {
    button.addEventListener('click', function () {
      const requestId = this.getAttribute('data-request-id');
      
      Swal.fire({
        title: 'Êtes-vous sûr?',
        text: 'Vous ne pourrez pas revenir en arrière!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Oui, supprimer!',
        cancelButtonText: 'Annuler'
      }).then((result) => {
        if (result.isConfirmed) {
          deleteRequest(requestId);
        }
      });
    });
  });
});