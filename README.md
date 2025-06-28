# 🎵 Güvenilir MP3'tan Metne Çevirici

Bu Python betiği, bir `.mp3` ses dosyasını **Türkçe metne** dönüştürmek için üç farklı yöntem dener:

- 🛠 **Pydub** ile WAV'a dönüştürerek tanıma
- ⚙️ **FFmpeg** kullanarak WAV formatına dönüştürüp tanıma
- 🧪 **Doğrudan MP3 okuma** (deneysel)

Her yöntem başarısız olursa sıradaki denenir. En başarılı olan sonuç döndürülür ve `.txt` dosyası olarak kaydedilir.

---

## 🧩 Gereksinimler

Aşağıdaki Python kütüphanelerinin kurulu olması gerekir:

```bash
pip install SpeechRecognition pydub
