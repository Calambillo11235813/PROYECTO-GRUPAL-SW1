import 'package:flutter/material.dart';

/// Colores cyberpunk/neón basados en el frontend
class AppColors {
  // Colores principales
  static const Color azulNeon = Color(0xFF06B6D4); // cyan-500
  static const Color purpuraNeon = Color(0xFFA855F7); // purple-500
  static const Color amarilloAcento = Color(0xFFFDE047); // yellow-300
  static const Color fondoOscuro = Color(0xFF0F172A); // slate-900
  static const Color textoClaro = Color(0xFFF1F5F9); // slate-100
  static const Color exito = Color(0xFF22C55E); // green-500
  static const Color peligro = Color(0xFFF97316); // orange-500

  // Variaciones
  static const Color fondoTarjeta = Color(0xFF1E293B); // slate-800
  static const Color bordeSutil = Color(0xFF334155); // slate-700
  static const Color textoSecundario = Color(0xFF94A3B8); // slate-400
}

/// Tema principal de la aplicación con estilo cyberpunk
class AppTheme {
  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,

      // Color scheme principal
      colorScheme: ColorScheme.dark(
        primary: AppColors.azulNeon,
        secondary: AppColors.purpuraNeon,
        surface: AppColors.fondoOscuro,
        background: AppColors.fondoOscuro,
        error: AppColors.peligro,
        onPrimary: AppColors.fondoOscuro,
        onSecondary: AppColors.fondoOscuro,
        onSurface: AppColors.textoClaro,
        onBackground: AppColors.textoClaro,
        onError: Colors.white,
      ),

      // Scaffold
      scaffoldBackgroundColor: AppColors.fondoOscuro,

      // AppBar
      appBarTheme: AppBarTheme(
        backgroundColor: AppColors.fondoOscuro,
        elevation: 0,
        centerTitle: true,
        iconTheme: const IconThemeData(color: AppColors.azulNeon),
        titleTextStyle: const TextStyle(
          color: AppColors.textoClaro,
          fontSize: 20,
          fontWeight: FontWeight.bold,
        ),
      ),

      // Cards
      cardTheme: CardThemeData(
        color: AppColors.fondoTarjeta,
        elevation: 8,
        shadowColor: AppColors.azulNeon,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: const BorderSide(color: AppColors.bordeSutil, width: 1),
        ),
      ),

      // Botones elevados
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.azulNeon,
          foregroundColor: AppColors.fondoOscuro,
          elevation: 8,
          shadowColor: AppColors.azulNeon.withOpacity(0.5),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ),

      // Botones de texto
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          foregroundColor: AppColors.azulNeon,
          textStyle: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
        ),
      ),

      // Campos de texto
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: AppColors.fondoTarjeta,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: AppColors.bordeSutil),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: AppColors.bordeSutil),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: AppColors.azulNeon, width: 2),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: AppColors.peligro),
        ),
        labelStyle: TextStyle(color: AppColors.textoSecundario),
        hintStyle: TextStyle(color: AppColors.textoSecundario),
        prefixIconColor: AppColors.azulNeon,
        suffixIconColor: AppColors.textoSecundario,
      ),

      // Iconos
      iconTheme: const IconThemeData(color: AppColors.azulNeon, size: 24),

      // Progress indicators
      progressIndicatorTheme: const ProgressIndicatorThemeData(
        color: AppColors.azulNeon,
        circularTrackColor: AppColors.bordeSutil,
      ),

      // Dividers
      dividerTheme: DividerThemeData(color: AppColors.bordeSutil, thickness: 1),

      // Texto
      textTheme: const TextTheme(
        displayLarge: TextStyle(
          fontSize: 32,
          fontWeight: FontWeight.bold,
          color: AppColors.textoClaro,
        ),
        displayMedium: TextStyle(
          fontSize: 28,
          fontWeight: FontWeight.bold,
          color: AppColors.textoClaro,
        ),
        displaySmall: TextStyle(
          fontSize: 24,
          fontWeight: FontWeight.bold,
          color: AppColors.textoClaro,
        ),
        headlineLarge: TextStyle(
          fontSize: 22,
          fontWeight: FontWeight.w600,
          color: AppColors.textoClaro,
        ),
        headlineMedium: TextStyle(
          fontSize: 20,
          fontWeight: FontWeight.w600,
          color: AppColors.textoClaro,
        ),
        headlineSmall: TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.w600,
          color: AppColors.textoClaro,
        ),
        titleLarge: TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.w500,
          color: AppColors.textoClaro,
        ),
        titleMedium: TextStyle(
          fontSize: 16,
          fontWeight: FontWeight.w500,
          color: AppColors.textoClaro,
        ),
        titleSmall: TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.w500,
          color: AppColors.textoClaro,
        ),
        bodyLarge: TextStyle(fontSize: 16, color: AppColors.textoClaro),
        bodyMedium: TextStyle(fontSize: 14, color: AppColors.textoClaro),
        bodySmall: TextStyle(fontSize: 12, color: AppColors.textoSecundario),
        labelLarge: TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.w600,
          color: AppColors.textoClaro,
        ),
        labelMedium: TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.w600,
          color: AppColors.textoSecundario,
        ),
        labelSmall: TextStyle(
          fontSize: 11,
          fontWeight: FontWeight.w600,
          color: AppColors.textoSecundario,
        ),
      ),
    );
  }

  // Gradiente cyberpunk para fondos especiales
  static LinearGradient get cyberpunkGradient {
    return const LinearGradient(
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
      colors: [AppColors.azulNeon, AppColors.purpuraNeon],
    );
  }

  // Sombra neón para elementos destacados
  static List<BoxShadow> get neonGlow {
    return [
      BoxShadow(
        color: AppColors.azulNeon.withOpacity(0.5),
        blurRadius: 20,
        spreadRadius: 2,
      ),
    ];
  }

  // Sombra suave
  static List<BoxShadow> get softShadow {
    return [
      BoxShadow(
        color: Colors.black.withOpacity(0.3),
        blurRadius: 10,
        offset: const Offset(0, 4),
      ),
    ];
  }
}
