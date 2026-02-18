import ctypes
import sys

if sys.platform != "win32":
    print("[XboxGame] Not running on Windows. Xbox Game Mode not available.")
else:
    kernel32 = ctypes.windll.kernel32
    shell32 = ctypes.windll.shell32

    # Constants
    HIGH_PRIORITY_CLASS = 0x00000080
    PROCESS_ALL_ACCESS = 0x1F0FFF

    def set_game_mode(app_id="DazhoGames.Launcher"):
        """
        ست کردن پروسس فعلی (لانچر) به عنوان Game برای Xbox Game Bar / Game Mode
        """
        try:
            # ست کردن AppUserModelID
            shell32.SetCurrentProcessExplicitAppUserModelID(ctypes.c_wchar_p(app_id))
            # افزایش priority
            kernel32.SetPriorityClass(kernel32.GetCurrentProcess(), HIGH_PRIORITY_CLASS)
            print("[XboxGame] Current process set as Game successfully!")
        except Exception as e:
            print(f"[XboxGame] Failed to set Game Mode: {e}")

    def set_game_mode_for_pid(pid, app_id="DazhoGames.Launcher"):
        """
        ست کردن پروسس دیگر (مثل Dolphin.exe) به عنوان Game
        """
        try:
            # باز کردن پروسس
            hProc = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
            if not hProc:
                print(f"[XboxGame] Failed to open process PID {pid}")
                return

            # Set AppUserModelID
            shell32.SetCurrentProcessExplicitAppUserModelID(ctypes.c_wchar_p(app_id))

            # می‌تونی priority رو هم روی پروسس فرزند ست کنی
            kernel32.SetPriorityClass(hProc, HIGH_PRIORITY_CLASS)

            kernel32.CloseHandle(hProc)
            print(f"[XboxGame] PID {pid} set as Game successfully!")
        except Exception as e:
            print(f"[XboxGame] Failed to set Game Mode for PID {pid}: {e}")
