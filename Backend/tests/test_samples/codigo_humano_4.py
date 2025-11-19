# script para leer archivo csv y hacer algunos calculos
import csv

file = "data.csv"

try:
    with open(file, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
        
    # sacar el header
    header = data[0]
    rows = data[1:]
    
    # calcular el promedio de la columna 2 (asumiendo que son numeros)
    col2_values = [float(row[1]) for row in rows if len(row) > 1]
    avg = sum(col2_values) / len(col2_values)
    print(f"promedio: {avg}")
    
    # contar cuantos son mayores a 50
    count = 0
    for val in col2_values:
        if val > 50:
            count += 1
    
    print(f"valores > 50: {count}")
    
except FileNotFoundError:
    print("no se encontro el archivo")
except Exception as e:
    print(f"error: {e}")
