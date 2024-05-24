import RedirectUrls from '../../../../_globals/RedirectUrls.js';

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const employeeFirstName = document.getElementById('employeeFirstName').value;
        const employeeLastName = document.getElementById('employeeLastName').value;
        const employeeJobTitle = document.getElementById('employeeJobTitle').value;
        const employeeIdentifier = document.getElementById('employeeIdentifier').value;
        const url = window.location.pathname;

        fetch(form.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token() }}'
            },
            body: JSON.stringify({
                employee_first_name: employeeFirstName,
                employee_last_name: employeeLastName,
                employee_job_title: employeeJobTitle,
                employee_identifier: employeeIdentifier
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire(
                    'Succès',
                    data.message,
                    'success'
                ).then(() => {
                    window.location.href = RedirectUrls.EmployeeEditInfoSuccess;
                });
            } else {
                Swal.fire(
                    'Erreur',
                    data.message,
                    'error'
                );
            }
        })
        .catch(error => {
            Swal.fire(
                'Erreur',
                'Une erreur est survenue lors de la mise à jour.',
                'error'
            );
        });
    });
});
