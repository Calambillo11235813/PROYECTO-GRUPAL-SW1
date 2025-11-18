import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user_model.dart';

/// Servicio de Autenticación
class AuthService {
  static const String baseUrl = 'http://localhost:8000/api/auth';

  // Claves para almacenamiento local
  static const String _accessTokenKey = 'access_token';
  static const String _refreshTokenKey = 'refresh_token';
  static const String _userDataKey = 'user_data';

  // === REGISTRO ===

  Future<Map<String, dynamic>> register({
    required String email,
    required String username,
    required String password,
    required String firstName,
    required String lastName,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/register/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'username': username,
        'password': password,
        'first_name': firstName,
        'last_name': lastName,
      }),
    );

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body);
      await _saveTokens(data['tokens']['access'], data['tokens']['refresh']);
      await _saveUserData(data['user']);
      return data;
    } else {
      throw Exception('Error en registro: ${response.body}');
    }
  }

  // === LOGIN ===

  Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/login/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      await _saveTokens(data['tokens']['access'], data['tokens']['refresh']);
      await _saveUserData(data['user']);
      return data;
    } else {
      throw Exception('Error en login: ${response.body}');
    }
  }

  // === LOGOUT ===

  Future<void> logout() async {
    final refreshToken = await getRefreshToken();

    if (refreshToken != null) {
      try {
        await http.post(
          Uri.parse('$baseUrl/logout/'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({'refresh': refreshToken}),
        );
      } catch (e) {
        // Ignorar errores de logout en el servidor
      }
    }

    await _clearTokens();
  }

  // === GESTIÓN DE TOKENS ===

  Future<void> _saveTokens(String accessToken, String refreshToken) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_accessTokenKey, accessToken);
    await prefs.setString(_refreshTokenKey, refreshToken);
  }

  Future<String?> getAccessToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_accessTokenKey);
  }

  Future<String?> getRefreshToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_refreshTokenKey);
  }

  Future<void> _clearTokens() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_accessTokenKey);
    await prefs.remove(_refreshTokenKey);
    await prefs.remove(_userDataKey);
  }

  // === GESTIÓN DE USUARIO ===

  Future<void> _saveUserData(Map<String, dynamic> userData) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_userDataKey, jsonEncode(userData));
  }

  Future<User?> getCurrentUser() async {
    final prefs = await SharedPreferences.getInstance();
    final userDataString = prefs.getString(_userDataKey);

    if (userDataString != null) {
      final userData = jsonDecode(userDataString);
      return User.fromJson(userData);
    }

    return null;
  }

  Future<bool> isAuthenticated() async {
    final token = await getAccessToken();
    return token != null;
  }

  // === PERFIL ===

  Future<Map<String, dynamic>> getProfile() async {
    final token = await getAccessToken();

    if (token == null) {
      throw Exception('Usuario no autenticado');
    }

    final response = await http.get(
      Uri.parse('$baseUrl/profile/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Error al obtener perfil: ${response.body}');
    }
  }
}
