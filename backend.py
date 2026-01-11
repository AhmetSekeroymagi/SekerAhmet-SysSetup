# backend.py
import subprocess
import ctypes
import sys
import psutil
import platform
import socket
import datetime
import shutil
import os
import json

def is_admin():
    """Yönetici haklarını kontrol eder."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def restart_as_admin():
    """Programı yönetici olarak yeniden başlatır."""
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def run_command(command):
    """Verilen komutu çalıştırır ve sonucu döner."""
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, 
                                startupinfo=startupinfo, shell=True, encoding="utf-8", errors="ignore")
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, str(e)

def install_package(package_id):
    """Winget ile kurulum yapar."""
    cmd = f"winget install -e --id {package_id} --silent --accept-package-agreements --accept-source-agreements"
    return run_command(cmd)

def uninstall_package(package_name):
    """Winget ile kaldırma yapar."""
    cmd = f'winget uninstall --name "{package_name}" --silent --accept-source-agreements'
    return run_command(cmd)

def get_installed_apps():
    """Yüklü programları listeler."""
    success, output = run_command("winget list")
    if not success: return []
    
    apps = []
    lines = output.splitlines()
    
    for line in lines:
        line = line.strip()
        # Header ve ayırıcıları filtrele
        if not line or line.startswith("Name") or line.startswith("Id") or "-------" in line or len(line) < 3:
            continue
            
        # Winget çıktısında ilk 35 karakter genelde isimdir
        name = line[:35].strip()
        
        if name:
            apps.append({"name": name, "full": line})
            
    apps.sort(key=lambda x: x["name"].lower())
    return apps

def restart_explorer():
    run_command("taskkill /f /im explorer.exe")
    subprocess.Popen("explorer.exe", shell=True)

# --- STARTUP MANAGER ---
def get_startup_items():
    """Başlangıçta çalışan programları listeler."""
    ps_command = 'Get-CimInstance Win32_StartupCommand | Select-Object Name, Command, Location | ConvertTo-Json'
    
    success, output = run_command(f'powershell -Command "{ps_command}"')
    if not success or not output.strip(): return []
    
    try:
        items = json.loads(output)
        if isinstance(items, dict): items = [items]
        return items
    except:
        return []

def remove_startup_item(name, location):
    """Programı başlangıçtan kaldırır."""
    if "HK" in location: # Registry (HKCU veya HKLM)
        reg_path = "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        if "HKLM" in location or "LocalMachine" in location:
            reg_path = "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            
        cmd = f'reg delete "{reg_path}" /v "{name}" /f'
        return run_command(cmd)
        
    elif "Startup" in location:
        return False, "Dosya tabanlı startup silme henüz aktif değil."
    
    return False, "Bilinmeyen konum."

# --- PROFIL YÖNETİMİ ---
def save_profile(filepath, data):
    """Seçili ayarları JSON dosyasına kaydeder."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True, "Profil başarıyla kaydedildi."
    except Exception as e:
        return False, f"Kaydetme hatası: {str(e)}"

