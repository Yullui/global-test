import os
import pandas as pd
import streamlit as st
import geoip2.database
import hashlib
import datetime
import smtplib
from email.message import EmailMessage  # This is the secret for emojis
from dotenv import load_dotenv

# --- 1. CORE CONFIGURATION ---
st.set_page_config(layout="wide", page_title="SOC Command Center", page_icon="🛡️")

env_path = r"C:\Users\userA\Agentic\.env"
load_dotenv(dotenv_path=env_path)

email_address = os.getenv('EMAIL_ADDRESS')
password = os.getenv('PASSWORD')
RECIPIENT = "RECIPIENT@proton.me"

BLACKLIST_PATH = r"C:\Users\userA\Agentic\blacklist.txt"
GEOIP_DB_PATH = r"C:\Users\userA\Agentic\GeoLite2-City.mmdb"
SOC_LAT, SOC_LON = 38.8339, -104.8214


# --- 2. DATA PROCESSING ---
@st.cache_data
def process_blacklist(file_path):
    if not os.path.exists(GEOIP_DB_PATH): return pd.DataFrame()
    reader = geoip2.database.Reader(GEOIP_DB_PATH)
    data = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                ip = line.strip()
                if not ip: continue
                try:
                    res = reader.city(ip)
                    data.append({
                        "ip": ip, "lat": res.location.latitude, "lon": res.location.longitude,
                        "country": res.country.name, "city": res.city.name or "Unknown",
                        "tactic": "Initial Access"
                    })
                except:
                    continue
    except:
        pass
    return pd.DataFrame(data)


# --- 3. MAIN INTERFACE ---
def main():
    st.markdown("<h1 style='text-align: center; color: #00f2ff; font-family: monospace;'>SOC VECTOR COMMAND</h1>",
                unsafe_allow_html=True)

    df = process_blacklist(BLACKLIST_PATH)

    if not df.empty:
        col_intel, col_map = st.columns([1, 2.5])

        with col_intel:
            st.markdown("### 📡 Node Investigation")
            selected_ip = st.selectbox("Select Target IP", options=df['ip'].unique())
            node = df[df['ip'] == selected_ip].iloc[0]

            with st.container(border=True):
                st.info(f"**Origin:** {node['city']}, {node['country']}")

                if st.button("🚨 Create Incident Ticket"):
                    with st.spinner("Dispatching via SMTP..."):
                        try:
                            # 1. Create unique metadata
                            t_hash = hashlib.md5((node['ip'] + str(datetime.datetime.now())).encode()).hexdigest()
                            ticket_id = f"SOC-{t_hash[:8].upper()}"
                            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            # 2. Setup the EmailMessage (Handles Unicode/Emojis)
                            msg = EmailMessage()
                            msg['Subject'] = f"🚨 SOC ALERT: {ticket_id} | {node['ip']}"
                            msg['From'] = email_address
                            msg['To'] = RECIPIENT

                            content = f"""SOC Incident Report
-------------------
Ticket ID: {ticket_id}
Target IP: {node['ip']}
Location:  {node['city']}, {node['country']}
Timestamp: {timestamp}
Notes:     Manual Flag by {RECIPIENT}"""

                            msg.set_content(content)

                            # 3. Send via SMTP
                            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                                smtp.ehlo()
                                smtp.starttls()
                                smtp.login(email_address, password)
                                smtp.send_message(msg)  # Note: send_message instead of sendmail

                            st.success(f"Ticket {ticket_id} Sent!")
                        except Exception as e:
                            st.error(f"Error: {e}")

        with col_map:
            map_data = pd.DataFrame([{"lat": node['lat'], "lon": node['lon']}, {"lat": SOC_LAT, "lon": SOC_LON}])
            st.map(map_data, color="#ff0000", size=20)
            st.caption(f"Threat Vector: {node['city']} → Colorado Springs")


if __name__ == "__main__":
    main()