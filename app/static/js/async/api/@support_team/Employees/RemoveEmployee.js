import RedirectUrls from '../../../../_globals/RedirectUrls.js';
import UtilApiURLs from '../../../../_globals/UtilApiUrls.js';

const URL = UtilApiURLs.DeleteEmployeeURL

document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.dropdown-item.text-danger');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const employeeId = this.getAttribute('data-employee-id');

            Swal.fire({
                title: 'Êtes-vous sûr de vouloir supprimer cet employé?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Oui, supprimer!',
                cancelButtonText: 'Annuler'
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`${URL}${employeeId}`, {
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
                                'L\'employé a été retiré de la base de données',
                                'success'
                            ).then(() => {
                                window.location.href = RedirectUrls.EmployeeEditInfoSuccess;
                            });
                        } else {
                            Swal.fire(
                                'Erreur!',
                                'Une erreur est survenue.',
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
