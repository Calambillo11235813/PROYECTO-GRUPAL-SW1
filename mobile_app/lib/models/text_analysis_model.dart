/// Modelo de Análisis de Texto
class TextAnalysis {
  final int? id;
  final String prediccion;
  final double probabilidadIa;
  final double probabilidadHumano;
  final String confianza;
  final String modeloUsado;
  final DateTime? fechaAnalisis;

  TextAnalysis({
    this.id,
    required this.prediccion,
    required this.probabilidadIa,
    required this.probabilidadHumano,
    required this.confianza,
    required this.modeloUsado,
    this.fechaAnalisis,
  });

  factory TextAnalysis.fromJson(Map<String, dynamic> json) {
    return TextAnalysis(
      id: json['analisis_id'],
      prediccion: json['prediccion'] ?? json['resultado'],
      probabilidadIa: (json['probabilidad_ia'] ?? 0.0).toDouble(),
      probabilidadHumano: (json['probabilidad_humano'] ?? 0.0).toDouble(),
      confianza: json['confianza'] ?? 'MEDIA',
      modeloUsado: json['modelo_usado'] ?? json['modelo_utilizado'] ?? 'B',
      fechaAnalisis: json['fecha_analisis'] != null
          ? DateTime.parse(json['fecha_analisis'])
          : null,
    );
  }

  bool get esIA => prediccion.toUpperCase() == 'IA';
  bool get esHumano => prediccion.toUpperCase() == 'HUMANO';
  bool get altaConfianza => confianza.toUpperCase() == 'ALTA';
}
