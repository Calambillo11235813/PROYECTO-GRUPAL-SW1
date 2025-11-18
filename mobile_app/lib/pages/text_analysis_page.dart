import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/text_analysis_model.dart';
import '../theme/app_theme.dart';
import '../widgets/result_card.dart';

/// Página de análisis de texto
class TextAnalysisPage extends StatefulWidget {
  const TextAnalysisPage({Key? key}) : super(key: key);

  @override
  State<TextAnalysisPage> createState() => _TextAnalysisPageState();
}

class _TextAnalysisPageState extends State<TextAnalysisPage> {
  final _textController = TextEditingController();
  final ApiService _apiService = ApiService();

  bool _isLoading = false;
  TextAnalysis? _result;
  String _selectedModel = 'B';

  @override
  void dispose() {
    _textController.dispose();
    super.dispose();
  }

  Future<void> _handleAnalyze() async {
    if (_textController.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Por favor ingresa un texto')),
      );
      return;
    }

    setState(() {
      _isLoading = true;
      _result = null;
    });

    try {
      final result = await _apiService.analizarTexto(
        _textController.text.trim(),
        modelo: _selectedModel,
      );

      setState(() {
        _result = result;
      });
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error: $e'),
            backgroundColor: AppColors.peligro,
            behavior: SnackBarBehavior.floating,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Análisis de Texto')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Selector de modelo
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Modelo de análisis',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const SizedBox(height: 8),
                    SegmentedButton<String>(
                      segments: const [
                        ButtonSegment(
                          value: 'B',
                          label: Text('Modelo B'),
                          icon: Icon(Icons.star),
                        ),
                        ButtonSegment(
                          value: 'N',
                          label: Text('Modelo N'),
                          icon: Icon(Icons.science),
                        ),
                      ],
                      selected: {_selectedModel},
                      onSelectionChanged: (Set<String> newSelection) {
                        setState(() {
                          _selectedModel = newSelection.first;
                        });
                      },
                      style: ButtonStyle(
                        backgroundColor: MaterialStateProperty.resolveWith((
                          states,
                        ) {
                          if (states.contains(MaterialState.selected)) {
                            return AppColors.azulNeon;
                          }
                          return AppColors.fondoTarjeta;
                        }),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Campo de texto
            TextField(
              controller: _textController,
              maxLines: 10,
              decoration: const InputDecoration(
                hintText: 'Escribe o pega el texto a analizar...',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),

            // Botón de análisis
            ElevatedButton(
              onPressed: _isLoading ? null : _handleAnalyze,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              child: _isLoading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Text('Analizar Texto'),
            ),
            const SizedBox(height: 24),

            // Resultado
            if (_result != null)
              ResultCard(
                title: 'Resultado del Análisis',
                result: _result!.prediccion,
                probabilityIA: _result!.probabilidadIa,
                probabilityHuman: _result!.probabilidadHumano,
                confidence: _result!.confianza,
                isIA: _result!.esIA,
              ),
          ],
        ),
      ),
    );
  }
}
