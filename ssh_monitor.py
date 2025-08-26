#!/usr/bin/env python3
import time
import re
import smtplib
from email.mime.text import MIMEText
import requests
import threading
import os

# === Configuration ===
LOG_AUTH = "/var/log/auth.log"             # journal SSH
LOG_COMMANDS = "/var/log/bash_command.log" # journal commandes utilisateurs
LOCAL_LOG = "/var/log/ssh_monitor.log"     # log global

# Mail settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "leoncerado@gmail.com"
SMTP_PASS = "wzaa iuwh jfey uihl"
MAIL_TO = "leoncerado@gmail.com"

# Slack webhook
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# Regex pour SSH
success_pattern = re.compile(r"Accepted .* for (\w+) from ([\d.]+)")
fail_pattern = re.compile(r"Failed password for (invalid user )?(\w+) from ([\d.]+)")

# Regex pour commandes loggées (voir profile.d/cmdlog.sh)
cmd_pattern = re.compile(r"SSH user=(\w+) ip=([\d.]+) tty=(\S+) cmd=(.*) rc=(-?\d+)")

# === Fonctions ===

def send_mail(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = MAIL_TO

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, [MAIL_TO], msg.as_string())
        server.quit()
    except Exception as e:
        print(f"[ERREUR Mail] {e}")

def send_slack(message):
    try:
        payload = {"text": message}
        requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"[ERREUR Slack] {e}")

def log_local(message):
    with open(LOCAL_LOG, "a") as f:
        f.write(message + "\n")

def notify(event_type, message):
    msg = f"[{event_type}] {message}"
    print(msg)
    log_local(msg)
    send_slack(msg)
    send_mail(f"SSH Monitor: {event_type}", message)  # Correction ici

# === Threads de surveillance ===
def monitor_auth():
    """Surveille les connexions SSH"""
    with open(LOG_AUTH, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue

            success = success_pattern.search(line)
            if success:
                user, ip = success.groups()
                notify("Connexion SSH réussie", f"user={user} ip={ip}")

            fail = fail_pattern.search(line)
            if fail:
                _, user, ip = fail.groups()
                notify("Connexion SSH échouée", f"user={user} ip={ip}")

def monitor_commands():
    """Surveille les commandes tapées avec IP"""
   
    with open(LOG_COMMANDS, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            print(f"[DEBUG]  Lignelue: {line.strip()}")
            m = cmd_pattern.search(line)
            if m:
                user, ip, tty, cmd, rc = m.groups()
                notify("Commande exécutée", f"user={user} ip={ip} tty={tty} cmd=\"{cmd}\" rc={rc}")
            else:
                notify("Commande non parsée", f"Erreu du commande")

# === Lancer ===
if __name__ == "__main__":
    t1 = threading.Thread(target=monitor_auth, daemon=True)
    t2 = threading.Thread(target=monitor_commands, daemon=True)
    t1.start()
    t2.start()
    while True:
        time.sleep(1)
