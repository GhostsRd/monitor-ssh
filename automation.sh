#!/bin/bash

# Liste des serveurs : IP:USER:PASS
SERVERS=(
    "10.10.10.26:tsirika:addroot:5522"
    

)

# Fichiers à déployer
#LOCAL_FILES=("file.sh" "test.sh")
LOCAL_FILES=("upgradeuser.sh")

REMOTE_TMP="/home/tsirika/monitor/"

for SERVER_INFO in "${SERVERS[@]}"; do
    # Extraire IP, USER et PASS
    SERVER=$(echo $SERVER_INFO | cut -d: -f1)
    USER=$(echo $SERVER_INFO | cut -d: -f2)
    PASS=$(echo $SERVER_INFO | cut -d: -f3)
    PORT=$(echo $SERVER_INFO | cut -d: -f4)

    #echo "==> Déploiement sur $SERVER avec l'utilisateur $USER"

    # Copier les fichiers avec rsync
    for FILE in "${LOCAL_FILES[@]}"; do
        sshpass -p "$PASS" rsync -avz -e "ssh -p $PORT" "$FILE" $USER@$SERVER:$REMOTE_TMP/
    done

    # Déplacer les fichiers et mettre les permissions
    #shpass -p "$PASS" ssh -p $PORT $USER@$SERVER "sudo mv /tmp/cmdlog.sh /etc/profile.d/ && sudo chmod +x /etc/profile.d/cmdlog.sh"
    #sshpass -p "$PASS" ssh -p $PORT $USER@$SERVER "sudo mv /tmp/ssh_monitor.py /usr/local/bin/ && sudo chmod +x /usr/local/bin/ssh_monitor.py"
    sshpass -p "$PASS" ssh -p $PORT $USER@$SERVER "bash /home/tsirika/monitor/upgradeuser.sh"
    # Lancer le script Python en arrière-plan
    #sshpass -p "$PASS" ssh -p $PORT $USER@$SERVER "nohup sudo python3 /usr/local/bin/ssh_monitor.py &> /var/log/ssh_monitor.log &"

    echo "==> Upgrade terminé sur $SERVER"
done
