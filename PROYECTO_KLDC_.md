## Métrica KLoC del directorio `Backend` (excluyendo CSV)
## Resumen de exclusiones y totales resultantes

Listado de items que podemos excluir (valores tomados de `.VSCodeCounter/2025-11-15_09-50-29/results.txt`):

- Líneas totales (base): **546,097**
- CSV (todos los CSV del `Backend`): **171,983**
- Tokenizer principal: `Backend/codigo/code_detection-model-complete/tokenizer.json` = **250,371**
- Segundo tokenizer: `Backend/texto/modelo_deteccion_ia_N/tokenizer.json` = **119,711**
- Total JSON (todos los archivos JSON): **370,320**

Resultados después de aplicar exclusiones (líneas y KLoC):

1) Sin exclusiones (base): 546,097 líneas → **546.097 KLoC**

2) Excluyendo sólo CSV:
	- Cálculo: 546,097 − 171,983 = **374,114** líneas → **374.114 KLoC**

3) Excluyendo sólo el tokenizer principal (`code_detection-model-complete/tokenizer.json`):
	- Cálculo: 546,097 − 250,371 = **295,726** líneas → **295.726 KLoC**

4) Excluyendo sólo el tokenizer de `texto` (`modelo_deteccion_ia_N/tokenizer.json`):
	- Cálculo: 546,097 − 119,711 = **426,386** líneas → **426.386 KLoC**



5) Excluyendo CSV + ambos tokenizers (171,983 + 370,082 = 542,065):
	- Cálculo: 546,097 − 542,065 = **4,032** líneas → **4.032 KLoC**

- KLoC oficial: **4.032 KLoC**

Fuente: `.VSCodeCounter/2025-11-15_09-50-29/results.txt` (secciones "Languages" y listado de archivos).


## ¿Qué es un "tokenizer" y por qué lo excluimos?

- Definición breve: un *tokenizer* es un componente de un modelo de lenguaje que transforma texto en "tokens" (números o subunidades) que el modelo puede procesar. Los archivos `tokenizer.json` suelen contener vocabularios, reglas y tablas grandes necesarias para la tokenización.
- Naturaleza del archivo: en la práctica los tokenizers son artefactos de datos (vocabularios/índices) con mucho contenido repetitivo y tamaño grande. No son código fuente ejecutable (p. ej. Python, JS) sino datos que el modelo utiliza.
- Razón para excluirlo: los tokenizers inflan enormemente el conteo de líneas (por ejemplo, >250k líneas). Para medir KLoC —que pretende reflejar el tamaño del código fuente— es razonable excluir estos artefactos, porque distorsionan la métrica y no representan trabajo de desarrollo mantenible.
- Qué hacer con ellos: si necesitan versionarse, usamos soluciones específicas en lugar del repositorio principal (Git LFS, almacenamiento en la nube o artefactos de release). Esto mantiene el repositorio ligero y la métrica KLoC representativa.




## Métrica KLoC del directorio `Frontend` 
- Líneas totales (Frontend): **9,949**
- Cálculo: 9,949 / 1,000 = **9.949 KLoC**
- Resultado: **aproximadamente 9.949 KLoC**

Fuente: `.VSCodeCounter/2025-11-15_10-09-56/results.txt` (secciones "Languages" y listado de archivos).

## TOTAL DE AMBOS DIRECTORIOS : 

- Métrica oficial Backend (seleccionada): **4,032** líneas → **4.032 KLoC**
- Métrica Frontend: **9,949** líneas → **9.949 KLoC**
- Líneas combinadas: 4,032 + 9,949 = **13,981** líneas
- KLoC combinado: 13,981 / 1,000 = **13.981 KLoC**


