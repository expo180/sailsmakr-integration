import UtilApiURLs from '../../../../_globals/UtilApiUrls.js'
const URL = UtilApiURLs.ManageTaskURL


document.addEventListener('DOMContentLoaded', function () {
    const deleteTaskButtons = document.querySelectorAll('.delete-task');

    deleteTaskButtons.forEach(button => {
        button.addEventListener('click', function () {
            const taskId = this.dataset.taskId;
            handleTaskDeletion(taskId);
        });
    });

    function handleTaskDeletion(taskId) {
        Swal.fire({
            title: 'Êtes-vous sûr ?',
            text: 'Vous ne pourrez pas récupérer cette tâche !',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Supprimer',
            cancelButtonText: 'Annuler',
            dangerMode: true,
        }).then((result) => {
            if (result.isConfirmed) {
                fetch(`${URL}${taskId}`, {
                    method: 'DELETE',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire('Supprimée !', 'Votre tâche a été supprimée.', 'success')
                            .then(() => location.reload());
                    } else {
                        Swal.fire('Erreur', 'Une erreur est survenue lors de la suppression de la tâche.', 'error');
                    }
                })
                .catch(error => {
                    Swal.fire('Erreur', 'Une erreur est survenue lors de la suppression de la tâche.', 'error');
                });
            }
        });
    }
});
