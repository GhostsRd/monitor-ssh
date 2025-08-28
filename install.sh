#create user
apt-get install rsyslog -y
apt-get install python3 -y
apt-get install python3-venv -y
sudo useradd -r -s /bin/false sshwatch
groups sshwatch


#ajouter dans /etc/rsyslog.d/50-default.conf
#auth,authpriv.*    /var/log/auth.log
#local6.debug    /var/log/bash_command.log

sudo touch /var/log/ssh_monitor.log
sudo touch /var/log/auth.log
sudo touch /var/log/bash_command.log

sudo chown sshwatch:sshwatch /var/log/ssh_monitor.log
sudo chown sshwatch:sshwatch /var/log/bash_command.log
sudo chown sshwatch:sshwatch /var/log/auth.log

chmod 777 /var/log/auth.log
chmod 777 /var/log/bash_command.log
chmod 777 /var/log/ssh_monitor.log


sudo tee /etc/rsyslog.d/50-default.conf >/dev/null <<'EOF'
auth,authpriv.*    /var/log/auth.log
local6.debug    /var/log/bash_command.log
EOF



sudo tee /etc/profile.d/cmdlog.sh >/dev/null <<'EOF'
export PROMPT_COMMAND='RET=$?;
IP=$(who -u am i 2>/dev/null | awk "{print \$NF}" | sed -e "s/[()]//g" | awk "{print \$NF}");
TTY=$(tty);
cmd=$(history 1 | sed '\''s/^[ ]*[0-9]\+[ ]*//'\'' );
SERVER_IP=$(hostname -I | awk "{print \$1}");
logger -p local6.debug -- "SSH user=$(whoami) ip=${IP} server_ip=${SERVER_IP} tty=$TTY cmd=$cmd rc=$RET"'
EOF

mkdir -p /usr/local/bin/monitoring-ssh
cp ssh_monitor.py /usr/local/bin/monitoring-ssh/ssh_monitor.py
cd /usr/local/bin/monitoring-ssh
python3 -m venv .venv
source .venv/bin/activate
pip install requests


sudo systemctl daemon-reload
sudo systemctl enable rsyslog
sudo systemctl start rsyslog

sudo tee /etc/systemd/system/ssh-monitor.service >/dev/null <<'EOF'
[Unit]
Description=Surveillance SSH et commandes (alertes mail + Slack)
After=network.target
[Service]
Type=simple
ExecStart=/bin/bash -c 'cd /usr/local/bin/monitoring-ssh && source .venv/bin/activate && python3 ssh_monitor.py'
Restart=always
RestartSec=5
User=sshwatch
Group=sshwatch
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=ssh-monitor
[Install]
WantedBy=multi-user.target

EOF

cat << 'EOF' >> /root/.bashrc

# Logger toutes les commandes root
export PROMPT_COMMAND='RET=$?;
IP=$(who -u am i 2>/dev/null | awk "{print \$NF}" | sed -e "s/[()]//g" | awk "{print \$NF}");
TTY=$(tty);
cmd=$(history 1 | sed '\''s/^[ ]*[0-9]\+[ ]*//'\'' );
SERVER_IP=$(hostname -I | awk "{print \$1}");
logger -p local6.debug -- "SSH user=$(whoami) ip=${IP} server_ip=${SERVER_IP} tty=$TTY cmd=$cmd rc=$RET"'

EOF


sudo systemctl daemon-reload
sudo systemctl enable ssh-monitor
sudo systemctl start ssh-monitor