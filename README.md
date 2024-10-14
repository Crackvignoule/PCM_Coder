Lien google docs : https://docs.google.com/document/d/11a2RUUIz6Qj_WmRjsjtVaEH0H74NKgQbIN6jzMXGLjA/edit?usp=sharing


# Analyse du PCM - DPCM - Partie 1
Nous nous proposons d'étudier l'impact des erreurs "type" induites par un réseau, sur un codeur de type PCM (ou DPCM)

Dans un premier temps, on simulera le fonctionnement d'un codeur PCM, linéaire, avec une résolution de R bits/éch.
1. Création d'un signal de référence.
    - a. Créer une tonalité sinusoïdale de fréquence 2kHz, de 3 sec de durée, en utilisant 10 échantillons (en float) par période. Reproduire cette tonalité sur les haut-parleurs de votre ordinateur.
    - b. Quantifier ce signal en (int) à 8 bits/éch.
    - c. Quantifier ce signal en utilisant une résolution de 6 bits/éch, de 4 bits/éch, de 3 bits/éch et de 2 bits/éch.
    - d. Que se passe-t-il quand la résolution du quantificateur devient 1 bit/éch ?

2. Nous allons simuler la latence d'un réseau fonctionnant en mode paquet.
Reprendre la tonalité représentée dans la partie 1) quantifiée avec une résolution de 8 b/éch. Créer des paquets de deux octets (c'est-à-dire, 2 échantillons par paquet) et simuler l'envoie de ces paquets à travers un réseau IP. Le sens de l'ouïe est sensible à la latence ? Simuler des retards de transmission différents pour chaque paquet. Conclusions ?

3. Nous allons maintenant simuler la perte de paquets. Reprendre le signal de la partie 1) en utilisant le quantificateur à 8 b/éch. Créez des paquets de 2 octets (c'est-à-dire, deux échantillons). Déterminer le nombre de paquets engendrés pour la tonalité de 3 sec de durée. Avec probabilité p=10-3, on va perdre un paquet complet. Comment simuler cette perte ? Tester avec p=10-2. Conclusions ?

# Analyse du PCM - DPCM - Partie 2
On simulera maintenant un codeur du type DPCM linéaire avec une résolution R (bits/éch). Il suffit de quantifier les différences entre deux échantillons consécutifs.

1. Étudier l'impact de la latence dans ce type de codage.

2. Que se passe-t-il si on perd des « paquets » d'octets? Conclure à partir de la taille des paquets et du taux de perte.

3. Comment se porte ce codeur si on est en présence d'erreurs aléatoires avec un taux d'erreur z=10-2 et z=10-3. Conclusions ?

4. Quantifier la voix de Xtine en utilisant une résolution de 8 bits/éch, et créer des paquets de 4 octets. Que se passe-t-il si on perd des « paquets » ? Indiquez le taux de pertes de blocs de 4 octets.
