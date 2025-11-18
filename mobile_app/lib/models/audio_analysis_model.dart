/// Modelo de Análisis de Audio
class AudioAnalysis {
  final int id;
  final String fileUrl;
  final String? originalFilename;
  final String? result;
  final double? probability;
  final String? spectrogram;
  final DateTime createdAt;

  AudioAnalysis({
    required this.id,
    required this.fileUrl,
    this.originalFilename,
    this.result,
    this.probability,
    this.spectrogram,
    required this.createdAt,
  });

  factory AudioAnalysis.fromJson(Map<String, dynamic> json) {
    return AudioAnalysis(
      id: json['id'],
      fileUrl: json['file_url'] ?? '',
      originalFilename: json['original_filename'],
      result: json['result'],
      probability: json['probability']?.toDouble(),
      spectrogram: json['spectrogram'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  bool get esReal => result?.toUpperCase() == 'REAL';
  bool get esIA => result?.toUpperCase() == 'IA';
  String get resultadoTexto => result ?? 'Analizando...';
  double get probabilidadPorcentaje => (probability ?? 0.0) * 100;
}
