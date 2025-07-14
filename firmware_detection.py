# firmware_gui_streamlit.py
import streamlit as st

# --------------------------- Simulated Data ---------------------------

KNOWN_GOOD_GUIDS = {
    "7C79AC8C-5FA3-4E73-8D46-97859C5D2C0E",
    "F0A30A0F-2D28-4212-81B9-46A3C3ABFE2D",
    "A1B2C3D4-E5F6-7890-1234-56789ABCDEF0"
}

FOUND_GUIDS = [
    "7C79AC8C-5FA3-4E73-8D46-97859C5D2C0E",
    "E4C1F23A-1C45-4829-9E14-B12345678901"
]

DXE_PAYLOADS = {
    "trusted_driver.bin": "clean",
    "malicious_dxe.bin": "moonbounce_behavior_detected"
}

UEFI_VARS = {
    "BootOrder": "normal",
    "LoJaxVar": "boot_redirection_enabled"
}

SPI_FLASH_HASH = "abcd1234"
GOLDEN_IMAGE_HASH = "abcd5678"

# --------------------------- Detection Logic ---------------------------

def baseline_checker():
    log = ["[GUID CHECK]"]
    for guid in FOUND_GUIDS:
        if guid in KNOWN_GOOD_GUIDS:
            log.append(f"✔ GUID {guid} is safe.")
        else:
            log.append(f"⚠ Unknown GUID {guid} found! Possible injected driver.")
    return log

def dxe_payload_scanner():
    log = ["\n[DXE PAYLOAD SCAN]"]
    for fname, status in DXE_PAYLOADS.items():
        if status == "clean":
            log.append(f"✔ {fname}: clean.")
        elif status == "moonbounce_behavior_detected":
            log.append(f"❗ {fname}: matches MoonBounce malware behavior!")
    return log

def nvram_variable_checker():
    log = ["\n[UEFI VARIABLE SCAN]"]
    for var, val in UEFI_VARS.items():
        if var.lower() == "lojaxvar":
            log.append(f"❗ UEFI var '{var}' indicates LoJax-style persistence!")
        else:
            log.append(f"✔ UEFI var '{var}': normal.")
    return log

def spi_flash_integrity_check():
    log = ["\n[SPI FLASH INTEGRITY]"]
    if SPI_FLASH_HASH != GOLDEN_IMAGE_HASH:
        log.append("❗ Firmware hash mismatch detected! Flash may be tampered.")
    else:
        log.append("✔ SPI flash hash matches expected baseline.")
    return log

def run_full_scan():
    log = []
    log += baseline_checker()
    log += dxe_payload_scanner()
    log += nvram_variable_checker()
    log += spi_flash_integrity_check()
    log.append("\n[SCAN COMPLETE]")
    return "\n".join(log)

# --------------------------- Streamlit UI ---------------------------

def firmware_scan_ui():
    st.header("🔍 Firmware Sentinel - UEFI Malware Detection")

    # Initialize session state variable if not already
    if "firmware_log" not in st.session_state:
        st.session_state.firmware_log = ""

    # Run scan when button is clicked
    if st.button("🔍 Run Firmware Scan"):
        with st.spinner("Scanning..."):
            st.session_state.firmware_log = run_full_scan()
            st.success("Scan complete!")

    # Display log and download only if scan has been run
    if st.session_state.firmware_log:
        st.code(st.session_state.firmware_log)
        st.download_button(
            label="📁 Download Log",
            data=st.session_state.firmware_log,
            file_name="firmware_log.txt",
            mime="text/plain"
        )

# Call the UI function to display the Streamlit application
if __name__ == "__main__":
    firmware_scan_ui()