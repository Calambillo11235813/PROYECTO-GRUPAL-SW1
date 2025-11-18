import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/text_analysis_model.dart';
import '../models/audio_analysis_model.dart';
import 'auth_service.dart';

/// Servicio principal de API
class ApiService {
  // Configuración base de API
  static const String baseUrl = 'http://localhost:8000/api';

  final AuthService _authService = AuthService();

  // Headers comunes
  Future<Map<String, String>> _getHeaders({bool requiresAuth = false}) async {
    final headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };

    if (requiresAuth) {
      final token = await _authService.getAccessToken();
      if (token != null) {
        headers['Authorization'] = 'Bearer $token';
      }
    }

    return headers;
  }

  // === ENDPOINTS DE TEXTO ===

  /// Analizar texto directo
  Future<TextAnalysis> analizarTexto(
    String texto, {
    String modelo = 'B',
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/texto/analizar/'),
      headers: await _getHeaders(),
      body: jsonEncode({'texto': texto, 'modelo': modelo}),
    );

    if (response.statusCode == 200) {
      return TextAnalysis.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Error al analizar texto: ${response.body}');
    }
  }

  /// Analizar archivo de texto
  Future<TextAnalysis> analizarArchivo(
    String filePath, {
    String modelo = 'B',
  }) async {
    final request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/texto/analizar-archivo/'),
    );

    request.fields['modelo'] = modelo;
    request.files.add(await http.MultipartFile.fromPath('archivo', filePath));

    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 200) {
      return TextAnalysis.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Error al analizar archivo: ${response.body}');
    }
  }

  /// Comparar modelos
  Future<Map<String, dynamic>> compararModelos(String texto) async {
    final response = await http.post(
      Uri.parse('$baseUrl/texto/comparar/'),
      headers: await _getHeaders(),
      body: jsonEncode({'texto': texto}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Error al comparar modelos: ${response.body}');
    }
  }

  // === ENDPOINTS DE AUDIO ===

  /// Subir y analizar audio
  Future<AudioAnalysis> analizarAudio(String filePath) async {
    final token = await _authService.getAccessToken();

    final request = http.MultipartRequest('POST', Uri.parse('$baseUrl/audio/'));

    if (token != null) {
      request.headers['Authorization'] = 'Bearer $token';
    }
    request.files.add(await http.MultipartFile.fromPath('file', filePath));

    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body)['data'];
      return AudioAnalysis.fromJson(data);
    } else {
      throw Exception('Error al analizar audio: ${response.body}');
    }
  }

  /// Obtener historial de audios
  Future<List<AudioAnalysis>> obtenerHistorialAudio() async {
    final response = await http.get(
      Uri.parse('$baseUrl/audio/analysis/'),
      headers: await _getHeaders(requiresAuth: true),
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => AudioAnalysis.fromJson(json)).toList();
    } else {
      throw Exception('Error al obtener historial: ${response.body}');
    }
  }

  // === ENDPOINTS DE ESTADO ===

  /// Verificar estado del servicio
  Future<Map<String, dynamic>> verificarEstado() async {
    final response = await http.get(
      Uri.parse('$baseUrl/texto/estado/'),
      headers: await _getHeaders(),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Error al verificar estado: ${response.body}');
    }
  }
}
