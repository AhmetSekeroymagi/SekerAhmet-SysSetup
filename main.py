import sys
import backend
from gui import SysSetupApp

if __name__ == "__main__":
    if not backend.is_admin():
        backend.restart_as_admin()
    else:
        app = SysSetupApp()
        app.mainloop()