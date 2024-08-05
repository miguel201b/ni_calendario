from flask import Flask, send_file, request, jsonify, render_template
from flask_cors import CORS
import os
from psycopg2 import sql
from datetime import datetime
import pytz
from funciones import obtener_horas, insertarEstadisticas
from unidecode import unidecode

app = Flask(__name__)
CORS(app)  # Habilitar CORS

# Define el directorio donde se almacenan tus archivos PDF
PDF_DIRECTORY = 'Resources'

@app.route('/get_calendar', methods=['GET'])
def get_calendar():
    letter = request.args.get('letter')
    shift = request.args.get('shift')
    apellido = request.args.get('surname')

    if not letter or not shift:
        return jsonify({"error": "Please provide both 'letter' and 'shift' parameters"}), 400
    
    apellido = unidecode(apellido).upper()
    insertarEstadisticas(letter,apellido)

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
    app.run(host='0.0.0.0', port=8000)
