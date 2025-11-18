import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

/// Widget reutilizable para mostrar resultados de análisis
class ResultCard extends StatelessWidget {
  final String title;
  final String result;
  final double probabilityIA;
  final double probabilityHuman;
  final String confidence;
  final bool isIA;

  const ResultCard({
    Key? key,
    required this.title,
    required this.result,
    required this.probabilityIA,
    required this.probabilityHuman,
    required this.confidence,
    required this.isIA,
  }) : super(key: key);

  Color _getResultColor() {
    if (isIA) {
      return AppColors.peligro;
    } else {
      return AppColors.exito;
    }
  }

  IconData _getResultIcon() {
    if (isIA) {
      return Icons.smart_toy;
    } else {
      return Icons.person;
    }
  }

  Color _getConfidenceColor() {
    switch (confidence.toUpperCase()) {
      case 'ALTA':
        return AppColors.exito;
      case 'MEDIA':
        return AppColors.amarilloAcento;
      case 'BAJA':
        return AppColors.peligro;
      default:
        return AppColors.textoSecundario;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 8,
      shadowColor: AppColors.azulNeon.withOpacity(0.3),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Título
            Text(title, style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 16),

            // Resultado principal
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: _getResultColor().withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: _getResultColor(), width: 2),
              ),
              child: Row(
                children: [
                  Icon(_getResultIcon(), size: 40, color: _getResultColor()),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Resultado:',
                          style: Theme.of(context).textTheme.bodySmall,
                        ),
                        Text(
                          result.toUpperCase(),
                          style: Theme.of(context).textTheme.headlineSmall
                              ?.copyWith(
                                color: _getResultColor(),
                                fontWeight: FontWeight.bold,
                              ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // Probabilidades
            _buildProbabilityBar(
              context,
              label: 'Probabilidad IA',
              probability: probabilityIA,
              color: Colors.red,
            ),
            const SizedBox(height: 12),
            _buildProbabilityBar(
              context,
              label: 'Probabilidad Humano',
              probability: probabilityHuman,
              color: Colors.green,
            ),
            const SizedBox(height: 20),

            // Confianza
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Nivel de confianza:',
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    color: _getConfidenceColor().withOpacity(0.2),
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: _getConfidenceColor(), width: 1),
                  ),
                  child: Text(
                    confidence.toUpperCase(),
                    style: TextStyle(
                      color: _getConfidenceColor(),
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildProbabilityBar(
    BuildContext context, {
    required String label,
    required double probability,
    required Color color,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label),
            Text(
              '${probability.toStringAsFixed(1)}%',
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
          ],
        ),
        const SizedBox(height: 4),
        Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(8),
            boxShadow: [
              BoxShadow(
                color: color.withOpacity(0.3),
                blurRadius: 8,
                spreadRadius: 1,
              ),
            ],
          ),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: LinearProgressIndicator(
              value: probability / 100,
              backgroundColor: AppColors.bordeSutil,
              valueColor: AlwaysStoppedAnimation<Color>(color),
              minHeight: 12,
            ),
          ),
        ),
      ],
    );
  }
}
