document.addEventListener('DOMContentLoaded', function () {
    const addTaskButton = document.querySelector('#addTaskButton');
    const taskForm = document.querySelector('#taskForm');

    addTaskButton.addEventListener('click', function (event) {
        event.preventDefault();
        handleFormSubmission();
    });

    function handleFormSubmission() {
        if (!isFormValid()) {
            return;
        }

        disableButton();

        const formData = new FormData(taskForm);

        fetch(taskForm.action, {
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
                    icon: 'success',
                    title: 'Succès',
                    text: 'La tâche a été ajoutée avec succès.',
                    confirmButtonText: 'OK'
                }).then(() => {
                    location.reload();
                });
            } else {
                showError('Une erreur est survenue lors de l\'ajout de la tâche.');
                enableButton();
            }
        })
        .catch(error => {
            showError('Une erreur est survenue lors de l\'ajout de la tâche.');
            enableButton();
        });
    }

    function isFormValid() {
        let isValid = true;

        const title = document.querySelector('#TaskTitle');
        const description = document.querySelector('#TaskDescription');
        const assignedTo = document.querySelector('#AssignedTo');

        if (title.value.trim() === '') {
            document.querySelector('#TaskTitleError').style.display = 'block';
            isValid = false;
        } else {
            document.querySelector('#TaskTitleError').style.display = 'none';
        }

        if (description.value.trim() === '') {
            document.querySelector('#TaskDescriptionError').style.display = 'block';
            isValid = false;
        } else {
            document.querySelector('#TaskDescriptionError').style.display = 'none';
        }

        if (assignedTo.value === '0') {
            document.querySelector('#TaskAssingmentError').style.display = 'block';
            isValid = false;
        } else {
            document.querySelector('#TaskAssingmentError').style.display = 'none';
        }

        return isValid;
    }

    function disableButton() {
        addTaskButton.disabled = true;
        document.querySelector('#AddTaskText').style.display = 'none';
        document.querySelector('#LoadingText').style.display = 'inline-block';
        document.querySelector('.spinner-border').style.display = 'inline-block';
        document.querySelector('#addTaskButton i').style.display = 'none';
    }

    function enableButton() {
        addTaskButton.disabled = false;
        document.querySelector('#AddTaskText').style.display = 'inline-block';
        document.querySelector('#LoadingText').style.display = 'none';
        document.querySelector('.spinner-border').style.display = 'none';
        document.querySelector('#addTaskButton i').style.display = 'inline-block';
    }

    function showError(message) {
        Swal.fire({
            icon: 'error',
            title: 'Erreur',
            text: message,
            confirmButtonText: 'OK'
        });
    }
});
