import speech_recognition as sr
from pydub import AudioSegment
import os
import sys
import time

def mp3_to_text_robust(mp3_file_path):
    """
    Güvenilir MP3'ten metne çevirme
    """
    try:
        print(f"🎵 MP3 dosyası işleniyor: {mp3_file_path}")
        print("=" * 50)
        
        # Farklı yöntemlerle dene
        methods = [
            ("Pydub ile WAV'a çevir", convert_with_pydub),
            ("FFmpeg ile WAV'a çevir", convert_with_ffmpeg),
            ("Doğrudan MP3 oku", read_mp3_direct)
        ]
        
        for method_name, method_func in methods:
            try:
                print(f"\n🔄 {method_name} deneniyor...")
                result = method_func(mp3_file_path)
                
                if result:
                    print(f"✅ {method_name} başarılı!")
                    return result
                    
            except Exception as e:
                print(f"❌ {method_name} hatası: {e}")
                continue
        
        print("\n❌ Hiçbir yöntem çalışmadı!")
        return None
        
    except Exception as e:
        print(f"❌ Genel hata: {e}")
        return None

def convert_with_pydub(mp3_file_path):
    """
    Pydub ile WAV'a çevir
    """
    # MP3'ü WAV'a çevir
    audio = AudioSegment.from_mp3(mp3_file_path)
    temp_wav = "temp_audio_pydub.wav"
    audio.export(temp_wav, format="wav")
    
    # Speech recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_wav) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language="tr-TR")  # type: ignore[attr-defined]
    
    # Temizlik
    if os.path.exists(temp_wav):
        os.remove(temp_wav)
    
    return text

def convert_with_ffmpeg(mp3_file_path):
    """
    FFmpeg ile WAV'a çevir
    """
    import subprocess
    
    temp_wav = "temp_audio_ffmpeg.wav"
    
    # FFmpeg komutu
    cmd = [
        'ffmpeg', '-i', mp3_file_path,
        '-acodec', 'pcm_s16le',
        '-ar', '16000',
        '-ac', '1',
        '-y', temp_wav
    ]
    
    # FFmpeg çalıştır
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"FFmpeg hatası: {result.stderr}")
    
    # Speech recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_wav) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language="tr-TR")  # type: ignore[attr-defined]
    
    # Temizlik
    if os.path.exists(temp_wav):
        os.remove(temp_wav)
    
    return text

def read_mp3_direct(mp3_file_path):
    """
    Doğrudan MP3'ü oku (deneysel)
    """
    # Bu yöntem genellikle çalışmaz ama deneyelim
    recognizer = sr.Recognizer()
    
    # MP3'ü doğrudan oku
    with sr.AudioFile(mp3_file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language="tr-TR")  # type: ignore[attr-defined]
    
    return text

def main():
    """
    Ana fonksiyon
    """
    print("🎵 Güvenilir MP3'ten Metne Çevirme")
    print("=" * 40)
    print("🔧 Farklı yöntemlerle çalışır")
    print("=" * 40)
    
    # Komut satırından dosya yolu al
    if len(sys.argv) > 1:
        mp3_file = sys.argv[1]
    else:
        # Kullanıcıdan dosya yolu iste
        mp3_file = input("MP3 dosyasının yolunu girin: ").strip()
    
    # Dosya uzantısını kontrol et
    if not mp3_file.lower().endswith('.mp3'):
        print("❌ Hata: Lütfen geçerli bir MP3 dosyası seçin!")
        return
    
    # Dosyanın var olup olmadığını kontrol et
    if not os.path.exists(mp3_file):
        print(f"❌ Hata: {mp3_file} dosyası bulunamadı!")
        return
    
    # MP3'ten metne çevir
    result = mp3_to_text_robust(mp3_file)
    
    if result:
        print("\n" + "=" * 50)
        print("✅ BAŞARILI!")
        print("=" * 50)
        print(result)
        print("=" * 50)
        
        # Sonucu dosyaya kaydet
        output_file = mp3_file.replace('.mp3', '_robust_metin.txt')
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"\n💾 Metin dosyaya kaydedildi: {output_file}")
        except Exception as e:
            print(f"❌ Dosya kaydetme hatası: {e}")
    else:
        print("\n❌ Hiçbir yöntem çalışmadı!")
        print("💡 Öneriler:")
        print("   - Farklı bir MP3 dosyası deneyin")
        print("   - Web tabanlı çözüm kullanın")
        print("   - Dosya formatını kontrol edin")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Uygulama kapatıldı.")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        print("Gerekli kütüphanelerin yüklü olduğundan emin olun:")
        print("pip install SpeechRecognition pydub")