import subprocess
import ctypes
import sys
import os

# Uygulama Listesi (Adı : Winget ID'si)
# Winget ID'lerini terminale 'winget search program_adi' yazarak bulabilirsin.
UYGULAMALAR = {
    "Notepad++": "Notepad++.Notepad++",
    "7-Zip": "7zip.7zip",
    "Google Chrome": "Google.Chrome",
    "VLC Player": "VideoLAN.VLC",
    "VS Code": "Microsoft.VisualStudioCode"
}

def is_admin():
    """Kullanıcı yönetici mi diye kontrol eder."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def install_program(app_name, app_id):
    """Winget kullanarak programı sessizce kurar."""
    print(f"⏳ {app_name} kuruluyor... Lütfen bekleyin.")
    
    # Winget komutu: install (kur), -e (tam eşleşme), --id (kimlik), --silent (sessiz mod), --accept-source-agreements (onaylar)
    command = f"winget install -e --id {app_id} --silent --accept-package-agreements --accept-source-agreements"
    
    # Komutu çalıştır
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {app_name} başarıyla kuruldu!")
        return True
    else:
        print(f"❌ {app_name} kurulamadı. Hata: {result.stderr}")
        return False

def main():
    # 1. Yönetici izni kontrolü
    if not is_admin():
        print("⚠️  Bu script Yönetici hakları gerektirir. Yeniden başlatılıyor...")
        # Scripti yönetici olarak tekrar çalıştır
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    print("="*40)
    print("   OTOMATİK KURULUM SİSTEMİ (SysSetup)")
    print("="*40)

    # 2. Kurulum Döngüsü
    basarili = 0
    basarisiz = 0

    for name, app_id in UYGULAMALAR.items():
        # Kullanıcıya soralım mı? (Şimdilik hepsini kuralım)
        if install_program(name, app_id):
            basarili += 1
        else:
            basarisiz += 1
            
    print("\n" + "="*40)
    print(f"🎉 İşlem Tamamlandı!")
    print(f"Başarılı: {basarili} | Başarısız: {basarisiz}")
    input("\nÇıkmak için Enter'a basın...")

if __name__ == "__main__":
    main()