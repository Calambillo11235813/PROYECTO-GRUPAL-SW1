import torch
from texto.predictor import TextoPredictor

class FakeTokenizer:
    def __init__(self, token_len_fn=None):
        self.token_len_fn = token_len_fn or (lambda t: len(t.split()))
    def encode(self, text, add_special_tokens=True):
        n = self.token_len_fn(text)
        return list(range(n))
    def decode(self, ids, skip_special_tokens=True):
        return "decoded_chunk"
    def __call__(self, text, return_tensors="pt", truncation=True, max_length=None, padding=None, add_special_tokens=True):
        max_len = max_length or self.token_len_fn(text)
        input_ids = torch.ones((1, max_len), dtype=torch.long)
        attention_mask = torch.ones((1, max_len), dtype=torch.long)
        return {'input_ids': input_ids, 'attention_mask': attention_mask}

class FakeModel:
    def __init__(self, prob_ia=0.8):
        self.prob_ia = prob_ia
    def __call__(self, **inputs):
        p = self.prob_ia
        logits = torch.log(torch.tensor([[1.0 - p, p]], dtype=torch.float32))
        class Out:
            def __init__(self, logits):
                self.logits = logits
        return Out(logits)

if __name__ == '__main__':
    tokenizer = FakeTokenizer()
    model = FakeModel(prob_ia=0.85)
    pr = TextoPredictor(model_type='B', model=model, tokenizer=tokenizer)
    res = pr.predict('Hello world')
    print(res)
