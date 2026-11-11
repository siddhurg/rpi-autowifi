from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

HTML_FORM = """
<!doctype html>
<html>
<head><title>Pi WiFi Setup</title></head>
<body>
  <h2>Connect Raspberry Pi to Wi-Fi</h2>
  <form method="POST" action="/connect">
    SSID: <input type="text" name="ssid"><br><br>
    Password: <input type="password" name="psk"><br><br>
    <input type="submit" value="Connect">
  </form>
</body>
</html>
"""

@app.route("/")
def index():
    return HTML_FORM

@app.route("/connect", methods=["POST"])
def connect():
    ssid = request.form["ssid"]
    psk = request.form["psk"]
    
    # Append new wifi network to wpa_supplicant
    config_entry = f'\nnetwork={{\n    ssid="{ssid}"\n    psk="{psk}"\n}}\n'
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a") as f:
        f.write(config_entry)
        
    subprocess.run(["sudo", "wpa_cli", "-i", "wlan0", "reconfigure"])
    return "Saved! The Pi is attempting to connect to " + ssid

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
