import UtilApiURLs from '../../../../_globals/UtilApiUrls.js';
const URL = UtilApiURLs.ManageNoteURL;


document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('.edit-note');

    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            const noteId = this.dataset.noteId;
            openEditModal(noteId);
        });
    });

    function openEditModal(noteId) {
        fetch(`${URL}${noteId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    populateEditForm(data.note);
                    $('#EditNoteModal').modal('show');
                } else {
                    showError('Une erreur s\'est produite lors de la récupération des détails de la note.');
                }
            })
            .catch(error => {
                console.error('Error fetching note details:', error);
                showError('Une erreur s\'est produite lors de la récupération des détails de la note.');
            });
    }

    function populateEditForm(note) {
        if (!note) {
            console.error('No note data provided');
            return;
        }
        document.querySelector('#EditNoteTitle').value = note.title || '';
        document.querySelector('#EditNoteContent').value = note.content || '';
        document.querySelector('#EditNoteNature').value = note.nature || 'Warning';
        document.querySelector('#editNoteForm').action = `${URL}${note.id}`;
    }

    document.querySelector('#editNoteButton').addEventListener('click', function (event) {
        event.preventDefault();
        handleFormSubmission();
    });

    function handleFormSubmission() {
        const editNoteForm = document.querySelector('#editNoteForm');

        if (!isFormValid()) {
            return;
        }

        disableButton();

        const formData = {
            title: document.querySelector('#EditNoteTitle').value,
            content: document.querySelector('#EditNoteContent').value,
            nature: document.querySelector('#EditNoteNature').value
        };

        fetch(editNoteForm.action, {
            method: 'PUT',
            body: JSON.stringify(formData),
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    title: 'Succès!',
                    text: 'La note a été mise à jour avec succès.',
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then(() => {
                    location.reload();
                });
            } else {
                showError('Une erreur s\'est produite lors de la mise à jour de la note.');
                enableButton();
            }
        })
        .catch(error => {
            console.error('Error updating note:', error);
            showError('Une erreur s\'est produite lors de la mise à jour de la note.');
            enableButton();
        });
    }

    function isFormValid() {
        let isValid = true;

        const title = document.querySelector('#EditNoteTitle');
        const content = document.querySelector('#EditNoteContent');

        if (title.value.trim() === '') {
            document.querySelector('#EditNoteTitleError').style.display = 'block';
            isValid = false;
        } else {
            document.querySelector('#EditNoteTitleError').style.display = 'none';
        }

        if (content.value.trim() === '') {
            document.querySelector('#EditNoteContentError').style.display = 'block';
            isValid = false;
        } else {
            document.querySelector('#EditNoteContentError').style.display = 'none';
        }

        return isValid;
    }

    function disableButton() {
        const button = document.querySelector('#editNoteButton');
        button.disabled = true;
        document.querySelector('#EditNoteText').style.display = 'none';
        document.querySelector('#EditLoadingText').style.display = 'inline-block';
        document.querySelector('.spinner-border').style.display = 'inline-block';
    }

    function enableButton() {
        const button = document.querySelector('#editNoteButton');
        button.disabled = false;
        document.querySelector('#EditNoteText').style.display = 'inline-block';
        document.querySelector('#EditLoadingText').style.display = 'none';
        document.querySelector('.spinner-border').style.display = 'none';
    }

    function showError(message) {
        Swal.fire({
            title: 'Erreur!',
            text: message,
            icon: 'error',
            confirmButtonText: 'OK'
        });
    }
});
