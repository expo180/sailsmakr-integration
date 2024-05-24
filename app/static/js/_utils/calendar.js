import UtilApiUrls from '../_globals/UtilApiUrls.js';

document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    locale: 'fr',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    selectable: true,
    editable: true,
    events: UtilApiUrls.GetEventsApiURL,
    dateClick: function(info) {
      document.getElementById('eventForm').reset();
      document.getElementById('start_from').value = info.dateStr + 'T00:00';
      document.getElementById('end_at').value = info.dateStr + 'T23:59';
      var myModal = new bootstrap.Modal(document.getElementById('eventModal'), {});
      myModal.show();
    }
  });
  calendar.render();
});