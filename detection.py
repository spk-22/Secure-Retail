# detection.py
import hashlib
import shutil

baseline_file = "baseline_firmware.bin"
files = [
    ("lojax_modified.bin", "LoJax"),
    ("moonbounce_modified.bin", "MoonBounce"),
    ("boothole_modified.bin", "BootHole"),
    ("evil_maid_modified.bin", "Evil Maid")
]

with open(baseline_file, "rb") as f:
    BASELINE_HASH = hashlib.sha256(f.read()).hexdigest()

def hash_file(filename):
    with open(filename, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def recover_file(filename):
    shutil.copy(baseline_file, filename)

def check_and_recover():
    result = []
    for filename, label in files:
        current_hash = hash_file(filename)
        if current_hash != BASELINE_HASH:
            recover_file(filename)
            result.append((label, "Compromised", "Recovered"))
        else:
            result.append((label, "Safe", ""))
    return result
