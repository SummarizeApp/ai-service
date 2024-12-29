from transformers import MBartForConditionalGeneration, MBart50Tokenizer
from src.config import device, save_directory

try:
    model = MBartForConditionalGeneration.from_pretrained(save_directory).to(device)
except Exception as e:
    raise RuntimeError(f"Model yüklenirken hata oluştu: {e}")

try:
    tokenizer = MBart50Tokenizer.from_pretrained(save_directory)
except Exception as e:
    raise RuntimeError(f"Tokenizer yüklenirken hata oluştu: {e}")