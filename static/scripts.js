class CalendarManager {
    constructor() {
        this.form = document.getElementById('calendarForm');
        this.surnameField = document.getElementById('surname');
        this.shiftField = document.getElementById('shift');
        this.surnameError = document.getElementById('errorApellido');
        this.downloadButton = document.getElementById('downloadButton');
        this.calendarContainer = document.getElementById('calendarContainer');
        this.calendarContent = document.getElementById('calendarContent');

        this.initEventListeners();
    }

    initEventListeners() {
        this.form.addEventListener('submit', (event) => this.handleSubmit(event));
        this.downloadButton.addEventListener('click', (event) => this.handleDownload(event));
    }

    handleSubmit(event) {
        event.preventDefault();
        this.surnameError.style.visibility = 'hidden'; 

        let surname = this.surnameField.value.trim().toUpperCase();
        let shift = this.shiftField.value;

        if (surname === '') {
            this.surnameError.style.visibility = 'visible';
            return;
        }

        let initial = surname.charAt(0);
        this.fetchCalendarInfo(initial, shift);
        this.prepareDownloadLink(initial, shift);
    }

    fetchCalendarInfo(initial, shift) {
        fetch(`/get_calendar_info?letter=${initial}&shift=${shift}`)
            .then(response => response.json())
            .then(data => this.renderCalendar(data))
            .catch(error => console.error('Error al obtener la información del calendario:', error));
    }

    renderCalendar(data) {
        this.calendarContent.innerHTML = data.calendar_html;
        this.calendarContainer.style.display = 'block';
    }

    prepareDownloadLink(initial, shift) {
        fetch(`/get_calendar?letter=${initial}&shift=${shift}`)
            .then(response => response.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                this.downloadButton.href = url;
                this.downloadButton.style.display = 'block';
            })
            .catch(error => console.error('Error al preparar el enlace de descarga:', error));
    }

    handleDownload(event) {
        if (this.downloadButton.href === '#') {
            event.preventDefault();
            alert('El enlace de descarga no está disponible. Por favor, obtén el calendario primero.');
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new CalendarManager();
});
