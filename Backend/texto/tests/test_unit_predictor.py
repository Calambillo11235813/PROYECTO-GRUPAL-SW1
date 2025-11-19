import unittest
import torch

from texto.predictor import TextoPredictor


class FakeTokenizer:
    def __init__(self, token_len_fn=None):
        # token_len_fn: function(text) -> int
        self.token_len_fn = token_len_fn or (lambda t: len(t.split()))

    def encode(self, text, add_special_tokens=True):
        n = self.token_len_fn(text)
        return list(range(n))

    def decode(self, ids, skip_special_tokens=True):
        # Return a simple string to be tokenized again
        return "decoded_chunk"

    def __call__(self, text, return_tensors="pt", truncation=True, max_length=None, padding=None, add_special_tokens=True):
        # Simulate tokenizer returning fixed-size tensors (batch_size=1)
        max_len = max_length or self.token_len_fn(text)
        input_ids = torch.ones((1, max_len), dtype=torch.long)
        attention_mask = torch.ones((1, max_len), dtype=torch.long)
        return {'input_ids': input_ids, 'attention_mask': attention_mask}


class FakeModel:
    def __init__(self, prob_ia=0.8):
        # prob_ia: probability for IA class
        self.prob_ia = prob_ia

    def __call__(self, **inputs):
        # Return an object with logits attribute
        p = self.prob_ia
        logits = torch.log(torch.tensor([[1.0 - p, p]], dtype=torch.float32))
        class Out:
            def __init__(self, logits):
                self.logits = logits
        return Out(logits)


class TextoPredictorTests(unittest.TestCase):
    def test_predict_short_text(self):
        tokenizer = FakeTokenizer()
        model = FakeModel(prob_ia=0.85)
        predictor = TextoPredictor(model_type='B', model=model, tokenizer=tokenizer)

        res = predictor.predict('Hello world')
        self.assertIn('prediccion', res)
        self.assertIn('probabilidad_ia', res)
        self.assertEqual(res['prediccion'], 'IA')

    def test_predict_long_text_chunks(self):
        # Force small max_length to trigger chunking
        tokenizer = FakeTokenizer(token_len_fn=lambda t: len(t.split()))
        model = FakeModel(prob_ia=0.7)
        predictor = TextoPredictor(model_type='B', model=model, tokenizer=tokenizer)
        predictor.max_length = 10

        # Create a long text (50 words)
        long_text = 'word ' * 50
        res = predictor.predict(long_text)
        self.assertIn('prediccion', res)
        self.assertIn('probabilidad_ia', res)
        self.assertEqual(res['prediccion'], 'IA')


if __name__ == '__main__':
    unittest.main()
