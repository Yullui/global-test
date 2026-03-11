Overview

The SOC Command Center is a real-time Security Operations Center (SOC) dashboard built with Streamlit. It visualizes threat vectors from blacklisted IPs to your local SOC location  and allows for one-click incident reporting via a secure SMTP integration.
Core Features

    Geospatial Visualization: Maps incoming threat IPs from a blacklist.txt file against a MaxMind GeoLite2 database to show physical attack vectors.

    Node Investigation: Select a specific IP to see its origin city, country, and a simulated MITRE ATT&CK tactic.

    One-Click Ticketing: Generates a deterministic, hashed Ticket ID (e.g., SOC-022FEEBF) and dispatches a full Incident Report to a specified Proton Mail account.

    Secure SMTP Logic: Uses Python's EmailMessage class and STARTTLS to handle secure authentication and Unicode characters (emojis) in threat alerts.
<img width="1772" height="417" alt="image" src="https://github.com/user-attachments/assets/fc3b43c5-d644-4985-a23d-4d2f138b5757" />

System Requirements

    Python 3.10+

    MaxMind GeoLite2 City Database: Required for IP-to-Location mapping.

    App Passwords: Requires a Google App Password for the sender account.

🛠️ Components Documentation
1. SOC Vector Dashboard (global_test.py)

This is the primary interface for threat analysis.

Workflow:

    Ingestion: Reads blacklist.txt for a list of suspicious IPs.

    Enrichment: Pulls latitude, longitude, and city data from the local .mmdb file.

    Authentication: Loads credentials from a hidden .env file to prevent hardcoding sensitive data.

    Reporting: When the "Create Incident Ticket" button is triggered, it executes an SMTP handshake to send the following report:

        Ticket ID: Unique MD5 hash based on IP and Timestamp.

        Timestamp: ISO-standard incident time.

        Origin: Physical location of the threat.

        Notes: Automatic manual flag attribution.

2. Standalone SMTP Utility (mailer_test.py)

A lightweight diagnostic script used to verify connectivity without the GUI.

Purpose:

    Tests the python-dotenv parsing of the .env file.

    Verifies that the Google SMTP server (smtp.gmail.com:587) accepts the App Password.

    Confirms that emails are successfully landing in the Proton Mail inbox.

🚀 Setup & Installation

    Configure Environment:
    Create a .env file in the project root:
    Code snippet

    EMAIL_ADDRESS=your_sender@gmail.com
    PASSWORD=your_16_digit_app_password

    Install Dependencies:
    Bash

    pip install streamlit pandas geoip2 python-dotenv

    Run Dashboard:
    Bash

    streamlit run redacted_global_test.py
