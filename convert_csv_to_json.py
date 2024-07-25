import csv
import json
from datetime import datetime
import os

def convert_csv_to_json():
    """Convierte el archivo CSV a un archivo JSON completo."""
    csv_file_path = "data/Cerrados Tickets - 20240725.csv"
    json_file_path = "data/tickets_data.json"
    
    tickets_data = []

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ticket = {}
            for key, value in row.items():
                # Convertir fechas a formato ISO
                if 'Fecha' in key and value:
                    try:
                        date = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                        ticket[key] = date.isoformat()
                    except ValueError:
                        ticket[key] = value
                # Convertir valores numéricos
                elif key in ['Número de Ticket', 'Cuenta de hilos', 'Reabrir contador', 'Recuento de datos adjuntos', 'Task Count']:
                    try:
                        ticket[key] = int(value) if value else None
                    except ValueError:
                        ticket[key] = value
                # Convertir valores booleanos
                elif key in ['Atrasado', 'Merged', 'Linked', 'Respondió']:
                    ticket[key] = value.lower() in ['yes', 'sí', 'true']
                # Mantener el resto de campos como están
                else:
                    ticket[key] = value

            tickets_data.append(ticket)

    # Crear el objeto JSON final
    json_data = {
        "last_updated": datetime.now().isoformat(),
        "total_tickets": len(tickets_data),
        "tickets": tickets_data
    }

    # Guardar el JSON
    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(json_data, jsonfile, ensure_ascii=False, indent=2)

    print(f"Archivo JSON creado con éxito: {json_file_path}")

if __name__ == "__main__":
    convert_csv_to_json()