def load_profile(filepath):
    """JSON dosyasından ayarları okur."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return True, data
    except Exception as e:
        return False, None

# --- GÜNCELLEME MODÜLÜ ---
def update_all_packages():
    """Bilgisayardaki tüm programları son sürüme günceller."""
    cmd = "winget upgrade --all --include-unknown --silent --accept-package-agreements --accept-source-agreements"
    return run_command(cmd)

# --- DASHBOARD / SİSTEM İZLEME ---
def get_system_stats():
    """Anlık CPU, RAM ve Disk verilerini döner."""
    try:
        # CPU
        cpu_usage = psutil.cpu_percent(interval=None)
        
        # RAM
        ram = psutil.virtual_memory()
        ram_percent = ram.percent
        ram_used = round(ram.used / (1024**3), 1)
        ram_total = round(ram.total / (1024**3), 1)
        
        # Disk (C:)
        disk = psutil.disk_usage('C:\\')
        disk_percent = disk.percent
        disk_free = round(disk.free / (1024**3), 1)
        
        return {
            "cpu": cpu_usage,
            "ram_percent": ram_percent,
            "ram_text": f"{ram_used} GB / {ram_total} GB",
            "disk_percent": disk_percent,
            "disk_text": f"{disk_free} GB Boş (C:)"
        }
    except Exception as e:
        return {"cpu": 0, "ram_percent": 0, "ram_text": "Hata", "disk_percent": 0, "disk_text": "Hata"}

def get_system_info():
    """Statik sistem bilgilerini döner (Windows 11 tespiti dahil)."""
    try:
        hostname = socket.gethostname()
        
        os_name = platform.system()
        os_release = platform.release()
        
        # Windows 11 Kontrolü (Build >= 22000)
        if os_name == "Windows":
            try:
                version_parts = platform.version().split('.')
                build_number = int(version_parts[2])
                if build_number >= 22000:
                    os_release = "11"
            except:
                pass
        
        os_info = f"{os_name} {os_release}"
        
        # Uptime hesaplama
        # Not: Fast Startup açıksa sadece restart sonrası sıfırlanır.
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.datetime.fromtimestamp(boot_time_timestamp)
        now = datetime.datetime.now()
        uptime = now - bt
        
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days > 0:
            uptime_str = f"{days} gün, {hours} sa, {minutes} dk"
        else:
            uptime_str = f"{hours} sa, {minutes} dk"
        
        ip_addr = socket.gethostbyname(socket.gethostname())

        return {
            "hostname": hostname,
            "os": os_info,
            "uptime": uptime_str,
            "ip": ip_addr
        }
    except Exception as e:
        return {"hostname": "-", "os": f"Hata: {str(e)}", "uptime": "-", "ip": "-"}

# --- TEMİZLİK MODÜLÜ ---
def clean_item(item_type):
    """Belirtilen türdeki sistem artıklarını temizler."""
    msg = ""
    try:
        if item_type == "temp":
            temp_path = os.getenv('TEMP')
            files_deleted = 0
            for root, dirs, files in os.walk(temp_path):
                for f in files:
                    try:
                        os.remove(os.path.join(root, f))
                        files_deleted += 1
                    except: pass
                for d in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, d))
                    except: pass
            msg = f"Temp klasörü temizlendi ({files_deleted} dosya)."

        elif item_type == "prefetch":
            prefetch_path = "C:\\Windows\\Prefetch"
            files_deleted = 0
            if os.path.exists(prefetch_path):
                for f in os.listdir(prefetch_path):
                    try:
                        os.remove(os.path.join(prefetch_path, f))
                        files_deleted += 1
                    except: pass
            msg = f"Prefetch temizlendi ({files_deleted} dosya)."

        elif item_type == "dns":
            run_command("ipconfig /flushdns")
            msg = "DNS önbelleği sıfırlandı."

        elif item_type == "recycle":
            # -Force parametresi onay sormadan siler
            run_command('powershell -Command "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"')
            msg = "Geri Dönüşüm Kutusu boşaltıldı."

        elif item_type == "windows_update":
            run_command("net stop wuauserv")
            path = "C:\\Windows\\SoftwareDistribution\\Download"
            if os.path.exists(path):
                shutil.rmtree(path, ignore_errors=True)
            run_command("net start wuauserv")
            msg = "Windows Update kalıntıları temizlendi."

        return True, msg

    except Exception as e:
        return False, f"Hata: {str(e)}"

# --- GÜNCELLEME MOTORU v2 ---
def check_for_updates():
    """Güncelleme bekleyen uygulamaların listesini döner."""
    success, output = run_command("winget upgrade --include-unknown")
    if not success: return []

    updates = []
    lines = output.splitlines()
    
    start_parsing = False
    for line in lines:
        if "Name" in line and "Id" in line:
            start_parsing = True
            continue
        
        if "---" in line: continue
        
        if start_parsing and line.strip():
            # Satırın başındaki ismi al (Genelde ilk 35 karakter)
            name = line[:35].strip()
            updates.append({"name": name, "full_line": line})
                
    return updates

def update_single_package(package_name):
    """Tek bir paketi günceller."""
    cmd = f'winget upgrade --name "{package_name}" --silent --accept-package-agreements --accept-source-agreements'
    return run_command(cmd)