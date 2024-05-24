import RedirectURLs from "../../../../_globals/RedirectUrls.js";

document.addEventListener('DOMContentLoaded', function () {
    const addNoteButton = document.querySelector('#addNoteButton');
    const noteForm = document.querySelector('#noteForm');

    addNoteButton.addEventListener('click', function (event) {
        event.preventDefault();
        handleFormSubmission();
    });

    function handleFormSubmission() {
        if (!isFormValid()) {
            return;
        }

        disableButton();

        const formData = new FormData(noteForm);

        fetch(noteForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    title: 'Success!',
                    text: 'Note ajoutée avec succès',
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then(() => {
                    location.reload();
                });
            } else {
                showError('Une erreur s\'est produite lors de l\'ajout');
                enableButton();
            }
        })
        .catch(error => {
            showError('Une erreur s\'est produite lors de l\'ajout');
            enableButton();
        });
    }

    function isFormValid() {
        let isValid = true;

        const title = document.querySelector('#NoteTitle');
        const content = document.querySelector('#NoteContent');
        const nature = document.querySelector('#NoteNature');

        if (title.value.trim() === '') {
            document.querySelector('#NoteTitleError').style.display = 'block';
            isValid = false;
        } else {
            document.querySelector('#NoteTitleError').style.display = 'none';
        }

        if (content.value.trim() === '') {
            document.querySelector('#NoteContentError').style.display = 'block';
            isValid = false;
        } else {
            document.querySelector('#NoteContentError').style.display = 'none';
        }

        if (nature.value === '') {
            document.querySelector('#NoteCategoryError').style.display = 'block';
            isValid = false;
        } else {
            document.querySelector('#NoteCategoryError').style.display = 'none';
        }

        return isValid;
    }

    function disableButton() {
        addNoteButton.disabled = true;
        document.querySelector('#PublishText').style.display = 'none';
        document.querySelector('#LoadingText').style.display = 'inline-block';
        document.querySelector('.spinner-border').style.display = 'inline-block';
        document.querySelector('#addNoteButton i').style.display = 'none';
    }

    function enableButton() {
        addNoteButton.disabled = false;
        document.querySelector('#PublishText').style.display = 'inline-block';
        document.querySelector('#LoadingText').style.display = 'none';
        document.querySelector('.spinner-border').style.display = 'none';
        document.querySelector('#addNoteButton i').style.display = 'inline-block';
    }

    function showError(message) {
        Swal.fire({
            title: 'Error!',
            text: message,
            icon: 'error',
            confirmButtonText: 'OK'
        });
    }
});
