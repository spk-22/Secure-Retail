import streamlit as st
from cor import firmware_scan_ui
from detection import check_and_recover
from admin_features import (
    get_admin_action_logs,
    simulate_zero_trust_check,
    get_incoming_payments_summary,
    get_hashed_transaction_logs,
    generate_single_transaction_data,
    generate_device_fingerprint
)
import pandas as pd
import random
import time
import hashlib # For hashing admin inputs

# --- Page Configuration ---
st.set_page_config(
    page_title="Retail Trust Shield",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Enhanced Styling ---
st.markdown(
    """
    <style>
    /* Main app background */
    .main .block-container {
        background-color: white;
        padding: 2rem 1rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f0f2f6;
        padding: 1rem;
    }
    
    /* Common notification styling */
    .st-notification {
        position: fixed;
        padding: 12px 25px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        opacity: 0;
        transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;
        font-size: 15px;
        min-width: 280px;
        text-align: left;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border: 1px solid;
    }
    .st-notification.show {
        opacity: 1;
        transform: translateY(-50%); /* For vertical centering */
    }

    /* Right-middle notifications */
    #right-middle-notification { /* Changed ID for clarity */
        top: 50%; /* Vertically center */
        right: 20px;
        transform: translateY(-50%) translateX(50px); /* Start off-screen to the right */
    }
    #right-middle-notification.show {
        transform: translateY(-50%) translateX(0); /* Slide in */
    }

    /* Close button for notifications */
    .st-notification .close-btn {
        background: none;
        border: none;
        font-size: 20px;
        cursor: pointer;
        padding: 0 5px;
        line-height: 1;
        transition: color 0.2s ease;
        margin-left: 10px; /* Space between text and button */
    }
    .st-notification .close-btn:hover {
        color: #dc3545; /* Red on hover for dismiss */
    }

    /* Specific alert styles */
    .alert-success { background-color: #d4edda; color: #155724; border-color: #c3e6cb; }
    .alert-success .close-btn { color: #155724; }

    .alert-warning { background-color: #fff3cd; color: #856404; border-color: #ffeeba; }
    .alert-warning .close-btn { color: #856404; }

    .alert-danger { background-color: #f8d7da; color: #721c24; border-color: #f5c6cb; }
    .alert-danger .close-btn { color: #721c24; }

    .alert-info {
        background-color: white;
        color: #007bff;
        border-color: #007bff;
    }
    .alert-info .close-btn { color: #007bff; }

    /* For the "Click for details" link within notification */
    .st-notification a {
        color: inherit; /* Inherit text color */
        text-decoration: underline;
        margin-left: 8px;
    }
    .st-notification a:hover {
        opacity: 0.8;
    }

    /* Streamlit specific adjustments */
    div.stButton > button {
        border-radius: 8px;
    }

    /* Enhanced Feature Card Style */
    .feature-card {
        background-color: #f8f9fa; /* Light gray background */
        border-left: 5px solid #007bff; /* Blue left border for accent */
        border-radius: 8px;
        padding: 20px 25px;
        margin-bottom: 25px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        max-width: 100%;
        transition: box-shadow 0.3s ease;
    }
    .feature-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .feature-card p {
        font-size: 1.1em; /* Increased font size for description */
        line-height: 1.7;
        color: #333;
        margin-bottom: 8px;
    }
    .feature-card h4 {
        color: #0056b3; /* Darker blue for headings */
        margin-top: 0;
        margin-bottom: 15px;
        font-size: 1.3em; /* Larger heading for card */
        font-weight: 600;
    }
    .feature-card ul {
        font-size: 1.05em;
        line-height: 1.6;
        color: #444;
        margin-left: 20px;
    }
    .feature-card li {
        margin-bottom: 8px;
    }
    .feature-card strong {
        color: #0056b3;
        font-weight: 600;
    }

    /* Enhanced Home Section Styling */
    .home-hero {
        background: linear-gradient(135deg, #f0f2f6 0%, #e8ecf0 100%);
        padding: 40px 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .home-hero h1 {
        color: #007bff;
        font-size: 3.2em;
        margin-bottom: 15px;
        font-weight: 700;
    }
    .home-hero p {
        font-size: 1.3em;
        color: #555;
        line-height: 1.6;
        max-width: 800px;
        margin: 0 auto;
    }

    /* Enhanced content sections */
    .content-section {
        font-size: 1.15em;
        line-height: 1.8;
        margin-bottom: 30px;
    }
    .content-section h3 {
        color: #007bff;
        font-size: 1.4em;
        margin-top: 25px;
        margin-bottom: 15px;
        font-weight: 600;
    }
    .content-section ul {
        margin-left: 25px;
    }
    .content-section li {
        margin-bottom: 12px;
    }
    .content-section ol {
        margin-left: 25px;
    }
    .content-section ol li {
        margin-bottom: 15px;
    }

    /* Sidebar enhancements */
    .sidebar-score {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .sidebar-score h3 {
        font-size: 1.2em;
        margin-bottom: 10px;
        color: #1976d2;
    }

    /* Style for disabled buttons */
    .stButton > button[data-testid="stFormSubmitButton"],
    .stButton > button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    /* Enhanced metrics styling */
    .metric-container {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --- Notification Functions ---
def show_notification(message, type="info", duration=3):
    """Displays a custom alert at the right-middle position for a duration."""
    notification_id = "right-middle-notification"
    
    script = f"""
    <script>
    var notificationDiv = window.parent.document.getElementById('{notification_id}');
    if (!notificationDiv) {{
        notificationDiv = window.parent.document.createElement('div');
        notificationDiv.id = '{notification_id}';
        notificationDiv.className = 'st-notification';
        window.parent.document.body.appendChild(notificationDiv);
    }}
    
    notificationDiv.innerHTML = '<span>{message}</span><button class="close-btn">&times;</button>';
    notificationDiv.className = `st-notification show alert-{type}`;

    var closeButton = notificationDiv.querySelector('.close-btn');
    if (closeButton) {{
        closeButton.onclick = function() {{
            notificationDiv.className = 'st-notification';
            if (notificationDiv.timeoutId) {{
                clearTimeout(notificationDiv.timeoutId);
            }}
        }};
    }}
    
    if (notificationDiv.timeoutId) {{
        clearTimeout(notificationDiv.timeoutId);
    }}

    notificationDiv.timeoutId = setTimeout(function() {{
        notificationDiv.className = 'st-notification';
        notificationDiv.timeoutId = null;
    }}, {duration * 1000});
    </script>
    """
    st.components.v1.html(script, height=0, width=0)

# --- Enhanced Feature Card Function ---
def feature_card(title, description):
    """Generates a styled card for feature descriptions."""
    st.markdown(f"""
    <div class="feature-card">
        <h4>{title}</h4>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)

# --- Session State Initialization ---
if 'overall_safety_score' not in st.session_state:
    st.session_state.overall_safety_score = 70
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'user_trust_score' not in st.session_state:
    st.session_state.user_trust_score = 70
if 'device_fingerprint' not in st.session_state:
    st.session_state.device_fingerprint = None
if 'last_known_ip' not in st.session_state:
    st.session_state.last_known_ip = "192.168.1.1"
if 'cart_value' not in st.session_state:
    st.session_state.cart_value = 0
if 'items_in_cart' not in st.session_state:
    st.session_state.items_in_cart = 0
if 'original_shipping_address' not in st.session_state:
    st.session_state.original_shipping_address = "123 Main St, Anytown"
if 'original_payment_method' not in st.session_state:
    st.session_state.original_payment_method = "Visa ending 1234"
if 'password_reauth_attempted' not in st.session_state:
    st.session_state.password_reauth_attempted = False
if 'last_simulated_payment' not in st.session_state:
    st.session_state.last_simulated_payment = None
if 'show_payment_details' not in st.session_state:
    st.session_state.show_payment_details = False
if 'last_payment_sim_time' not in st.session_state:
    st.session_state.last_payment_sim_time = time.time()
if 'page' not in st.session_state:
    st.session_state.page = "Home & Demo Guide"
if 'suspicious_shopping_activity_detected' not in st.session_state:
    st.session_state.suspicious_shopping_activity_detected = False
if 'high_priced_only_flag' not in st.session_state:
    st.session_state.high_priced_only_flag = False
if 'low_medium_item_count' not in st.session_state:
    st.session_state.low_medium_item_count = 0
if 'high_priced_item_count' not in st.session_state:
    st.session_state.high_priced_item_count = 0

# --- Handle Query Parameters for Navigation ---
query_params = st.query_params
if 'trigger_payment_details' in query_params and query_params['trigger_payment_details'] == 'true':
    st.session_state.page = "Admin Dashboard"
    st.session_state.show_payment_details = True
    st.query_params.clear()
    st.rerun()

# --- Overall Safety Score Update Function ---
def update_overall_safety_score(change_amount):
    """Updates the overall safety score by a variable amount."""
    current_score = st.session_state.overall_safety_score
    if change_amount > 0:
        actual_change = random.randint(1, change_amount)
    else:
        actual_change = random.randint(change_amount, -1) if change_amount < 0 else 0
    
    new_score = current_score + actual_change
    st.session_state.overall_safety_score = max(0, min(100, new_score))

# --- Automated Payment Simulation Logic (every 20 seconds) ---
current_time = time.time()
if current_time - st.session_state.last_payment_sim_time >= 20:
    new_payment_data = generate_single_transaction_data()
    st.session_state.last_simulated_payment = new_payment_data
    
    get_hashed_transaction_logs(new_payment_data['hashed'])

    action_link = (
        f"<a href='#' onclick='window.location.href = window.location.href.split(\"?\")[0] + \"?trigger_payment_details=true\"; return false;'>"
        f"Click to know more</a>"
    )
    notification_message = (
        f"💰 New Incoming Payment: {new_payment_data['plain']['amount']} from {new_payment_data['plain']['customer_name']}! {action_link}"
    )
    show_notification(notification_message, type="success", duration=7)
    update_overall_safety_score(random.randint(2, 5))
    
    st.session_state.last_payment_sim_time = current_time
    st.rerun()

# --- Enhanced Sidebar with Safety Score ---
score_color = "green"
if st.session_state.overall_safety_score < 40:
    score_color = "red"
elif st.session_state.overall_safety_score < 70:
    score_color = "orange"

st.sidebar.markdown(f"""
<div class="sidebar-score">
    <h3>Overall Safety Score</h3>
    <div style="font-size: 1.5em; font-weight: bold; color: {score_color};">
        {st.session_state.overall_safety_score}/100
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# --- Sidebar Navigation ---
st.sidebar.header("Navigation")
page_selection = st.sidebar.radio("Go to", ["Home & Demo Guide", "Admin Dashboard", "User Features (Shopper/Customer)","Firmware Scanner (Experimental)"], index=["Home & Demo Guide", "Admin Dashboard", "User Features (Shopper/Customer)","Firmware Scanner (Experimental)"].index(st.session_state.page))

if page_selection != st.session_state.page:
    st.session_state.page = page_selection
    st.rerun()

# --- Enhanced Shopping Items Definition ---
SHOPPING_ITEMS = [
    {"name": "USB-C Cable", "price": 15, "type": "daily"},
    {"name": "Phone Case", "price": 25, "type": "daily"},
    {"name": "Wireless Mouse", "price": 40, "type": "daily"},
    {"name": "Bluetooth Speaker", "price": 75, "type": "daily"},
    {"name": "Gaming Headset", "price": 120, "type": "medium"},
    {"name": "Smartwatch", "price": 180, "type": "medium"},
    {"name": "Laptop Backpack", "price": 60, "type": "daily"},
    {"name": "Portable SSD 1TB", "price": 150, "type": "medium"},
    {"name": "Noise-Cancelling Headphones", "price": 250, "type": "medium"},
    {"name": "High-End Gaming Laptop", "price": 1800, "type": "luxury"},
    {"name": "Premium DSLR Camera", "price": 1500, "type": "luxury"},
    {"name": "4K Smart TV 65-inch", "price": 900, "type": "luxury"},
]
# --- Page Content ---
if st.session_state.page == "Home & Demo Guide":
    st.markdown("""
    <div class="home-hero">
        <h1>🛡️ Retail Trust Shield</h1>
        <p>
            <strong>Your comprehensive cybersecurity suite, fortifying every touchpoint from customer interactions to core administrative systems.</strong>
            <br>Experience next-generation retail security designed for trust and resilience.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.header("✨ Core Innovations at a Glance")
    
    st.markdown("""
    <div class="content-section">
        <p>Retail Trust Shield is built on a foundation of cutting-edge security principles, ensuring end-to-end protection across your retail operations.</p>
        <ul>
            <li><strong>Firmware Integrity:</strong> Proactive defense against deep-level hardware attacks on POS systems and servers.</li>
            <li><strong>Zero Trust Access:</strong> Dynamic, stringent verification for all administrative access.</li>
            <li><strong>AI-Powered Monitoring:</strong> LLM-driven anomaly detection to secure admin actions.</li>
            <li><strong>Hashed Payments:</strong> Guarantees customer payment privacy with secure, one-way encryption.</li>
            <li><strong>Behavioral Biometrics:</strong> Silently identifies fraud by analyzing unique user interaction patterns.</li>
            <li><strong>Invisible MFA:</strong> Reduces friction for trusted users while maintaining robust security for risky logins.</li>
            <li><strong>Session Re-verification:</strong> Blocks sophisticated mid-session hijacking attempts.</li>
        </ul>
    </div>
    
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🚀 How to Test This Demo: A Quick Guide")
    
    st.markdown("""
    <div class="content-section">
        <p>Navigate effortlessly using the sidebar. Each section below provides clear, actionable instructions for hands-on testing. Keep a close eye on the <strong>Overall Safety Score</strong> in the sidebar—it dynamically reflects the system's security posture!</p>
        <h3>🏢 Admin Dashboard Features:</h3>
        <ol>
            <li><strong>Firmware Integrity Monitor:</strong>
                <p><strong>Test:</strong> Click "Run Check". To simulate a breach, manually edit any <code>*_modified.bin</code> file (e.g., <code>lojax_modified.bin</code>) in the project directory, save it, and then re-run the check. Observe the system's recovery.</p>
            </li>
            <li><strong>Zero Trust Access Control:</strong>
                <p><strong>Test:</strong> Experiment with the input fields. Enter 'New York' for the location to simulate a geo-denial, or provide a random/unknown string for the 'Device ID' to trigger an untrusted device alert. Then, click "Run Zero Trust Checks".</p>
            </li>
            <li><strong>Admin Action Logging + LLM Monitor:</strong>
                <p><strong>Test:</strong> Click "Refresh Admin Action Logs". Observe the simulated anomaly flagging unusual administrative behavior.</p>
            </li>
            <li><strong>💳 Payment Monitoring & Hashed Transaction Logs:</strong>
                <p><strong>Test:</strong> A new incoming payment alert will automatically appear every 20 seconds. Click the "Click to know more" link within the alert to instantly view plain vs. hashed payment data and navigate directly to this section. The payment will also be added to the secure logs below.</p>
            </li>
            <li><strong>Honeypot Admin Port Simulation:</strong>
                <p><strong>Test:</strong> Enter any username and password into the simulated honeypot login form. Observe the immediate detection alert, demonstrating proactive attacker identification.</p>
            </li>
        </ol>
        <h3>🧑‍💻 User Features (Shopper/Customer) Side:</h3>
        <ol>
            <li><strong>Account Login & Trust Scoring / Invisible MFA:</strong>
                <ul>
                    <li><strong>Test Login:</strong> Use any username and password to log in.</li>
                    <li><strong>Behavioral Biometrics:</strong> Type naturally (aim for 10-100 characters) to achieve a high trust score. For lower trust, try typing very little (<code>abc</code>) or pasting an excessively long text.</li>
                    <li><strong>Device Fingerprinting/IP:</strong> After an initial login, change the "Simulate your IP Address" on subsequent logins to observe a drop in the trust score due to device/IP inconsistency.</li>
                    <li><strong>Invisible MFA:</strong> Pay attention to whether the system bypasses the OTP (indicating high trust) or requires it (indicating lower trust or suspicious activity).</li>
                </ul>
            </li>
            <li><strong>🛒 Shopping & Suspicious Transaction AI:</strong>
                <ul>
                    <li><strong>Test:</strong> Add various items to your cart normally.</li>
                    <li><strong>Suspicious Activity 1 (Thresholds):</strong> Continue adding items. If your cart total exceeds $500, a security score reduction and alert will occur. If it crosses $600, all "Add Item" buttons will be disabled, and a "Suspicious Shopping Activity" alert will be triggered.</li>
                    <li><strong>Suspicious Activity 2 (Luxury Items):</strong> Try adding *only* luxury (high-priced) items. If you add 6 or more high-priced items without any daily/medium items, a suspicious activity alert will be shown.</li>
                    <li><strong>Observe:</strong> The bill amount updates in real-time with each item addition.</li>
                </ul>
            </li>
            <li><strong>Session Re-verification & Checkout:</strong>
                <p><strong>Test:</strong> Modify either the "Shipping Address" or "Payment Method" before proceeding to checkout. The system will then prompt for re-authentication. Enter <code>password123</code> to successfully verify.</p>
            </li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "Admin Dashboard":
    st.header("🏢 Admin/Owner Side Features")

    tab_firmware, tab_zero_trust, tab_admin_logs, tab_payments, tab_honeypot = st.tabs([
        "Firmware Integrity Monitor",
        "Zero Trust Access Control",
        "LLM Anomaly Monitor for Admin Actions",
        "Payment Monitoring & Hashed Logs",
        "Honeypot Admin Port Simulation"
    ])

    with tab_firmware:
        feature_card(
            "1. Firmware Integrity Monitor",
            "<strong>What:</strong> Detects BIOS/BMC tampering. Auto-recovers from trusted baseline.<br>"
            "<strong>Why Innovative:</strong> Targets deep hardware vulnerabilities.<br>"
            "<strong>How to Test:</strong> Click 'Run Check'. To simulate breach, edit `lojax_modified.bin` (or any `*_modified.bin`), save, then re-run."
        )
        if st.button("Run Firmware Integrity Check", key="firmware_check_button"):
            results = check_and_recover()
            for name, status, action in results:
                color = "🟢" if status == "Safe" else "🔴"
                st.write(f"{color} **{name}**: {status}")
                if action:
                    st.info(f"{name} firmware was recovered automatically.")
                    show_notification(f"✅ Firmware '{name}' recovered!", type="success")
                    update_overall_safety_score(random.randint(5, 10))
                else:
                    show_notification(f"🟢 Firmware '{name}' is safe.", type="info")
                    update_overall_safety_score(random.randint(1, 3))
        else:
            st.write("Click the button to start integrity checks.")

    with tab_zero_trust:
        feature_card(
            "2. Zero Trust Access Control (Simulated)",
            "<strong>What:</strong> Admin access requires TPM, geo-location, and device trust verification.<br>"
            "<strong>Why Innovative:</strong> Modern, dynamic internal access control, beyond static passwords.<br>"
            "<strong>How to Test:</strong> Adjust inputs. Try 'New York' for geo-denial, or a random string for Device ID to trigger untrusted device. Click 'Run Checks'."
        )
        
        user_id_input = st.text_input("Enter Admin User ID", "admin_user", key="zt_user_id")
        device_id_input = st.text_input("Enter Device ID", "device_123", key="zt_device_id")
        location_input = st.text_input("Enter Desired Access Location", "Bengaluru", help="Try 'New York' to see a denied geo-location check.", key="zt_location")

        if st.button("Run Zero Trust Checks", key="run_zt_checks_button"):
            st.markdown("##### Zero Trust Check Results:")
            tpm_s, geo_s, device_s = simulate_zero_trust_check(user_id_input, device_id_input, location_input)
            
            st.markdown("---")
            st.markdown("##### Hashed Login Details for Auditing:")
            hashed_admin_id = hashlib.sha256(user_id_input.encode()).hexdigest()
            hashed_device_id = hashlib.sha256(device_id_input.encode()).hexdigest()
            st.write(f"**Hashed Admin ID:** `{hashed_admin_id[:10]}...`")
            st.write(f"**Hashed Device ID:** `{hashed_device_id[:10]}...`")
            st.info("These hashes are stored for auditing purposes without revealing plain text credentials.")

            all_zt_passed = ("🟢 Passed" in tpm_s) and ("🟢 Passed" in geo_s) and ("🟢 Passed" in device_s)
            if all_zt_passed:
                update_overall_safety_score(random.randint(3, 7))
                show_notification("✅ Zero Trust Access Granted!", type="success")
            else:
                update_overall_safety_score(random.randint(-10, -5))
                show_notification("❌ Zero Trust Access Denied!", type="danger")

    with tab_admin_logs:
        feature_card(
            "3. LLM Anomaly Monitor for Admin Actions (Simulated)",
            "<strong>What:</strong> Logs sensitive admin actions. Simulated LLM flags anomalies (e.g., unusual time/permissions).<br>"
            "<strong>Why Innovative:</strong> AI proactively identifies insider threats or compromised accounts.<br>"
            "<strong>How to Test:</strong> Click 'Refresh Logs'. Observe the simulated anomaly."
        )
        
        if st.button("Refresh Admin Action Logs"):
            admin_logs = get_admin_action_logs()
            df_admin_logs = pd.DataFrame(admin_logs)
            st.dataframe(df_admin_logs)
            st.info("LLM Monitoring (simulated): Anomaly detected - 'Attempted to download customer data' by 'charlie'.")
            show_notification("🚨 Admin action anomaly detected!", type="warning")
            update_overall_safety_score(random.randint(-5, -2))

    with tab_payments:
        feature_card(
            "4. 💳 Payment Monitoring & Hashed Transaction Logs",
            "<strong>What:</strong> Tracks payments, logs transactions with <strong>one-way hashed</strong> sensitive data.<br>"
            "<strong>Why Innovative:</strong> Combines business monitoring with 'privacy by design' (like end-to-end encryption).<br>"
            "<strong>How to Test:</strong> A new incoming payment alert will appear automatically every 20 seconds. Click 'Click to know more' on the alert to view plain vs. hashed data and automatically navigate to this section. The payment will also be added to the logs below."
        )
        
        st.markdown("##### Incoming Payments Summary:")
        payment_summary = get_incoming_payments_summary()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Daily Revenue", payment_summary["Total Daily Revenue"])
        with col2:
            st.metric("Transactions Today", payment_summary["Transactions Today"])
        with col3:
            st.metric("Average Transaction Value", payment_summary["Average Transaction Value"])
        
        st.write("Payment Method Breakdown:")
        st.json(payment_summary["Payment Method Breakdown"])

        st.markdown("---")

        if st.session_state.show_payment_details and st.session_state.last_simulated_payment:
            st.subheader("🔍 Latest Incoming Payment Details:")
            st.info("This section displays the most recent payment data. On the left is the plain text information (for immediate review), and on the right is the corresponding hashed information (how it is securely stored).")
            col_plain, col_hashed = st.columns(2)
            with col_plain:
                st.markdown("##### Plain English Details:")
                st.json(st.session_state.last_simulated_payment['plain'])
            with col_hashed:
                st.markdown("##### Hashed Details (for secure storage):")
                st.json(st.session_state.last_simulated_payment['hashed'])
            
            if st.button("Close Payment Details", key="close_payment_details"):
                st.session_state.show_payment_details = False
                st.rerun()

        st.markdown("---")
        st.subheader("🔒 Secure Transaction History (Hashed)")
        hashed_logs = get_hashed_transaction_logs()
        if hashed_logs:
            df_hashed = pd.DataFrame(hashed_logs)
            st.dataframe(df_hashed)
            st.info("All sensitive customer data is stored in hashed format to ensure privacy protection.")
        else:
            st.info("No transaction logs available yet. Wait for incoming payments to populate this section.")

    with tab_honeypot:
        feature_card(
            "5. Honeypot Admin Port Simulation",
            "<strong>What:</strong> Fake admin login to detect attackers.<br>"
            "<strong>Why Innovative:</strong> Proactive threat detection - identifies bad actors before they cause damage.<br>"
            "<strong>How to Test:</strong> Enter any username/password in the honeypot form below. Observe immediate detection alert."
        )
        
        st.markdown("##### Simulated Honeypot Admin Login:")
        st.warning("⚠️ This is a honeypot - any login attempt will be flagged as suspicious!")
        
        with st.form("honeypot_form"):
            honeypot_user = st.text_input("Admin Username", placeholder="Enter username")
            honeypot_pass = st.text_input("Admin Password", type="password", placeholder="Enter password")
            honeypot_submit = st.form_submit_button("Login to Admin Panel")
            
            if honeypot_submit:
                if honeypot_user and honeypot_pass:
                    st.error("🚨 SECURITY ALERT: Unauthorized admin access attempt detected!")
                    st.markdown(f"""
                    **Detected Attempt:**
                    - Username: `{honeypot_user}`
                    - IP Address: `{st.session_state.last_known_ip}`
                    - Timestamp: `{time.strftime('%Y-%m-%d %H:%M:%S')}`
                    """)
                    show_notification("🚨 Honeypot triggered! Attacker detected!", type="danger")
                    update_overall_safety_score(random.randint(-15, -8))
                else:
                    st.warning("Please enter both username and password to test the honeypot.")

elif st.session_state.page == "User Features (Shopper/Customer)":
    st.header("🧑‍💻 User/Customer Side Features")

    tab_login, tab_shopping, tab_checkout = st.tabs([
        "Account Login & Trust Scoring",
        "Shopping & Suspicious Transaction AI", 
        "Session Re-verification & Checkout"
    ])

    with tab_login:
        feature_card(
            "1. Account Login & Behavioral Biometrics + Invisible MFA",
            "<strong>What:</strong> Analyzes typing patterns, device fingerprinting, and IP consistency. High trust = no MFA; low trust = requires OTP.<br>"
            "<strong>Why Innovative:</strong> Reduces friction for legitimate users while maintaining security.<br>"
            "<strong>How to Test:</strong> Type naturally (10-100 chars) for high trust. Try very short (`abc`) or very long pasted text for lower trust. Change IP after initial login to see trust score drop."
        )

        if st.session_state.logged_in_user:
            st.success(f"✅ Welcome back, {st.session_state.logged_in_user}!")
            st.info(f"🎯 Your current trust score: {st.session_state.user_trust_score}/100")
            
            if st.button("Logout", key="logout_button"):
                st.session_state.logged_in_user = None
                st.session_state.user_trust_score = 70
                st.session_state.device_fingerprint = None
                show_notification("👋 Logged out successfully!", type="info")
                st.rerun()
        else:
            st.subheader("🔐 Customer Login")
            
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                st.markdown("##### Behavioral Biometrics Test:")
                typing_sample = st.text_area(
                    "Type a message naturally (this analyzes your typing pattern):",
                    placeholder="Type something here... (10-100 characters for optimal trust scoring)",
                    height=100
                )
                
                ip_input = st.text_input(
                    "Simulate your IP Address", 
                    value=st.session_state.last_known_ip,
                    help="Change this after initial login to see trust score impact"
                )
                
                login_submit = st.form_submit_button("Login")
                
                if login_submit and username and password:
                    user_agent_sim = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                    # Generate device fingerprint on first login
                    if not st.session_state.device_fingerprint:
                        st.session_state.device_fingerprint = generate_device_fingerprint(user_agent=user_agent_sim, ip_address=ip_input)
                    
                    # Behavioral biometrics scoring
                    trust_score = 70  # Base score
                    
                    # Typing pattern analysis
                    if typing_sample:
                        typing_length = len(typing_sample)
                        if 10 <= typing_length <= 100:
                            trust_score += random.randint(10, 20)
                            st.info("✅ Natural typing pattern detected - trust score increased!")
                        elif typing_length < 10:
                            trust_score -= random.randint(15, 25)
                            st.warning("⚠️ Insufficient typing sample - trust score decreased!")
                        else:
                            trust_score -= random.randint(20, 30)
                            st.warning("⚠️ Unusual typing pattern (too long/pasted) - trust score decreased!")
                    
                    # IP consistency check
                    if ip_input != st.session_state.last_known_ip:
                        trust_score -= random.randint(20, 30)
                        st.warning("⚠️ IP address changed - trust score decreased!")
                        st.session_state.last_known_ip = ip_input
                    else:
                        trust_score += random.randint(5, 10)
                        st.info("✅ Consistent IP address - trust score maintained!")
                    
                    trust_score = max(0, min(100, trust_score))
                    st.session_state.user_trust_score = trust_score
                    
                    # Invisible MFA logic
                    if trust_score >= 75:
                        st.session_state.logged_in_user = username
                        st.success("🎉 High trust score detected - MFA bypassed!")
                        show_notification(f"✅ Welcome {username}! (MFA bypassed)", type="success")
                        update_overall_safety_score(random.randint(3, 7))
                        st.rerun()
                    else:
                        st.warning("🔐 Lower trust score detected - MFA required!")
                        otp_input = st.text_input("Enter OTP (use any 6-digit code):", max_chars=6)
                        if st.form_submit_button("Verify OTP") and len(otp_input) == 6:
                            st.session_state.logged_in_user = username
                            st.success("✅ OTP verified - Login successful!")
                            show_notification(f"✅ Welcome {username}! (MFA completed)", type="success")
                            update_overall_safety_score(random.randint(1, 4))
                            st.rerun()

    with tab_shopping:
        feature_card(
            "2. Shopping & Suspicious Transaction AI",
            "<strong>What:</strong> Monitors cart patterns. Flags high-value carts ($500+) and luxury-only purchases.<br>"
            "<strong>Why Innovative:</strong> Real-time fraud detection based on shopping behavior.<br>"
            "<strong>How to Test:</strong> Add items normally. Try exceeding $500 total or adding 6+ luxury items without daily/medium items."
        )

        if not st.session_state.logged_in_user:
            st.info("Please log in to access shopping features.")
        else:
            st.subheader("🛒 Shopping Cart")
            
            # Display current cart status
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Cart Total", f"${st.session_state.cart_value}")
            with col2:
                st.metric("Items in Cart", st.session_state.items_in_cart)
            
            # Shopping items grid
            st.markdown("##### Available Items:")
            
            # Check if shopping is disabled due to suspicious activity
            shopping_disabled = (
                st.session_state.cart_value > 600 or 
                st.session_state.suspicious_shopping_activity_detected
            )
            
            if shopping_disabled:
                st.error("🚨 Shopping temporarily disabled due to suspicious activity!")
            
            # Display items in a grid
            cols = st.columns(3)
            for i, item in enumerate(SHOPPING_ITEMS):
                with cols[i % 3]:
                    st.markdown(f"**{item['name']}**")
                    st.markdown(f"Price: ${item['price']}")
                    st.markdown(f"Type: {item['type']}")
                    
                    if st.button(
                        f"Add to Cart", 
                        key=f"add_{item['name']}", 
                        disabled=shopping_disabled
                    ):
                        # Update cart
                        st.session_state.cart_value += item['price']
                        st.session_state.items_in_cart += 1
                        
                        # Track item types for suspicious activity detection
                        if item['type'] in ['daily', 'medium']:
                            st.session_state.low_medium_item_count += 1
                        elif item['type'] == 'luxury':
                            st.session_state.high_priced_item_count += 1
                        
                        # Check for suspicious patterns
                        if st.session_state.cart_value > 500:
                            if not st.session_state.suspicious_shopping_activity_detected:
                                show_notification("⚠️ High-value cart detected! Monitoring increased.", type="warning")
                                update_overall_safety_score(random.randint(-8, -3))
                        
                        if st.session_state.cart_value > 600:
                            st.session_state.suspicious_shopping_activity_detected = True
                            show_notification("🚨 Suspicious shopping activity! Cart locked.", type="danger")
                            update_overall_safety_score(random.randint(-15, -10))
                        
                        # Check for luxury-only purchases
                        if (st.session_state.high_priced_item_count >= 6 and 
                            st.session_state.low_medium_item_count == 0):
                            st.session_state.suspicious_shopping_activity_detected = True
                            show_notification("🚨 Luxury-only purchase pattern detected!", type="danger")
                            update_overall_safety_score(random.randint(-12, -7))
                        
                        show_notification(f"✅ {item['name']} added to cart!", type="success")
                        st.rerun()

    with tab_checkout:
        feature_card(
            "3. Session Re-verification & Checkout",
            "<strong>What:</strong> Detects changes to critical checkout info (shipping/payment). Requires re-authentication.<br>"
            "<strong>Why Innovative:</strong> Prevents session hijacking during critical transactions.<br>"
            "<strong>How to Test:</strong> Modify shipping address or payment method, then try checkout. Use `password123` to verify."
        )

        if not st.session_state.logged_in_user:
            st.info("Please log in to access checkout features.")
        elif st.session_state.items_in_cart == 0:
            st.info("Your cart is empty. Add some items to proceed to checkout.")
        else:
            st.subheader("🛍️ Checkout")
            
            # Display order summary
            st.markdown("##### Order Summary:")
            st.info(f"Total Items: {st.session_state.items_in_cart} | Total Amount: ${st.session_state.cart_value}")
            
            # Checkout form
            with st.form("checkout_form"):
                st.markdown("##### Shipping & Payment Information:")
                
                shipping_address = st.text_area(
                    "Shipping Address", 
                    value=st.session_state.original_shipping_address,
                    height=80
                )
                
                payment_method = st.selectbox(
                    "Payment Method",
                    ["Visa ending 1234", "MasterCard ending 5678", "PayPal", "Apple Pay"],
                    index=0 if st.session_state.original_payment_method == "Visa ending 1234" else 0
                )
                
                checkout_submit = st.form_submit_button("Proceed to Checkout")
                
                if checkout_submit:
                    # Check if critical info has changed
                    address_changed = shipping_address != st.session_state.original_shipping_address
                    payment_changed = payment_method != st.session_state.original_payment_method
                    
                    if address_changed or payment_changed:
                        st.warning("🔐 Critical information changed - Re-authentication required!")
                        
                        changes_detected = []
                        if address_changed:
                            changes_detected.append("Shipping Address")
                        if payment_changed:
                            changes_detected.append("Payment Method")
                        
                        st.info(f"Changed: {', '.join(changes_detected)}")
                        
                        # Re-authentication form
                        reauth_password = st.text_input(
                            "Enter your password to confirm changes:",
                            type="password",
                            key="reauth_password"
                        )
                        
                        if st.button("Verify & Complete Order"):
                            if reauth_password == "password123":
                                st.success("✅ Re-authentication successful! Order completed.")
                                show_notification("🎉 Order completed successfully!", type="success")
                                update_overall_safety_score(random.randint(5, 10))
                                
                                # Reset cart and update stored preferences
                                st.session_state.cart_value = 0
                                st.session_state.items_in_cart = 0
                                st.session_state.original_shipping_address = shipping_address
                                st.session_state.original_payment_method = payment_method
                                st.session_state.suspicious_shopping_activity_detected = False
                                st.session_state.high_priced_item_count = 0
                                st.session_state.low_medium_item_count = 0
                                
                                st.rerun()
                            else:
                                st.error("❌ Incorrect password. Please try again.")
                                show_notification("❌ Re-authentication failed!", type="danger")
                                update_overall_safety_score(random.randint(-8, -3))
                    else:
                        st.success("✅ Order completed successfully!")
                        show_notification("🎉 Order completed successfully!", type="success")
                        update_overall_safety_score(random.randint(3, 7))
                        
                        # Reset cart
                        st.session_state.cart_value = 0
                        st.session_state.items_in_cart = 0
                        st.session_state.suspicious_shopping_activity_detected = False
                        st.session_state.high_priced_item_count = 0
                        st.session_state.low_medium_item_count = 0
                        
                        st.rerun()

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🛡️ <strong>Retail Trust Shield</strong> - Comprehensive Cybersecurity Suite</p>
    <p><em>Protecting your retail operations with cutting-edge security technology</em></p>
</div>
""", unsafe_allow_html=True)