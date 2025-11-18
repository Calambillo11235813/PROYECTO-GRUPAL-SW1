# Mobile App - Detección de IA

Aplicación móvil Flutter para la detección de contenido generado por IA (texto y audio).

## 📱 Estructura del Proyecto

```
mobile_app/
├── lib/
│   ├── models/           # Modelos de datos
│   ├── services/         # Servicios (API, Auth)
│   ├── pages/            # Páginas/Pantallas
│   ├── widgets/          # Widgets reutilizables
│   └── main.dart         # Punto de entrada
```

## 🚀 Funcionalidades Implementadas

- **Autenticación:** Registro, Login, Logout con JWT
- **Análisis de Texto:** Detección de IA con modelos B y N
- **Interfaz:** Material Design 3 con resultados visuales

## 🔧 Configuración

```bash
cd mobile_app
flutter pub get
flutter run
```

Configura la URL del backend en `lib/services/api_service.dart`:
```dart
static const String baseUrl = 'http://10.0.2.2:8000/api';  // Para emulador
```

## 📦 Dependencias

- http ^1.1.0 - Peticiones HTTP
- shared_preferences ^2.2.2 - Almacenamiento local
- file_picker ^6.1.1 - Selección de archivos
- permission_handler ^11.1.0 - Permisos

## 📄 Licencia

Proyecto KLDC - Detección de IA
