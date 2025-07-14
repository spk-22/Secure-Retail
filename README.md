# SecureCart
Advanced Firmware Threat Detection and Application-Layer Security

---

## Overview

SecureWalmart Suite is a dual-module security system designed to protect both hardware-level infrastructure and application-level activities in a retail environment.

It consists of:

- **Firmware Sentinel** – A bootable Linux-based scanning tool that simulates detection of firmware threats like LoJax and MoonBounce.
- **Retail Trust Shield** – A Streamlit-based dashboard for monitoring admin activity, payment integrity, and customer-side behavioral anomalies.

---

## Part 1: Firmware Sentinel (Bootable Linux Environment)

### Purpose


This tool initiates a detection workflow to identify advanced threats like LoJax and MoonBounce, which reside in the SPI flash memory and persist below the operating system.

It is designed to interface with low-level tools such as `CHIPSEC` or `flashrom` when run in a privileged Linux environment (e.g., bootable Ubuntu USB). The tool simulates UEFI module analysis, integrity verification, and log generation.

It provides a viable framework for future extension into real-time hardware-integrated detection.

---

### Setup Instructions

#### Step 1: Requirements

- Ubuntu ISO (22.04 LTS or later): https://ubuntu.com/download/desktop  
- USB drive (minimum 8 GB)  
- Bootable USB creator (Rufus or BalenaEtcher)  
- Internet access during session (optional)  

---

#### Step 2: Create a Bootable USB

1. Use Rufus or BalenaEtcher to flash the Ubuntu ISO to your USB.
2. Boot the target system from USB.
3. Choose **"Try Ubuntu"** when prompted.

---

#### Step 3: Install Environment Tools

Once booted into Ubuntu, open the terminal and run:

```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install streamlit
```

---

#### Step 4: Clone the Project and Run the Firmware Tool

```bash
git clone https://github.com/yourusername/securewalmart-suite.git
cd securewalmart-suite
python3 firmware_sentinel.py
```

This tool will:

- Simulate scanning of UEFI modules  
- Flag unknown GUIDs and modified firmware sections  
- Generate logs under the `logs/` directory  

These logs can be imported into the dashboard for further analysis.

---

## Part 2: Retail Trust Shield (Admin & Customer-Facing Simulation)

### Purpose

Retail Trust Shield is a frontend dashboard for simulating modern application-layer protections such as:

- Admin anomaly detection  
- Honeypot login monitoring  
- Secure payment tracking via hashing  
- Customer behavior monitoring via biometrics  
- Dynamic MFA triggers  

---

### Setup Instructions

#### Step 1: Install Streamlit

If Streamlit is not already installed, run:

```bash
pip3 install streamlit
```

---

#### Step 2: Run the Application

From the root project directory:

```bash
cd securewalmart-suite
streamlit run main_app.py
```

---

## Dashboard Features

### Page 1: Firmware Log Viewer

- Upload logs from the Firmware Sentinel tool  
- Parse and display suspicious GUIDs  
- Simulate forensic analysis of SPI flash data  

---

### Page 2: Retail Trust Shield

- Admin login anomaly detection using simulated LLM analysis  
- Honeypot ports for threat diversion  
- Payment integrity checks via hash comparison  
- Behavioral biometric tracking (typing, movement simulation)  
- Smart MFA triggering and session revalidation  

---

## Tech Stack

- Python 3.x  
- Tkinter (firmware GUI)  
- Streamlit (dashboard UI)  
- JSON/text log simulation  
- Simulated GPT/LLM anomaly engine  
- Behavioral biometrics (mocked patterns)

---

## Future Enhancements

- Real CHIPSEC + SPI flash integrations  
- TPM-backed boot validation  
- True LLM-based log parsing  
- Unified timeline visualization across both tools  

---

## Conclusion

SecureCart models a multi-layered defense system that:

- Scans deep firmware components from a secure environment  
- Protects frontend admin and customer interfaces from misuse and fraud  

Together, the suite delivers protection from power-on to checkout.
