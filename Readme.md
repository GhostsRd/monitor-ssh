<h1>Moniteur de Connexion SSH 🤖</h1>
Ce script Bash simple et puissant est conçu pour surveiller la disponibilité de vos serveurs via SSH. Il est idéal pour les administrateurs système, les développeurs DevOps et toute personne ayant besoin de s'assurer que leurs connexions SSH sont toujours opérationnelles et sécurisées. Le script peut être facilement intégré à des tâches cron pour une surveillance régulière.

Fonctionnalités Principales ✨
Vérification de la connectivité SSH : Teste si une connexion SSH peut être établie avec succès.

Surveillance de la disponibilité : S'assure que vos serveurs sont en ligne et accessibles.

Notifications Personnalisées : Peut être configuré pour envoyer des alertes en cas d'échec de connexion (par e-mail, Slack, etc.).

Léger et Efficace : Utilise des commandes Bash de base, sans dépendances lourdes.

Facile à Intégrer : S'intègre parfaitement dans vos workflows d'automatisation et de CI/CD.

Comment ça fonctionne ? 💡
Le script utilise la commande ssh en mode non interactif pour tenter de se connecter à un serveur spécifié. En fonction du résultat, il renvoie un statut de succès ou d'échec. Vous pouvez l'adapter pour qu'il exécute des commandes spécifiques sur le serveur distant, ou simplement pour vérifier la connectivité de base. Il est recommandé de l'exécuter avec une clé SSH et un agent SSH pour éviter d'avoir à saisir un mot de passe.

Exemples d'Utilisation 🛠️
Surveillance de production : S'assurer que les serveurs critiques sont toujours accessibles.

Vérification de déploiement : Confirmer que le service SSH est opérationnel après une mise à jour ou un redémarrage.

Audit de sécurité : Tester régulièrement la connectivité pour détecter d'éventuels problèmes.

Commencer 🚀
Clonez le dépôt : git clone [votre-url-du-depot]

Naviguez dans le répertoire : cd [votre-repertoire]

Modifiez le script monitor.sh (ou le nom de votre script) pour y insérer l'utilisateur et l'adresse IP de votre serveur.

Exécutez le script : ./monitor.sh

Note : Pensez à rendre le script exécutable avec chmod +x monitor.sh.




\#create user
sudo useradd -r -s /bin/false sshwatch
groups sshwatch

sudo chown sshwatch:sshwatch /usr/local/bin/ssh\_monitor.py
apt-get install rsyslog -y


#ajouter dans /etc/rsyslog.d/50-default.conf

auth,authpriv.\*    /var/log/auth.log
local6.debug    /var/log/bash\_command.log



sudo touch /var/log/ssh\_monitor.log
sudo chown sshwatch:sshwatch /var/log/ssh\_monitor.log

chmod 777 /var/log/bash\_command.log



sudo tee /etc/profile.d/cmdlog.sh >/dev/null <<'EOF'
export PROMPT\_COMMAND='RET=$?;
IP=$(who -u am i 2>/dev/null | awk "{print $NF}" | sed -e "s/\[()]//g");
TTY=$(tty);
logger -p local6.debug -- "SSH user=$(whoami) ip=${IP:-unknown} tty=$TTY cmd=$(history 1 | sed "s/^\[ ]*\[0-9]+\[ ]*//") rc=$RET"'
EOF

&nbsp;

\#creer le log ssh

touch /var/log/ssh\_monitor.log
sudo chown sshwatch:sshwatch /var/log/ssh\_monitor.log



SSH user=rado ip=192.168.1.25 tty=/dev/pts/0 cmd=ls -la rc=0
SSH user=ubuntu ip=203.0.113.15 tty=/dev/pts/1 cmd=cat /etc/passwd rc=0


#test de print
echo 'SSH user=test ip=127.0.0.1 tty=/dev/pts/1 cmd=ls rc=0' >> /var/log/bash\_command.log



\#run python as service sur venv

nano  /etc/systemd/system/ssh-monitor.service
\[Unit]
Description=Surveillance SSH et commandes (alertes mail + Slack)
After=network.target
\[Service]
Type=simple
ExecStart=/bin/bash -c 'cd /usr/local/bin \&\& source .venv/bin/activate \&\& p>Restart=always
RestartSec=5
User=sshwatch
Group=sshwatch
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=ssh-monitor
\[Install]
WantedBy=multi-user.target



sudo systemctl daemon-reload

sudo systemctl enable ssh-monitor

sudo systemctl start ssh-monitor

