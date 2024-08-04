from flask import Flask, send_file, request, jsonify, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Habilitar CORS

# Define el directorio donde se almacenan tus archivos PDF
PDF_DIRECTORY = 'Resources'

def obtener_horas(inicial, turno):
    inicial = inicial.upper()

    if 'A' <= inicial <= 'E':
        horaBienvenida = "10:00 hrs."
        horaCharla = "9:00 hrs."
    elif 'F' <= inicial <= 'L':
        horaBienvenida = "12:00 hrs."
        horaCharla = "11:00 hrs."
    elif 'M' <= inicial <= 'Q':
        horaBienvenida = "14:00 hrs."
        horaCharla = "15:00 hrs."
    elif 'R' <= inicial <= 'Z':
        horaBienvenida = "16:00 hrs."
        horaCharla = "17:00 hrs."

    EI14, EI15, EI16, EI14hora, EI15hora, EI16hora = "", "", "", "", "", ""
    if turno == "Matutino":
        if 'A' <= inicial <= 'C':
            EI14, EI14hora = "Inscripción", "09:30"
        elif 'D' <= inicial <= 'G':
            EI14, EI14hora = "Inscripción", "11:30"
        elif 'H' <= inicial <= 'L':
            EI15, EI15hora = "Inscripción", "09:30"
        elif 'M' <= inicial <= 'O':
            EI15, EI15hora = "Inscripción", "11:30"
        elif 'P' <= inicial <= 'R':
            EI16, EI16hora = "Inscripción", "09:30"
        elif 'S' <= inicial <= 'Z':
            EI16, EI16hora = "Inscripción", "11:30"
    elif turno == "Vespertino":
        if 'A' <= inicial <= 'C':
            EI14, EI14hora = "Inscripción", "15:00"
        elif 'D' <= inicial <= 'G':
            EI14, EI14hora = "Inscripción", "17:00"
        elif 'H' <= inicial <= 'L':
            EI15, EI15hora = "Inscripción", "15:00"
        elif 'M' <= inicial <= 'O':
            EI15, EI15hora = "Inscripción", "17:00"
        elif 'P' <= inicial <= 'R':
            EI16, EI16hora = "Inscripción", "15:00"
        elif 'S' <= inicial <= 'Z':
            EI16, EI16hora = "Inscripción", "17:00"

    if 'P' <= inicial <= 'R':
        EI14, EI14hora = "EMA", "08:00"
    elif 'S' <= inicial <= 'T':
        EI14, EI14hora = "EMA", "11:00"
    elif 'U' <= inicial <= 'Z':
        EI14, EI14hora = "EMA", "14:00"
    elif 'A' <= inicial <= 'B':
        EI15, EI15hora = "EMA", "08:00"
    elif 'C' <= inicial <= 'D':
        EI15, EI15hora = "EMA", "11:00"
    elif 'E' <= inicial <= 'G':
        EI15, EI15hora = "EMA", "14:00"
    elif 'H' <= inicial <= 'L':
        EI16, EI16hora = "EMA", "08:00"
    elif inicial == 'M':
        EI16, EI16hora = "EMA", "11:00"
    elif inicial == 'N' or inicial == 'O':
        EI16, EI16hora = "EMA", "14:00"

    return {
        'horaBienvenida': horaBienvenida,
        'horaCharla': horaCharla,
        'EI14': EI14,
        'EI14hora': EI14hora,
        'EI15': EI15,
        'EI15hora': EI15hora,
        'EI16': EI16,
        'EI16hora': EI16hora
    }

@app.route('/get_calendar', methods=['GET'])
def get_calendar():
    letter = request.args.get('letter')
    shift = request.args.get('shift')

    if not letter or not shift:
        return jsonify({"error": "Please provide both 'letter' and 'shift' parameters"}), 400

    # Construir el nombre del archivo basado en la letra y el turno
    filename = f"calendario_{letter.upper()}_{shift.capitalize()}.pdf"

    # Verificar si el archivo existe
    file_path = os.path.join(PDF_DIRECTORY, filename)
    if not os.path.isfile(file_path):
        return jsonify({"error": "File not found"}), 404

    # Enviar el archivo con el nombre 'calendario.pdf'
    return send_file(file_path, as_attachment=True, download_name='calendario.pdf')

@app.route('/get_calendar_info', methods=['GET'])
def get_calendar_info():
    letter = request.args.get('letter', '')
    shift = request.args.get('shift', '')
    if not letter or not shift:
        return jsonify({'error': 'Missing parameters'}), 400
    
    info = obtener_horas(letter, shift)
    calendar_html = render_template('calendar_template.html', info=info)
    return jsonify({'calendar_html': calendar_html})

@app.route('/')
def main():
    return render_template('api.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
