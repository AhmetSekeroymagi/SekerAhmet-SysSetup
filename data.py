SOFTWARE_DB = {
    "Web Tarayıcılar": {
        "Google Chrome": "Google.Chrome",
        "Mozilla Firefox": "Mozilla.Firefox",
        "Microsoft Edge": "Microsoft.Edge",
        "Brave": "Brave.Brave",
        "Opera GX": "Opera.OperaGX"
    },
    "Geliştirme & IDE": {
        "Visual Studio 2022": "Microsoft.VisualStudio.2022.Community",
        "VS Code": "Microsoft.VisualStudioCode",
        "Cursor": "Anysphere.Cursor",
        "Android Studio": "Google.AndroidStudio",
        "IntelliJ IDEA": "JetBrains.IntelliJ.IDEA.Community",
        "PyCharm": "JetBrains.PyCharm.Community",
        "Unity Hub": "Unity.UnityHub"
    },
    "DevOps & Sanallaştırma": {
        "Docker Desktop": "Docker.DockerDesktop",
        "VirtualBox": "Oracle.VirtualBox",
        "VMware Player": "VMware.WorkstationPlayer",
        "PuTTY": "PuTTY.PuTTY",
        "FileZilla": "FileZilla.FileZilla",
        "Cisco Packet Tracer": "Cisco.PacketTracer"
    },
    "Veritabanı & API": {
        "SQL Server (SSMS)": "Microsoft.SQLServerManagementStudio",
        "DBeaver": "dbeaver.dbeaver",
        "Postman": "Postman.Postman",
        "MongoDB Compass": "MongoDB.Compass.Full",
        "SQLite Studio": "SalDonald.SQLiteStudio"
    },
    "Diller & Runtime": {
        "Python 3.12": "Python.Python.3.12",
        "Node.js LTS": "OpenJS.NodeJS.LTS",
        "Git": "Git.Git",
        "GitHub Desktop": "GitHub.GitHubDesktop",
        "Java JDK 21": "Oracle.JDK.21",
        "Go Lang": "GoLang.Go"
    },
    "İletişim & Ofis": {
        "Discord": "Discord.Discord",
        "Microsoft Teams": "Microsoft.Teams",
        "Zoom": "Zoom.Zoom",
        "Slack": "SlackTechnologies.Slack",
        "LibreOffice": "TheDocumentFoundation.LibreOffice"
    },
    "Araçlar & Sıkıştırma": {
        "7-Zip": "7zip.7zip",
        "WinRAR": "RARLab.WinRAR",
        "AnyDesk": "AnyDeskSoftwareGmbH.AnyDesk",
        "TeamViewer": "TeamViewer.TeamViewer",
        "PowerToys": "Microsoft.PowerToys"
    }
}

SYSTEM_TWEAKS = {
    "Dosya Uzantılarını Göster": {
        "on": 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v HideFileExt /t REG_DWORD /d 0 /f',
        "off": 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v HideFileExt /t REG_DWORD /d 1 /f'
    },
    "Gizli Dosyaları Göster": {
        "on": 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v Hidden /t REG_DWORD /d 1 /f',
        "off": 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v Hidden /t REG_DWORD /d 0 /f'
    },
    "Bu Bilgisayar Masaüstünde": {
        "on": 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\HideDesktopIcons\\NewStartPanel" /v "{20D04FE0-3AEA-1069-A2D8-08002B30309D}" /t REG_DWORD /d 0 /f',
        "off": 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\HideDesktopIcons\\NewStartPanel" /v "{20D04FE0-3AEA-1069-A2D8-08002B30309D}" /t REG_DWORD /d 1 /f'
    },
    "Karanlık Mod (Full)": {
        "on": 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v AppsUseLightTheme /t REG_DWORD /d 0 /f && reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v SystemUsesLightTheme /t REG_DWORD /d 0 /f',
        "off": 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v AppsUseLightTheme /t REG_DWORD /d 1 /f && reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v SystemUsesLightTheme /t REG_DWORD /d 1 /f'
    },
    "Saniye Bilgisini Göster": {
        "on": 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v ShowSecondsInSystemClock /t REG_DWORD /d 1 /f',
        "off": 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v ShowSecondsInSystemClock /t REG_DWORD /d 0 /f'
    },
    "Klasik Sağ Tık (Win11)": {
        "on": 'reg add "HKCU\\Software\\Classes\\CLSID\\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\\InprocServer32" /f /ve',
        "off": 'reg delete "HKCU\\Software\\Classes\\CLSID\\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}" /f'
    }
}