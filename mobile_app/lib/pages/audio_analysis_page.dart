import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

/// Página de análisis de audio (pendiente de implementación completa)
class AudioAnalysisPage extends StatefulWidget {
  const AudioAnalysisPage({Key? key}) : super(key: key);

  @override
  State<AudioAnalysisPage> createState() => _AudioAnalysisPageState();
}

class _AudioAnalysisPageState extends State<AudioAnalysisPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Análisis de Audio')),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Ícono con gradiente cyberpunk y glow
              Container(
                padding: const EdgeInsets.all(32),
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: AppTheme.cyberpunkGradient,
                  boxShadow: [
                    BoxShadow(
                      color: AppColors.purpuraNeon.withOpacity(0.5),
                      blurRadius: 20,
                      spreadRadius: 2,
                    ),
                  ],
                ),
                child: const Icon(
                  Icons.audiotrack,
                  size: 80,
                  color: Colors.white,
                ),
              ),
              const SizedBox(height: 32),

              // Badge "PRÓXIMAMENTE"
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 8,
                ),
                decoration: BoxDecoration(
                  color: AppColors.amarilloAcento.withOpacity(0.2),
                  border: Border.all(color: AppColors.amarilloAcento, width: 2),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: const Text(
                  'PRÓXIMAMENTE',
                  style: TextStyle(
                    color: AppColors.amarilloAcento,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.5,
                  ),
                ),
              ),
              const SizedBox(height: 24),

              Text(
                'Análisis de Audio con IA',
                style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                  color: AppColors.azulNeon,
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),

              // Lista de características
              Card(
                color: AppColors.fondoTarjeta,
                elevation: 8,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                  side: BorderSide(
                    color: AppColors.purpuraNeon.withOpacity(0.3),
                  ),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    children: [
                      _buildFeature(
                        Icons.upload_file,
                        'Subir archivos de audio',
                      ),
                      const SizedBox(height: 12),
                      _buildFeature(
                        Icons.verified_user,
                        'Verificar autenticidad con IA',
                      ),
                      const SizedBox(height: 12),
                      _buildFeature(
                        Icons.graphic_eq,
                        'Visualizar espectrogramas',
                      ),
                      const SizedBox(height: 12),
                      _buildFeature(
                        Icons.download,
                        'Descargar certificados PDF',
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildFeature(IconData icon, String text) {
    return Row(
      children: [
        Icon(icon, color: AppColors.purpuraNeon, size: 24),
        const SizedBox(width: 12),
        Expanded(
          child: Text(
            text,
            style: const TextStyle(
              fontSize: 16,
              color: AppColors.textoSecundario,
            ),
          ),
        ),
      ],
    );
  }
}
