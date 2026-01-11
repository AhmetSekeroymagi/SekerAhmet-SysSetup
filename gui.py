# gui.py
import customtkinter as ctk
import threading
from tkinter import filedialog
import backend
from data import SOFTWARE_DB, SYSTEM_TWEAKS

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue") 

class SysSetupApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SysSetup - ŞEKER AHMET V 1.0")
        self.geometry("1300x800")
        
        # Grid Configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Initialize Variables
        self.app_vars = {} 
        for cat, apps in SOFTWARE_DB.items():
            for name, app_id in apps.items():
                self.app_vars[name] = {"var": ctk.BooleanVar(value=False), "id": app_id, "cat": cat}

        self.tweak_vars = {}
        for name, cmds in SYSTEM_TWEAKS.items():
            self.tweak_vars[name] = {"var": ctk.IntVar(value=0), "cmds": cmds}
            
        self.installed_apps_data = []
        self.uninstall_vars = {}
        self.current_page_type = "dashboard" 

        # UI Initialization
        self.create_sidebar()
        self.create_main_area()
        self.create_summary_panel()
        
        # Start with Dashboard
        self.show_dashboard_page()
        self.update_summary()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Logo
        ctk.CTkLabel(self.sidebar, text="🚀 SysSetup", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(30, 20))

        # Dashboard
        ctk.CTkButton(self.sidebar, text="📊 Dashboard", anchor="w", fg_color="transparent", 
                      text_color="#f1c40f", font=ctk.CTkFont(size=14, weight="bold"), hover_color=("gray70", "gray30"),
                      command=self.show_dashboard_page).pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkFrame(self.sidebar, height=2, fg_color="gray").pack(fill="x", padx=20, pady=10)

        # Installation Section
        ctk.CTkLabel(self.sidebar, text="KURULUM", font=ctk.CTkFont(size=12, weight="bold"), text_color="gray").pack(anchor="w", padx=20, pady=(5,5))
        for category in SOFTWARE_DB.keys():
            ctk.CTkButton(self.sidebar, text=category, anchor="w", fg_color="transparent", 
                          text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                          command=lambda c=category: self.show_category_page(c)).pack(fill="x", padx=10, pady=2)

        ctk.CTkFrame(self.sidebar, height=2, fg_color="gray").pack(fill="x", padx=20, pady=20)
        
        # Management Section
        ctk.CTkLabel(self.sidebar, text="YÖNETİM", font=ctk.CTkFont(size=12, weight="bold"), text_color="gray").pack(anchor="w", padx=20, pady=(0,5))
        
        ctk.CTkButton(self.sidebar, text="⚙️ Windows Ayarları", anchor="w", fg_color="transparent", 
                      text_color="#3498db", font=ctk.CTkFont(size=13, weight="bold"), hover_color=("gray70", "gray30"),
                      command=self.show_tweaks_page).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(self.sidebar, text="🗑️ Kaldırıcı", anchor="w", fg_color="transparent", 
                      text_color="#e74c3c", font=ctk.CTkFont(size=13, weight="bold"), hover_color=("gray70", "gray30"),
                      command=self.show_uninstall_page).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(self.sidebar, text="🚀 Başlangıç Hızlandırıcı", anchor="w", fg_color="transparent", 
                      text_color="#f39c12", font=ctk.CTkFont(size=13, weight="bold"), hover_color=("gray70", "gray30"),
                      command=self.show_startup_page).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(self.sidebar, text="🧹 Sistem Temizliği", anchor="w", fg_color="transparent", 
                      text_color="#9b59b6", font=ctk.CTkFont(size=13, weight="bold"), hover_color=("gray70", "gray30"),
                      command=self.show_cleaner_page).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(self.sidebar, text="🔄 Tümünü Güncelle", anchor="w", fg_color="transparent", 
                      text_color="#00cec9", font=ctk.CTkFont(size=13, weight="bold"), hover_color=("gray70", "gray30"),
                      command=self.start_update_all_thread).pack(fill="x", padx=10, pady=5)

        # Profile Section
        ctk.CTkFrame(self.sidebar, height=2, fg_color="gray").pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(self.sidebar, text="PROFIL", font=ctk.CTkFont(size=12, weight="bold"), text_color="gray").pack(anchor="w", padx=20, pady=(0,5))

        ctk.CTkButton(self.sidebar, text="💾 Profili Kaydet", anchor="w", fg_color="transparent", 
                      text_color="#27ae60", font=ctk.CTkFont(size=13, weight="bold"), hover_color=("gray70", "gray30"),
                      command=self.save_current_profile).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(self.sidebar, text="📂 Profili Yükle", anchor="w", fg_color="transparent", 
                      text_color="#f1c40f", font=ctk.CTkFont(size=13, weight="bold"), hover_color=("gray70", "gray30"),
                      command=self.load_saved_profile).pack(fill="x", padx=10, pady=5)

    def create_main_area(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=20)
        self.main_frame.grid_rowconfigure(0, weight=0) 
        self.main_frame.grid_rowconfigure(1, weight=1) 
        self.main_frame.grid_rowconfigure(2, weight=0) 
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Header
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=50)
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.header_label = ctk.CTkLabel(self.header_frame, text="Hoşgeldiniz", font=ctk.CTkFont(size=20, weight="bold"))
        self.header_label.pack(side="left", padx=10)

        # Scroll Area
        self.scroll_area = ctk.CTkScrollableFrame(self.main_frame)
        self.scroll_area.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

        # Log Panel
        self.bottom_panel = ctk.CTkFrame(self.main_frame, height=120, fg_color="#2b2b2b")
        self.bottom_panel.grid(row=2, column=0, sticky="ew")
        
        self.log_box = ctk.CTkTextbox(self.bottom_panel, height=80, font=("Consolas", 12), text_color="#2ecc71", fg_color="black")
        self.log_box.pack(fill="both", expand=True, padx=10, pady=10)
        self.log("Sistem Hazır.")

    def create_summary_panel(self):
        self.summary_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#212121")
        self.summary_frame.grid(row=0, column=2, sticky="nsew")
        
        ctk.CTkLabel(self.summary_frame, text="İŞLEM KUYRUĞU", font=ctk.CTkFont(size=16, weight="bold"), text_color="#f1c40f").pack(pady=(30, 10))
        
        self.summary_box = ctk.CTkTextbox(self.summary_frame, font=("Consolas", 13), text_color="white", fg_color="transparent")
        self.summary_box.pack(fill="both", expand=True, padx=10, pady=10)
        self.summary_box.configure(state="disabled")

        self.action_frame = ctk.CTkFrame(self.summary_frame, fg_color="transparent")
        self.action_frame.pack(fill="x", padx=10, pady=20)

        self.progress = ctk.CTkProgressBar(self.action_frame)
        self.progress.pack(fill="x", pady=(0, 10))
        self.progress.set(0)

        self.start_btn = ctk.CTkButton(self.action_frame, text="İŞLEMİ BAŞLAT", font=ctk.CTkFont(size=15, weight="bold"),
                                       height=50, fg_color="#27ae60", hover_color="#2ecc71",
                                       command=self.start_processing)
        self.start_btn.pack(fill="x", pady=5)
        
        ctk.CTkButton(self.action_frame, text="Explorer Restart", fg_color="#d35400", hover_color="#e67e22",
                      command=lambda: (backend.restart_explorer(), self.log("Explorer yeniden başlatıldı."))).pack(fill="x", pady=5)

    def log(self, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"> {msg}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def clear_scroll_area(self):
        for widget in self.scroll_area.winfo_children(): widget.destroy()
    
    def clear_header(self):
        for widget in self.header_frame.winfo_children():
            if widget != self.header_label: widget.destroy()

    # --- DASHBOARD PAGE ---
    def show_dashboard_page(self):
        self.current_page_type = "dashboard"
        self.clear_scroll_area()
        self.clear_header()
        self.header_label.configure(text="📊 Sistem İzleme Paneli")
        
        self.scroll_area.grid_columnconfigure(0, weight=1)
        self.scroll_area.grid_columnconfigure(1, weight=1)
        self.scroll_area.grid_columnconfigure(2, weight=1)

        # 1. Row: Resource Usage
        self.card_cpu = self.create_stat_card(0, 0, "CPU Kullanımı", "0%", "#e74c3c")
        self.card_ram = self.create_stat_card(0, 1, "RAM Kullanımı", "0 GB", "#3498db")
        self.card_disk = self.create_stat_card(0, 2, "Disk (C:)", "0 GB Boş", "#2ecc71")

        # 2. Row: System Info
        info_frame = ctk.CTkFrame(self.scroll_area, fg_color="#212121")
        info_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=20)
        
        sys_info = backend.get_system_info()
        self.create_info_label(info_frame, "🖥️ Bilgisayar Adı:", sys_info["hostname"], 0, 0)
        self.create_info_label(info_frame, "🪟 İşletim Sistemi:", sys_info["os"], 0, 1)
        self.create_info_label(info_frame, "⏱️ Açık Kalma Süresi:", sys_info["uptime"], 1, 0)
        self.create_info_label(info_frame, "🌐 Yerel IP:", sys_info["ip"], 1, 1)

        self.update_dashboard_loop()

    def create_stat_card(self, row, col, title, initial_val, color):
        card = ctk.CTkFrame(self.scroll_area, fg_color="#2b2b2b", corner_radius=10)
        card.grid(row=row, column=col, sticky="ew", padx=10, pady=10)
        
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14, weight="bold"), text_color="gray").pack(pady=(15,0))
        lbl_value = ctk.CTkLabel(card, text=initial_val, font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        lbl_value.pack(pady=5)
        
        progress = ctk.CTkProgressBar(card, orientation="horizontal", height=15, progress_color=color)
        progress.pack(fill="x", padx=20, pady=(0, 20))
        progress.set(0)
        return {"label": lbl_value, "progress": progress}

    def create_info_label(self, parent, title, value, row, col):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.grid(row=row, column=col, sticky="w", padx=40, pady=15)
        ctk.CTkLabel(f, text=title, font=ctk.CTkFont(weight="bold"), text_color="gray").pack(anchor="w")
        ctk.CTkLabel(f, text=value, font=ctk.CTkFont(size=14)).pack(anchor="w")

    def update_dashboard_loop(self):
        if self.current_page_type != "dashboard": return
        stats = backend.get_system_stats()
        
        self.card_cpu["progress"].set(stats["cpu"] / 100)
        self.card_cpu["label"].configure(text=f"%{stats['cpu']}")
        
        self.card_ram["progress"].set(stats["ram_percent"] / 100)
        self.card_ram["label"].configure(text=stats["ram_text"])
        
        self.card_disk["progress"].set(stats["disk_percent"] / 100)
        self.card_disk["label"].configure(text=f"%{stats['disk_percent']}")
        
        self.after(2000, self.update_dashboard_loop)

    # --- OTHER PAGES ---
    def show_category_page(self, category_name):
        self.current_page_type = "install"
        self.clear_header()
        self.header_label.configure(text=category_name)
        self.clear_scroll_area()
        self.scroll_area.grid_columnconfigure(0, weight=1)
        self.scroll_area.grid_columnconfigure(1, weight=1)

        row, col = 0, 0
        apps_in_cat = {k:v for k,v in self.app_vars.items() if v["cat"] == category_name}

        for name, data in apps_in_cat.items():
            card = ctk.CTkFrame(self.scroll_area, fg_color="#3a3a3a")
            card.grid(row=row, column=col, sticky="ew", padx=10, pady=10)
            ctk.CTkCheckBox(card, text=name, variable=data["var"], font=ctk.CTkFont(size=13, weight="bold"),
                            checkbox_width=24, checkbox_height=24, command=self.update_summary).pack(anchor="w", padx=15, pady=15)
            col += 1
            if col > 1: col, row = 0, row + 1

    def show_tweaks_page(self):
        self.current_page_type = "tweak"
        self.clear_header()
        self.header_label.configure(text="⚙️ Windows Sistem Ayarları")
        self.clear_scroll_area()
        self.scroll_area.grid_columnconfigure(0, weight=1)
        self.scroll_area.grid_columnconfigure(1, weight=0)

        for name, data in self.tweak_vars.items():
            frame = ctk.CTkFrame(self.scroll_area, fg_color="#3a3a3a")
            frame.pack(fill="x", padx=10, pady=10)
            ctk.CTkLabel(frame, text=name, font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=20, pady=15)
            ctk.CTkSwitch(frame, text="", variable=data["var"], onvalue=1, offvalue=0, 
                          progress_color="#3498db", command=self.update_summary).pack(side="right", padx=20)

    def show_uninstall_page(self):
        self.current_page_type = "uninstall"
        self.clear_scroll_area()
        self.clear_header()
        self.header_label.configure(text="🗑️ Program Kaldırıcı")

        self.refresh_btn = ctk.CTkButton(self.header_frame, text="🔄 Listeyi Getir", width=150, 
                                         command=self.load_installed_apps_thread)
        self.refresh_btn.pack(side="right", padx=10)

        self.search_entry = ctk.CTkEntry(self.header_frame, placeholder_text="🔍 Uygulama Ara...", width=250, height=35, corner_radius=20)
        self.search_entry.pack(side="right", padx=10)
        self.search_entry.bind("<KeyRelease>", self.filter_installed_apps)

        ctk.CTkLabel(self.scroll_area, text="Yüklü programları listelemek için butona basın.", font=ctk.CTkFont(size=14)).pack(pady=50)

    def show_startup_page(self):
        self.current_page_type = "startup"
        self.clear_scroll_area()
        self.clear_header()
        self.header_label.configure(text="🚀 Başlangıç (Startup) Yöneticisi")

        self.refresh_btn = ctk.CTkButton(self.header_frame, text="🔄 Analiz Et", width=150, 
                                         command=self.load_startup_items_thread)
        self.refresh_btn.pack(side="right", padx=10)

        ctk.CTkLabel(self.scroll_area, text="Bilgisayar açılırken çalışan programlar burada listelenir.\nGereksizleri kapatarak açılışı hızlandırın.", 
                     font=ctk.CTkFont(size=14), text_color="gray").pack(pady=20)

    def show_cleaner_page(self):
        self.current_page_type = "cleaner"
        self.clear_scroll_area()
        self.clear_header()
        self.header_label.configure(text="🧹 Sistem Temizliği")
        
        self.cleaner_options = [
            {"id": "temp", "name": "Geçici Dosyalar (Temp)", "desc": "Uygulamaların bıraktığı gereksiz dosyalar."},
            {"id": "prefetch", "name": "Windows Prefetch", "desc": "Eski önyükleme kayıtları (Sistemi hızlandırabilir)."},
            {"id": "dns", "name": "DNS Önbelleği", "desc": "İnternet bağlantı sorunlarını çözer."},
            {"id": "recycle", "name": "Geri Dönüşüm Kutusu", "desc": "Silinmiş dosyaları tamamen yok eder."},
            {"id": "windows_update", "name": "Windows Update Artıkları", "desc": "Eski güncelleme dosyalarını siler."}
        ]
        
        self.cleaner_vars = {}
        
        self.scroll_area.grid_columnconfigure(0, weight=1)
        
        row = 0
        for item in self.cleaner_options:
            card = ctk.CTkFrame(self.scroll_area, fg_color="#2b2b2b", height=60)
            card.grid(row=row, column=0, sticky="ew", padx=10, pady=5)
            
            # Left: Info
            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", padx=10, pady=5)
            ctk.CTkLabel(info, text=item["name"], font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
            ctk.CTkLabel(info, text=item["desc"], font=ctk.CTkFont(size=11), text_color="gray").pack(anchor="w")
            
            # Right: Selection
            var = ctk.BooleanVar(value=False)
            self.cleaner_vars[item["id"]] = {"var": var, "name": item["name"]}
            
            ctk.CTkCheckBox(card, text="Temizle", variable=var, 
                            fg_color="#9b59b6", hover_color="#8e44ad",
                            command=self.update_summary).pack(side="right", padx=15)
            row += 1

    # --- BUSINESS LOGIC & THREADS ---
    def load_startup_items_thread(self):
        self.refresh_btn.configure(state="disabled", text="Taranıyor...")
        threading.Thread(target=self.load_startup_items).start()

    def load_startup_items(self):
        items = backend.get_startup_items()
        self.after(0, lambda: self.render_startup_items(items))

    def render_startup_items(self, items):
        self.clear_scroll_area()
        self.startup_vars = {}
        
        if not items:
            ctk.CTkLabel(self.scroll_area, text="✅ Başlangıçta çalışan gereksiz program bulunamadı!", font=ctk.CTkFont(size=16)).pack(pady=50)
            self.refresh_btn.configure(state="normal", text="🔄 Yenile")
            return

        self.scroll_area.grid_columnconfigure(0, weight=1)
        row = 0
        for item in items:
            self.create_startup_card(item, row)
            row += 1
        self.refresh_btn.configure(state="normal", text="🔄 Yenile")

    def create_startup_card(self, item, row):
        card = ctk.CTkFrame(self.scroll_area, fg_color="#2b2b2b", height=60)
        card.grid(row=row, column=0, sticky="ew", padx=10, pady=5)
        
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", padx=10, pady=5)
        
        ctk.CTkLabel(info_frame, text=item.get("Name", "Bilinmeyen"), font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(info_frame, text=item.get("Location", "")[:40]+"...", font=ctk.CTkFont(size=11), text_color="gray").pack(anchor="w")

        var = ctk.BooleanVar(value=False)
        unique_id = f"{item['Name']}|{item['Location']}"
        self.startup_vars[unique_id] = {"var": var, "name": item["Name"], "loc": item["Location"]}

        ctk.CTkCheckBox(card, text="Devre Dışı Bırak", variable=var, fg_color="#e67e22", hover_color="#d35400",
                        command=self.update_summary).pack(side="right", padx=15)

    def load_installed_apps_thread(self):
        self.refresh_btn.configure(state="disabled", text="Taranıyor...")
        threading.Thread(target=self.load_installed_apps).start()

    def load_installed_apps(self):
        apps = backend.get_installed_apps()
        self.installed_apps_data = apps
        self.after(0, self.render_installed_apps)

    def render_installed_apps(self):
        self.clear_scroll_area()
        self.uninstall_vars = {}
        self.scroll_area.grid_columnconfigure(0, weight=1)
        self.scroll_area.grid_columnconfigure(1, weight=1)
        row, col = 0, 0
        for app in self.installed_apps_data:
            self.create_uninstall_card(app, row, col)
            col += 1
            if col > 1: col, row = 0, row + 1
        self.refresh_btn.configure(state="normal", text="🔄 Yenile")

    def create_uninstall_card(self, app, row, col):
        card = ctk.CTkFrame(self.scroll_area, fg_color="#2b2b2b", border_width=1, border_color="#c0392b", corner_radius=8) 
        card.grid(row=row, column=col, sticky="ew", padx=8, pady=6)
        
        var = ctk.BooleanVar(value=False)
        self.uninstall_vars[app["name"]] = {"var": var, "id": app["name"]}

        cb = ctk.CTkCheckBox(card, text=f"{app['name'][:25]}...", variable=var, text_color="white",
                             font=ctk.CTkFont(size=13, weight="bold"), hover_color="#c0392b", fg_color="#e74c3c", command=self.update_summary)
        cb.pack(side="left", padx=15, pady=15)
        ctk.CTkLabel(card, text="🗑️", font=ctk.CTkFont(size=16)).pack(side="right", padx=15)

    def filter_installed_apps(self, event=None):
        search_text = self.search_entry.get().lower()
        self.clear_scroll_area()
        self.uninstall_vars = {}
        row, col = 0, 0
        for app in self.installed_apps_data:
            if search_text in app["name"].lower():
                self.create_uninstall_card(app, row, col)
                col += 1
                if col > 1: col, row = 0, row + 1

    # --- UPDATE ALL ---
    def start_update_all_thread(self):
        self.log("🚀 TÜM GÜNCELLEMELER BAŞLATILIYOR...")
        self.start_btn.configure(state="disabled", text="GÜNCELLENİYOR...")
        threading.Thread(target=self.run_update_all).start()

    def run_update_all(self):
        self.log("🔍 Güncellemeler kontrol ediliyor (Biraz sürebilir)...")
        
        updates = backend.check_for_updates()
        
        if not updates:
            self.log("✅ Sisteminiz güncel! Güncellenecek paket bulunamadı.")
            self.start_btn.configure(state="normal", text="İŞLEMİ BAŞLAT")
            return

        total = len(updates)
        self.log(f"📦 Toplam {total} güncelleme bulundu.")
        
        success_count = 0
        for i, app in enumerate(updates):
            # Update Progress Bar
            progress_percent = (i) / total
            self.progress.set(progress_percent)
            
            app_name = app["name"]
            percent_text = int(progress_percent * 100)
            self.start_btn.configure(text=f"GÜNCELLENİYOR... (%{percent_text})")
            
            self.log(f"⬇️ [{i+1}/{total}] İndiriliyor ve Kuruluyor: {app_name}...")
            
            # Send Update Command
            success, output = backend.update_single_package(app_name)
            
            if success:
                self.log(f"✅ GÜNCELLENDİ: {app_name}")
                success_count += 1
            else:
                self.log(f"❌ HATA: {app_name} güncellenemedi.")

        self.progress.set(1)
        self.start_btn.configure(state="normal", text="İŞLEMİ BAŞLAT")
        self.log(f"🎉 İşlem Tamamlandı! ({success_count}/{total} başarılı)")

    # --- PROFILE MANAGEMENT ---
    def save_current_profile(self):
        profile_data = {
            "apps": [name for name, data in self.app_vars.items() if data["var"].get()],
            "tweaks": [name for name, data in self.tweak_vars.items() if data["var"].get() == 1]
        }
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Dosyası", "*.json")], title="Profili Kaydet")
        if not filepath: return
        success, msg = backend.save_profile(filepath, profile_data)
        self.log(f"💾 {msg}")

    def load_saved_profile(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON Dosyası", "*.json")], title="Profil Yükle")
        if not filepath: return
        success, data = backend.load_profile(filepath)
        if not success:
            self.log("❌ Profil yüklenemedi!")
            return
        
        for val in self.app_vars.values(): val["var"].set(False)
        for val in self.tweak_vars.values(): val["var"].set(0)

        if "apps" in data:
            for name in data["apps"]:
                if name in self.app_vars: self.app_vars[name]["var"].set(True)
        if "tweaks" in data:
            for name in data["tweaks"]:
                if name in self.tweak_vars: self.tweak_vars[name]["var"].set(1)

        self.update_summary()
        self.log(f"✅ Profil yüklendi!")

    # --- CORE PROCESSING LOGIC ---
    def update_summary(self):
        text = ""
        count = 0
        
        selected_apps = [name for name, data in self.app_vars.items() if data["var"].get()]
        if selected_apps:
            text += "--- KURULACAK ---\n" + "\n".join([f"✅ {x}" for x in selected_apps]) + "\n\n"
            count += len(selected_apps)

        selected_un = [name for name, data in self.uninstall_vars.items() if data["var"].get()]
        if selected_un:
            text += "--- KALDIRILACAK ---\n" + "\n".join([f"🗑️ {x}" for x in selected_un]) + "\n\n"
            count += len(selected_un)
        
        if hasattr(self, 'startup_vars'):
            selected_startup = [data["name"] for uid, data in self.startup_vars.items() if data["var"].get()]
            if selected_startup:
                text += "--- BAŞLANGIÇTAN SİL ---\n" + "\n".join([f"🛑 {x}" for x in selected_startup]) + "\n\n"
                count += len(selected_startup)

        if hasattr(self, 'cleaner_vars'):
            selected_clean = [data["name"] for uid, data in self.cleaner_vars.items() if data["var"].get()]
            if selected_clean:
                text += "--- TEMİZLİK ---\n" + "\n".join([f"✨ {x}" for x in selected_clean]) + "\n\n"
                count += len(selected_clean)

        active_tweaks = [name for name, data in self.tweak_vars.items() if data["var"].get() == 1]
        if active_tweaks:
            text += "--- AYARLAR ---\n" + "\n".join([f"⚙️ {x}" for x in active_tweaks]) + "\n"
            count += len(active_tweaks)

        if count == 0: text = "Henüz seçim yapılmadı."
        
        self.summary_box.configure(state="normal")
        self.summary_box.delete("0.0", "end")
        self.summary_box.insert("0.0", text)
        self.summary_box.configure(state="disabled")

    def start_processing(self):
        tasks = []
        for name, data in self.app_vars.items():
            if data["var"].get(): tasks.append({"type": "app", "name": name, "id": data["id"]})
        
        for name, data in self.tweak_vars.items():
            state = data["var"].get()
            tasks.append({"type": "tweak", "name": name, "cmds": data["cmds"], "state": state})

        for name, data in self.uninstall_vars.items():
            if data["var"].get(): tasks.append({"type": "uninstall", "name": name, "id": data["id"]})

        if hasattr(self, 'startup_vars'):
            for uid, data in self.startup_vars.items():
                if data["var"].get():
                    tasks.append({"type": "startup", "name": data["name"], "loc": data["loc"]})

        if hasattr(self, 'cleaner_vars'):
            for uid, data in self.cleaner_vars.items():
                if data["var"].get():
                    tasks.append({"type": "clean", "id": uid, "name": data["name"]})

        if not tasks:
            self.log("Liste boş.")
            return

        threading.Thread(target=self.run_tasks, args=(tasks,)).start()

    def run_tasks(self, tasks):
        self.start_btn.configure(state="disabled")
        self.log(f"--- {len(tasks)} İşlem Başlatıldı ---")
        
        total = len(tasks)
        for i, task in enumerate(tasks):
            self.progress.set((i+1)/total)
            
            if task["type"] == "app":
                self.log(f"📦 İndiriliyor: {task['name']}...")
                success, _ = backend.install_package(task["id"])
                self.log(f"✅ OK: {task['name']}" if success else f"❌ HATA: {task['name']}")

            elif task["type"] == "tweak":
                state = task["state"]
                cmd = task["cmds"]["on"] if state == 1 else task["cmds"]["off"]
                backend.run_command(cmd)

            elif task["type"] == "uninstall":
                self.log(f"🗑️ Kaldırılıyor: {task['name']}...")
                success, _ = backend.uninstall_package(task["name"])
                self.log(f"✅ SİLİNDİ: {task['name']}" if success else f"❌ HATA: {task['name']}")

            elif task["type"] == "startup":
                self.log(f"🛑 Devre dışı bırakılıyor: {task['name']}...")
                success, msg = backend.remove_startup_item(task["name"], task["loc"])
                if success: self.log(f"✅ SİLİNDİ: {task['name']}")
                else: self.log(f"❌ HATA: {task['name']}")

            elif task["type"] == "clean":
                self.log(f"🧹 Temizleniyor: {task['name']}...")
                success, msg = backend.clean_item(task["id"])
                if success: self.log(f"✅ {msg}")
                else: self.log(f"❌ {msg}")

        self.log("🎉 Bitti!")
        self.start_btn.configure(state="normal")
        self.progress.set(1)