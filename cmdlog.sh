export PROMPT_COMMAND='RET=$?;
IP=$(who -u am i 2>/dev/null | awk "{print \$NF}" | sed -e "s/[()]//g" | awk "{print \$NF}");
TTY=$(tty);
cmd=$(history 1 | sed '\''s/^[ ]*[0-9]\+[ ]*//'\'' );
SERVER_IP=$(hostname -I | awk "{print \$1}");
logger -p local6.debug -- "SSH user=$(whoami) ip=${IP} server_ip=${SERVER_IP} tty=$TTY cmd=$cmd rc=$RET"'