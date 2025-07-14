# admin_features.py
import datetime
import random
import hashlib
import streamlit as st # Streamlit might not be needed directly here, but often used for session_state in broader apps
import pandas as pd

def get_admin_action_logs():
    """Simulates fetching admin action logs."""
    logs = [
        {"timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S"),
         "user": "alice", "action": "Accessed sales reports", "status": "Success"},
        {"timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S"),
         "user": "bob", "action": "Modified product pricing", "status": "Success"},
        {"timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S"),
         "user": "charlie", "action": "Attempted to download customer data", "status": "Blocked - Insufficient Permissions"},
        {"timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M:%S"),
         "user": "alice", "action": "Updated security settings", "status": "Success"},
    ]
    return logs

def simulate_zero_trust_check(user_id, device_id, location):
    """Simulates Zero Trust Access Control checks and displays real-time stats."""
    st.markdown(f"#### Zero Trust Check for **{user_id}** at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_passed = True

    # Simulate TPM check
    tpm_status = "🟢 Passed (Simulated TPM Check)"
    st.write(tpm_status)
    
    # Simulate Geo-location check
    current_location = "Bengaluru, Karnataka, India"
    if "Bengaluru" in location or "Bengaluru" in current_location:
        geo_status = f"🟢 Passed (Geo-location: Access from {location} / Current: {current_location})"
    else:
        geo_status = f"🔴 Failed (Geo-location: Access from {location} / Current: {current_location} - Outside Allowed Area)"
        all_passed = False
    st.write(geo_status)

    # Simulate Device Check (randomly pass/fail for demo)
    if random.random() > 0.2: # 80% chance to pass
        device_status = "🟢 Passed (Device ID: Trusted)"
    else:
        device_status = "🔴 Failed (Device ID: Untrusted)"
        all_passed = False
    st.write(device_status)

    if all_passed:
        st.success(f"✅ Zero Trust Access Granted for {user_id}!")
    else:
        st.error(f"❌ Zero Trust Access Denied for {user_id}!")

    return tpm_status, geo_status, device_status


def get_incoming_payments_summary():
    """Simulates a summary of incoming payments."""
    payments = {
        "Total Daily Revenue": "$15,230.50",
        "Transactions Today": 185,
        "Average Transaction Value": "$82.33",
        "Payment Method Breakdown": {
            "Credit Card": "65%",
            "Debit Card": "20%",
            "Mobile Wallet": "10%",
            "Cash": "5%"
        }
    }
    return payments

# Global list to store transactions for simulation
_TRANSACTION_LOGS = []

def generate_single_transaction_data():
    """Generates a single simulated transaction with both plain and hashed details."""
    customer_names = ["Alice Smith", "Bob Johnson", "Charlie Brown", "Diana Prince", "Ethan Hunt"]
    payment_methods = ["Visa ending 1234", "Mastercard ending 5678", "Amex ending 9012", "RuPay ending 3456", "UPI ID: example@upi"]
    
    customer = random.choice(customer_names)
    plain_payment_detail = random.choice(payment_methods)
    amount = f"${random.randint(10, 500)}.00"
    
    hashed_credential = hashlib.sha256(plain_payment_detail.encode()).hexdigest()
    
    return {
        "plain": {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "customer_name": customer,
            "amount": amount,
            "payment_method": plain_payment_detail,
            "status": "Completed"
        },
        "hashed": {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "customer_name": customer,
            "amount": amount,
            "payment_credential_hash": hashed_credential,
            "status": "Completed"
        }
    }

def get_hashed_transaction_logs(new_transaction_hashed=None):
    """
    Simulates a log of transactions with hashed payment credentials.
    Can append a new transaction for real-time simulation.
    """
    global _TRANSACTION_LOGS # Access the global list

    if not _TRANSACTION_LOGS: # Initialize if empty
        customer_names = ["Alice Smith", "Bob Johnson", "Charlie Brown", "Diana Prince", "Ethan Hunt"]
        payment_methods = ["Visa ending 1234", "Mastercard ending 5678", "Amex ending 9012", "RuPay ending 3456", "UPI ID: example@upi"]
        
        for i in range(5): # Start with 5 initial transactions
            customer = random.choice(customer_names)
            payment_detail = random.choice(payment_methods)
            hashed_credential = hashlib.sha256(payment_detail.encode()).hexdigest()
            _TRANSACTION_LOGS.append({
                "timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=random.randint(1, 60))).strftime("%Y-%m-%d %H:%M:%S"),
                "customer_name": customer,
                "amount": f"${random.randint(10, 500)}.00",
                "payment_credential_hash": hashed_credential,
                "status": "Completed"
            })
        _TRANSACTION_LOGS.sort(key=lambda x: x['timestamp'], reverse=True) # Sort initial logs

    if new_transaction_hashed:
        _TRANSACTION_LOGS.insert(0, new_transaction_hashed) # Add new transaction to the top

    return _TRANSACTION_LOGS

def generate_device_fingerprint(user_agent, ip_address):
    """Simulates generating a unique device fingerprint."""
    raw_fingerprint = f"{user_agent}-{ip_address}-{random.randint(10000, 99999)}"
    return hashlib.sha256(raw_fingerprint.encode()).hexdigest()