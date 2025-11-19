from django.test import SimpleTestCase
from unittest.mock import patch
import json
import datetime


class FakePredictor:
    def predict(self, text):
        return {
            'prediccion': 'IA',
            'probabilidad_ia': 0.75,
            'probabilidad_humano': 0.25,
            'confianza': 'ALTA',
            'modelo_usado': 'B'
        }


class AnalizarTextoIntegrationTest(SimpleTestCase):
    @patch('texto.views.get_predictor')
    @patch('texto.views.AnalisisTexto')
    def test_analizar_texto_integration(self, mock_analisis_model, mock_get_predictor):
        """Integration test for /api/texto/analizar/ that patches predictor and model creation to avoid heavy model loads and DB usage."""
        mock_get_predictor.return_value = FakePredictor()

        # Patch AnalisisTexto.objects.create to return a dummy object with id and fecha_analisis
        dummy = type('D', (), {'id': 1, 'fecha_analisis': datetime.datetime.utcnow()})
        mock_analisis_model.objects.create.return_value = dummy

        payload = {
            'texto': 'Este es un texto de prueba para integración que debe procesarse correctamente.',
            'modelo': 'B'
        }

        response = self.client.post('/api/texto/analizar/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('prediccion', data)
        self.assertIn('probabilidad_ia', data)
        self.assertEqual(data['prediccion'], 'IA')
