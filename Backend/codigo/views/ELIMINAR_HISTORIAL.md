# 🗑️ Funcionalidad de Eliminación de Historial

## 📋 Resumen

Se han agregado dos nuevas funcionalidades para eliminar análisis del historial:

1. **Eliminar análisis individual**: Permite eliminar un análisis específico
2. **Eliminar todo el historial**: Permite eliminar todos los análisis del usuario

## 🔐 Seguridad

- **Usuarios autenticados**: Solo pueden eliminar sus propios análisis
- **Staff/Admin**: Pueden eliminar cualquier análisis y todo el historial (con `todos=true`)
- **Usuarios anónimos**: Solo pueden eliminar análisis sin usuario asignado

## 📡 Endpoints

### 1. Eliminar Análisis Individual

**Endpoint**: `DELETE /api/codigo/analisis/<id>/eliminar/`

**Descripción**: Elimina un análisis específico por su ID.

**Permisos**:
- Usuario autenticado: Solo sus propios análisis
- Staff: Cualquier análisis
- Anónimo: Solo análisis sin usuario

**Ejemplo de uso**:
```bash
# Eliminar análisis con ID 5
curl -X DELETE http://localhost:8000/api/codigo/analisis/5/eliminar/ \
  -H "Authorization: Bearer <token>"
```

**Respuesta exitosa** (200 OK):
```json
{
  "mensaje": "Análisis 'archivo.py' eliminado correctamente",
  "id_eliminado": 5
}
```

**Respuesta de error** (404 Not Found):
```json
{
  "error": "Análisis no encontrado o no tienes permiso para eliminarlo"
}
```

---

### 2. Eliminar Todo el Historial

**Endpoint**: `DELETE /api/codigo/historial/eliminar/`

**Descripción**: Elimina todos los análisis del usuario autenticado.

**Permisos**:
- Usuario autenticado: Elimina solo sus propios análisis
- Staff: Puede eliminar todo el historial con `?todos=true`
- Anónimo: Elimina solo análisis sin usuario

**Parámetros de consulta**:
- `todos=true`: Solo para staff. Elimina TODO el historial del sistema

**Ejemplo de uso**:

```bash
# Eliminar historial del usuario actual
curl -X DELETE http://localhost:8000/api/codigo/historial/eliminar/ \
  -H "Authorization: Bearer <token>"

# Staff: Eliminar TODO el historial del sistema
curl -X DELETE "http://localhost:8000/api/codigo/historial/eliminar/?todos=true" \
  -H "Authorization: Bearer <admin_token>"
```

**Respuesta exitosa** (200 OK):
```json
{
  "mensaje": "Se eliminaron 15 análisis de tu historial",
  "total_eliminados": 15
}
```

**Respuesta para staff eliminando todo**:
```json
{
  "mensaje": "Se eliminaron 150 análisis del historial completo",
  "total_eliminados": 150
}
```

---

## ⚙️ Funcionalidades Técnicas

### Eliminación de Archivos Físicos

- Los archivos físicos se eliminan automáticamente antes de eliminar los registros de la base de datos
- Si hay un error al eliminar un archivo físico, se registra un warning pero el proceso continúa
- Los registros de la base de datos se eliminan incluso si falla la eliminación del archivo

### Logging

- Todas las eliminaciones se registran en el log del sistema
- Incluye información sobre quién eliminó qué y cuántos registros

### Manejo de Errores

- Validación de IDs (deben ser números)
- Verificación de permisos antes de eliminar
- Manejo robusto de excepciones con mensajes claros

---

## 📝 Notas Importantes

1. **Operación irreversible**: La eliminación es permanente. No hay recuperación automática.

2. **Eliminación en cascada**: Al eliminar un análisis, también se elimina:
   - El archivo físico del código
   - Todos los datos asociados (análisis IA, métricas, etc.)

3. **Performance**: Para historiales muy grandes, la eliminación puede tardar unos segundos.

4. **Staff con cuidado**: El parámetro `todos=true` elimina TODO el historial del sistema. Usar con precaución.

---

## 🧪 Ejemplos de Uso con Python (requests)

```python
import requests

# Configuración
BASE_URL = "http://localhost:8000/api/codigo"
TOKEN = "tu_token_jwt"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

# Eliminar un análisis específico
response = requests.delete(
    f"{BASE_URL}/analisis/5/eliminar/",
    headers=headers
)
print(response.json())

# Eliminar todo el historial del usuario
response = requests.delete(
    f"{BASE_URL}/historial/eliminar/",
    headers=headers
)
print(response.json())

# Staff: Eliminar todo el historial del sistema
response = requests.delete(
    f"{BASE_URL}/historial/eliminar/?todos=true",
    headers=headers
)
print(response.json())
```

---

## ✅ Tests Recomendados

1. Eliminar análisis propio (usuario normal)
2. Intentar eliminar análisis de otro usuario (debe fallar)
3. Staff eliminando cualquier análisis
4. Eliminar historial completo del usuario
5. Staff eliminando todo el historial del sistema
6. Verificar que los archivos físicos se eliminen correctamente

