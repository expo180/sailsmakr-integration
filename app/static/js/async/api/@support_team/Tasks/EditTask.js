import UtilApiURLs from '../../../../_globals/UtilApiUrls.js'
const URL = UtilApiURLs.ManageTaskURL;

document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('.edit-task');
    const deleteTaskButtons = document.querySelectorAll('.delete-task');

    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            const taskId = this.dataset.taskId;
            openEditModal(taskId);
        });
    });

    deleteTaskButtons.forEach(button => {
        button.addEventListener('click', function () {
            const taskId = this.dataset.taskId;
            handleTaskDeletion(taskId);
        });
    });

    function openEditModal(taskId) {
        fetch(`${URL}${taskId}`)
            .then(response => response.json())
            .then(data => {
                if (data.success == true) {
                    populateEditForm(data.task);
                    $('#EditTaskModal').modal('show');
                } else {
                    showError('Une erreur s\'est produite lors de la récupération des détails de la tâche.');
                }
            })
            .catch(error => {
                console.error('Error fetching task details:', error);  // Log error details
                showError('Une erreur s\'est produite lors de la récupération des détails de la tâche.');
            });
    }

    function populateEditForm(task) {
        document.querySelector('#EditTaskTitle').value = task.title;
        document.querySelector('#EditTaskDescription').value = task.description;
        document.querySelector('#EditAssignedTo').value = task.assigned_to;
        document.querySelector('#editTaskForm').action = `${URL}${task.id}`;
    }

    document.querySelector('#editTaskButton').addEventListener('click', function (event) {
        event.preventDefault();
        handleFormSubmission();
    });

    function handleFormSubmission() {
        const editTaskForm = document.querySelector('#editTaskForm');

        if (!isFormValid()) {
            return;
        }

        disableButton();

        const formData = {
            title: document.querySelector('#EditTaskTitle').value,
            description: document.querySelector('#EditTaskDescription').value,
            assigned_to: document.querySelector('#EditAssignedTo').value
        };


        fetch(editTaskForm.action, {
            method: 'PUT',
            body: JSON.stringify(formData),
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })

        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    title: 'Succès!',
                    text: 'La tâche a été mise à jour avec succès.',
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then(() => {
                    location.reload();
                });
            } else {
                showError('Une erreur s\'est produite lors de la mise à jour de la tâche.');
                enableButton();
            }
        })
        .catch(error => {
            console.error('Error updating task:', error);
            showError('Une erreur s\'est produite lors de la mise à jour de la tâche.');
            enableButton();
        });
    }

    function isFormValid() {
        let isValid = true;

        const title = document.querySelector('#EditTaskTitle');
        const description = document.querySelector('#EditTaskDescription');
        const assignedTo = document.querySelector('#EditAssignedTo');

        if (title.value.trim() === '') {
            document.querySelector('#EditTaskTitleError').style.display = 'block';
            isValid = false;
        } else {
            document.querySelector('#EditTaskTitleError').style.display = 'none';
        }

        if (description.value.trim() === '') {
            document.querySelector('#EditTaskDescriptionError').style.display = 'block';
            isValid = false;
        } else {
            document.querySelector('#EditTaskDescriptionError').style.display = 'none';
        }

        if (assignedTo.value === '0') {
            document.querySelector('#EditTaskAssignmentError').style.display = 'block';
            isValid = false;
        } else {
            document.querySelector('#EditTaskAssignmentError').style.display = 'none';
        }

        return isValid;
    }

    function disableButton() {
        const button = document.querySelector('#editTaskButton');
        button.disabled = true;
        document.querySelector('#EditTaskText').style.display = 'none';
        document.querySelector('#EditLoadingText').style.display = 'inline-block';
        document.querySelector('.spinner-border').style.display = 'inline-block';
        document.querySelector('#editTaskButton i').style.display = 'none';
    }

    function enableButton() {
        const button = document.querySelector('#editTaskButton');
        button.disabled = false;
        document.querySelector('#EditTaskText').style.display = 'inline-block';
        document.querySelector('#EditLoadingText').style.display = 'none';
        document.querySelector('.spinner-border').style.display = 'none';
        document.querySelector('#editTaskButton i').style.display = 'inline-block';
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
