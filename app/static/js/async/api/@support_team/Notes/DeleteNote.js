import UtilApiURLs from '../../../../_globals/UtilApiUrls.js';
const URL = UtilApiURLs.ManageNoteURL;

document.addEventListener('DOMContentLoaded', function () {
    const deleteNoteButtons = document.querySelectorAll('.delete-note');

    deleteNoteButtons.forEach(button => {
        button.addEventListener('click', function () {
            const noteId = this.dataset.noteId;
            handleNoteDeletion(noteId);
        });
    });

    function handleNoteDeletion(noteId) {
        Swal.fire({
            title: 'Êtes-vous sûr ?',
            text: 'Vous ne pourrez pas récupérer cette note !',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Supprimer',
            cancelButtonText: 'Annuler',
            dangerMode: true,
        }).then((result) => {
            if (result.isConfirmed) {
                fetch(`${URL}${noteId}`, {
                    method: 'DELETE',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire('Supprimée !', 'Votre note a été supprimée.', 'success')
                            .then(() => location.reload());
                    } else {
                        Swal.fire('Erreur', 'Une erreur est survenue lors de la suppression de la note.', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error deleting note:', error);
                    Swal.fire('Erreur', 'Une erreur est survenue lors de la suppression de la note.', 'error');
                });
            }
        });
    }
});
