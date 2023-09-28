import os
import platform
import re
import shutil
import subprocess

extension = ""
if platform.system() == "Windows":
    extension = ".exe"

TARGET_DIR = "src-tauri/bin"
shutil.rmtree(TARGET_DIR, ignore_errors=True)
# os.makedirs(TARGET_DIR)

os.chdir("py")
subprocess.run(["poetry", "install", "--no-interaction", "--no-ansi"])
env_path = subprocess.run(
    ["poetry", "env", "info", "--path"], capture_output=True, text=True
).stdout.strip()
print(env_path)
shutil.copytree(".", f"../{TARGET_DIR}")
shutil.copytree(env_path, f"../{TARGET_DIR}/env")


rust_info = subprocess.check_output(["rustc", "-vV"]).decode("utf-8")
target_triple = re.search(r"host: (\S+)", rust_info).group(1)
if not target_triple:
    print("Failed to determine platform target triple")

try:
    if extension == ".exe":
        os.mkdir(f"../{TARGET_DIR}/env/bin")
        shutil.copy(
            f"../{TARGET_DIR}/env/Scripts/python.exe",
            f"../{TARGET_DIR}/env/bin/python{'-' if target_triple else ''}{target_triple}{extension}",
        )
        shutil.copy(
            f"../{TARGET_DIR}/env/Scripts/pip.exe",
            f"../{TARGET_DIR}/env/bin/pip{'-' if target_triple else ''}{target_triple}{extension}",
        )
    else:
        shutil.copy(
            f"../{TARGET_DIR}/env/bin/python",
            f"../{TARGET_DIR}/env/bin/python{'-' if target_triple else ''}{target_triple}{extension}",
        )
        shutil.copy(
            f"../{TARGET_DIR}/env/bin/pip",
            f"../{TARGET_DIR}/env/bin/pip{'-' if target_triple else ''}{target_triple}{extension}",
        )
except Exception as e:
    # print current dir
    print(os.getcwd())
    raise e
