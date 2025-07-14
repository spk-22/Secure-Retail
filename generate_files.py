# generate_files.py
files = {
    "baseline_firmware.bin": b"BASELINE_FIRMWARE_IMAGE_" + b"\x00" * 100,
    "lojax_modified.bin": b"LOJAX_ATTACK_VECTOR_" + b"\x01" * 100,
    "moonbounce_modified.bin": b"MOONBOUNCE_ATTACK_VECTOR_" + b"\x02" * 100,
    "boothole_modified.bin": b"BOOTHOLE_ATTACK_VECTOR_" + b"\x03" * 100,
    "evil_maid_modified.bin": b"EVIL_MAID_ATTACK_VECTOR_" + b"\x04" * 100,
}

for filename, content in files.items():
    with open(filename, "wb") as f:
        f.write(content)

print("✅ Firmware files generated.")
