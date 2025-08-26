

#create user
sudo useradd -r -s /bin/false sshwatch 
groups sshwatch 

sudo chown sshwatch:sshwatch /usr/local/bin/ssh_monitor.py 
apt-get install rsyslog -y
#ajouter dans /etc/rsyslog.d/50-default.conf

udo touch /var/log/ssh_monitor.log 
sudo chown sshwatch:sshwatch /var/log/ssh_monitor.log 

auth,authpriv.*    /var/log/auth.log
local6.debug    /var/log/bash_command.log

chmod 777 /var/log/bash_command.log


sudo tee /etc/profile.d/cmdlog.sh >/dev/null <<'EOF'
export PROMPT_COMMAND='RET=$?;
IP=$(who -u am i 2>/dev/null | awk "{print \$NF}" | sed -e "s/[()]//g");
TTY=$(tty);
logger -p local6.debug -- "SSH user=$(whoami) ip=${IP:-unknown} tty=$TTY cmd=$(history 1 | sed "s/^[ ]*[0-9]\+[ ]*//") rc=$RET"'
EOF

touch /var/log/ssh_monitor.log 
sudo chown sshwatch:sshwatch /var/log/ssh_monitor.log 


SSH user=rado ip=192.168.1.25 tty=/dev/pts/0 cmd=ls -la rc=0
SSH user=ubuntu ip=203.0.113.15 tty=/dev/pts/1 cmd=cat /etc/passwd rc=0
#test
echo 'SSH user=test ip=127.0.0.1 tty=/dev/pts/1 cmd=ls rc=0' >> /var/log/bash_command.log

#run python as service sur venv

nano  /etc/systemd/system/ssh-monitor.service
[Unit]
Description=Surveillance SSH et commandes (alertes mail + Slack)
After=network.target
[Service]
Type=simple
ExecStart=/bin/bash -c 'cd /usr/local/bin && source .venv/bin/activate && p>Restart=always
RestartSec=5
User=sshwatch
Group=sshwatch
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=ssh-monitor
[Install]
WantedBy=multi-user.target

