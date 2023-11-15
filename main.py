# Spawning JVM process with following configuration...
import os
import time
import subprocess
import ctypes
import sys

WLAN = "WLAN"


def run_as_admin():
    if sys.platform.startswith('win'):
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        except Exception as e:
            print(e)
            return False
        else:
            return True
    return False


if not ctypes.windll.shell32.IsUserAnAdmin():
    run_as_admin()
    sys.exit()

print("LunarBypasser | v1.0")
print("Author: HShiDianLu. (2023.11)")
print("Notice that this program will rewrite Lunar Client log file.")
print()

print("Connecting network...", end=" ")
result = subprocess.run("netsh interface set interface " + WLAN + " admin=enable", capture_output=True, text=True)
if result.returncode == 0:
    print("[Done]")
    print("Network connected.")
else:
    print("[Error]")
    print("Network connect failed:", result)
print("Initializing...", end=" ")
user_dir = os.path.expanduser("~")
f = open(user_dir + "/.lunarclient/logs/launcher/main.log", "r").read().replace(
    "Spawning JVM process with following configuration...", "")
w = open(user_dir + "/.lunarclient/logs/launcher/main.log", "w")
w.write(f)
w.close()
print("[Done]")
print("Ready to bypass. Launch the game to start bypassing.")

times = 0
wait = 600
while True:
    times += 1
    if times > wait:
        print("It seems that the game has not launched yet. Launch the game to start bypassing.")
        times = 0
        wait *= 2
    fn = open(user_dir + "/.lunarclient/logs/launcher/main.log", "r").read()
    if "Spawning JVM process with following configuration..." in fn:
        print()
        print("Detected JVM started.")
        print("Trying to disconnect network...", end=" ")
        result = subprocess.run("netsh interface set interface " + WLAN + " admin=disable", capture_output=True,
                                text=True)
        if result.returncode == 0:
            print("[Done]")
            print("Network disconnected.")
        else:
            print("[Error]")
            print("Network disconnect failed:", result)
        fn = fn.replace("Spawning JVM process with following configuration...", "")
        w = open(user_dir + "/.lunarclient/logs/launcher/main.log", "w")
        w.write(fn)
        w.close()
        print("Timer started(10s)...", end=" ")
        time.sleep(10)
        print("[End]")
        print("Trying to connect network...", end=" ")
        result = subprocess.run("netsh interface set interface " + WLAN + " admin=enable", capture_output=True,
                                text=True)
        if result.returncode == 0:
            print("[Done]")
            print("Network connected.")
        else:
            print("[Error]")
            print("Network connect failed:", result)
        print("Bypassed.")
        print("Press any key to exit.")
        os.system("pause")
        sys.exit()

    time.sleep(0.1)
