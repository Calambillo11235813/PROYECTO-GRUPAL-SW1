"""
Script para dividir el dataset entre traducciones completadas y pendientes
"""
import pandas as pd
import os

# Rutas actualizadas
input_path = r'D:\1.CARRERA UNIVERSITARIA\9. DECIMO SEMESTRE\1.INGIENERIA SOFTWARE 1\3.PROYECTOS\PROYECTO-GRUPAL-SW1\Backend\texto\Dataset_traducidos\dataset_binario_español_completo.csv'
output_folder = r'D:\1.CARRERA UNIVERSITARIA\9. DECIMO SEMESTRE\1.INGIENERIA SOFTWARE 1\3.PROYECTOS\PROYECTO-GRUPAL-SW1\Backend\texto\Dataset_traducidos'
traducido_path = os.path.join(output_folder, 'dataset_parte_traducida.csv')
pendiente_path = os.path.join(output_folder, 'dataset_parte_pendiente.csv')

# La carpeta ya existe, así que no es necesario crearla

# Cargar dataset
print("Cargando dataset...")
df = pd.read_csv(input_path)
total_rows = len(df)
print(f"Total de filas: {total_rows}")

# Identificar filas traducidas vs pendientes
df['necesita_traduccion'] = df['text_es'].apply(lambda x: not isinstance(x, str) or not str(x).strip())
traducidas = df[~df['necesita_traduccion']]
pendientes = df[df['necesita_traduccion']]

# Información sobre el punto de corte específico
punto_corte = 70265
print(f"Punto de corte solicitado: línea {punto_corte}")

# Comprobar si el punto de corte está dentro del rango
if punto_corte > 0 and punto_corte < total_rows:
    # División por índice exacto
    traducidas_por_indice = df.iloc[:punto_corte]
    pendientes_por_indice = df.iloc[punto_corte:]
    print(f"División por índice: {len(traducidas_por_indice)} traducidas, {len(pendientes_por_indice)} pendientes")

# Estadísticas de la división por contenido
print(f"División por contenido: {len(traducidas)} traducidas, {len(pendientes)} pendientes")

# Preguntar qué método usar
print("\n¿Qué método de división prefieres usar?")
print(f"1. División exacta por línea (en el punto {punto_corte})")
print("2. División por contenido (traducido vs vacío)")
opcion = '2'  # Por defecto usamos la opción 2 (más precisa)

# Ejecutar división según la opción
if opcion == '1':
    # Guardar archivos divididos por índice
    traducidas_por_indice.to_csv(traducido_path, index=False)
    pendientes_por_indice.to_csv(pendiente_path, index=False)
    print(f"\nArchivos guardados por división de índice:")
else:
    # Eliminar columna auxiliar antes de guardar
    traducidas = traducidas.drop(columns=['necesita_traduccion'])
    pendientes = pendientes.drop(columns=['necesita_traduccion'])
    
    # Guardar archivos divididos por contenido
    traducidas.to_csv(traducido_path, index=False)
    pendientes.to_csv(pendiente_path, index=False)
    print(f"\nArchivos guardados por división de contenido:")

print(f"- Traducciones completadas: {traducido_path}")
print(f"- Traducciones pendientes: {pendiente_path}")