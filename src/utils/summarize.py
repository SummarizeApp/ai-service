from src.model.load_model import model, tokenizer
from src.config import device

def summarize_with_model(input_text):
    try:
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True, max_length=4096)
    except Exception as e:
        raise ValueError(f"Tokenizasyon sırasında hata oluştu: {e}")
    
    try:
        inputs = {key: value.to(device) for key, value in inputs.items()}
    except Exception as e:
        raise ValueError(f"Verilerin cihaza yüklenmesi sırasında hata oluştu: {e}")
    
    try:
        outputs = model.generate(**inputs, max_length=1024, num_beams=4, early_stopping=True)
    except Exception as e:
        raise RuntimeError(f"Model özetleme sırasında hata oluştu: {e}")
    
    try:
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        raise ValueError(f"Özetin çözülmesi sırasında hata oluştu: {e}")
    
    return summary