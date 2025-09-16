<h1>Moniteur de Connexion SSH 🤖</h1>
Ce script Bash simple et puissant est conçu pour surveiller la disponibilité de vos serveurs via SSH. Il est idéal pour les administrateurs système, les développeurs DevOps et toute personne ayant besoin de s'assurer que leurs connexions SSH sont toujours opérationnelles et sécurisées. Le script peut être facilement intégré à des tâches cron pour une surveillance régulière.

<h2>Fonctionnalités Principales ✨</h2>
Vérification de la connectivité SSH : Teste si une connexion SSH peut être établie avec succès.

Surveillance de la disponibilité : S'assure que vos serveurs sont en ligne et accessibles.

Notifications Personnalisées : Peut être configuré pour envoyer des alertes en cas d'échec de connexion (par e-mail, Slack, etc.).

Léger et Efficace : Utilise des commandes Bash de base, sans dépendances lourdes.

Facile à Intégrer : S'intègre parfaitement dans vos workflows d'automatisation et de CI/CD.

<h2>Comment ça fonctionne ? 💡</h2>
Le script utilise la commande ssh en mode non interactif pour tenter de se connecter à un serveur spécifié. En fonction du résultat, il renvoie un statut de succès ou d'échec. Vous pouvez l'adapter pour qu'il exécute des commandes spécifiques sur le serveur distant, ou simplement pour vérifier la connectivité de base. Il est recommandé de l'exécuter avec une clé SSH et un agent SSH pour éviter d'avoir à saisir un mot de passe.

<h2>Exemples d'Utilisation 🛠️</h2>
Surveillance de production : S'assurer que les serveurs critiques sont toujours accessibles.

Vérification de déploiement : Confirmer que le service SSH est opérationnel après une mise à jour ou un redémarrage.

Audit de sécurité : Tester régulièrement la connectivité pour détecter d'éventuels problèmes.

</h2>Commencer 🚀</h2>
Clonez le dépôt : git clone https://github.com/GhostsRd/monitor-ssh

Naviguez dans le répertoire : cd monitor-ssh

Executer : bash install.sh

sudo systemctl daemon-reload

sudo systemctl enable ssh-monitor

sudo systemctl status ssh-monitor

