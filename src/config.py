import os
import torch

try:
    # CUDA kontrolü
    if not torch.cuda.is_available():
        raise EnvironmentError("CUDA cihazı bulunamadı. Lütfen GPU'nuzun doğru kurulu ve aktif olduğundan emin olun.")
    
    device = torch.device("cuda")
except EnvironmentError as e:
    print(f"Hata: {e}")
    device = torch.device("cpu")  # Alternatif olarak CPU'yu kullan

save_directory = "./models/model"

try:
    if not os.path.exists(save_directory):
        raise FileNotFoundError(f"Klasör bulunamadı: {save_directory}")
except FileNotFoundError as e:
    print(f"Hata: {e}")
except OSError as e:
    print(f"Klasör kontrol edilirken hata oluştu: {e}")