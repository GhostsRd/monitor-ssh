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
SMTP_USER = ""
SMTP_PASS = ""
MAIL_TO = ""

# Slack webhook
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"
#SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"
# Regex pour SSH
success_pattern = re.compile(r"Accepted .* for (\w+) from ([\d.]+)")
fail_pattern = re.compile(r"Failed password for (invalid user )?(\w+) from ([\d.]+)")

# Regex pour commandes loggÃ©es (voir profile.d/cmdlog.sh)
cmd_pattern = re.compile(r"SSH user=(\w+) ip=([\d.]+) server_ip=([\d.]+) tty=(\S+) cmd=(.*) rc=(-?\d+)")
# === Fonctions ===

def send_mail(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = MAIL_TO

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PsASS)
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
    #send_mail(f"SSH Monitor: {event_type}", message)  # Correction ici

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
                notify("Connexion SSH rÃ©ussie", f"user={user} client_ip={ip}  ")

            fail = fail_pattern.search(line)
            if fail:
                _, user, ip = fail.groups()
                notify("Connexion SSH Ã©chouÃ©e", f"user={user} ip={ip}")

def monitor_commands():
    """Surveille les commandes tapÃ©es avec IP"""
   
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
                user, ip, server_ip, tty, cmd, rc = m.groups()
                notify(
                    "Commande exÃ©cutÃ©e",
                    f"\n| Utilisateur\t| IP_client\t  | IP_serveur_cible\t|  Terminal type\t\t| rc\t| cmd\n"
                    f"| {user}\t| {ip}\t| {server_ip}\t\t| {tty}\t  | {rc}\t|  \"{cmd}\""
                )
            else:
                notify("Commande non parsÃ©e", f"Erreur du commande")

# === Lancer ===
if __name__ == "__main__":
    t1 = threading.Thread(target=monitor_auth, daemon=True)
    t2 = threading.Thread(target=monitor_commands, daemon=True)
    t1.start()
    t2.start()
    while True:
        time.sleep(1)