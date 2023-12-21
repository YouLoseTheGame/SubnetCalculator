##Calculateur de sous-réseaux IP

#importation du log2 du module math
from math import log2

# calcule le nombre d'hôtes maximum pour un sous-réseau donné
def nombreH(nbHote):
    i = 0
    # boucle pour trouver la puissance de 2 qui dépasse le nombre d'hôtes donné
    while (2**i) - 2 < nbHote:
        i += 1
    # retourne le nombre d'hôtes maximum pour un sous-réseau
    return (2**i) - 2

# calcule le nombre de sous-réseaux pour un nombre d'hôtes donné
def nombreRS(nbHote):
    i = 0
    # boucle pour trouver la puissance de 2 qui dépasse le nombre d'hôtes donné
    while (2**i) - 2 < nbHote:
        i += 1
    # retourne le nombre de sous-réseaux pour un nombre d'hôtes donné
    return (2**(i-1)) - 2


# découpe l'adresse IP en séparant les octets
def decoupIp(adresse):
    tabl = adresse.split(".")
    return(tabl)

# construit l'adresse de réseau à partir des octets et du compteur
def addrRes(adresseDecoup, cpt, nb0):
    adresseDecoup[-1] = str(cpt[-1])
    if nb0 > 1:
        adresseDecoup[-2] = str(cpt[-2])
        if nb0 > 2:
            adresseDecoup[-3] = str(cpt[-3])
    return adresseDecoup

# joint les octets pour former une adresse IP
def joindre(adresseDecoup):
    StrAdresse = ".".join(adresseDecoup)
    return StrAdresse



#calcule le masque de sous-réseau en fonction du nombre de bits de masque donnés
def SRMask(masque):
    #initialise les variables
    maskBit = ""
    MaskDecim = []
    valeur = 0
    MaskRes = ""
    # vérifie si le masque commence par un "/"
    if masque[0] == "/":
        masque = masque[1:]
        # boucle pour ajouter des "1" pour le nombre de bits de masque donné
        for cpt in range(int(masque)):
            maskBit += "1"
        # boucle pour ajouter des "0" pour compléter 32 bits
        for cpt in range(32- int(masque)):
            maskBit += "0"
        # boucle pour découper les bits en octets
        for cpt in range(0, len(maskBit), 8):
            MaskDecim.append(maskBit[cpt:cpt+8])
        # boucle pour calculer la valeur décimale de chaque octet
        for res in range(4):
            for sousres in range(8):
                valeur += int(MaskDecim[res][sousres]) * 2**(7-sousres)
            MaskRes += str(valeur)
            MaskRes += "."
            valeur = 0
        # enlève le dernier "." ajouté
        MaskRes = MaskRes[:-1]
        return MaskRes
    else:
        return masque

#transforme un compteur donné en une liste de 3 valeurs
def compteurTransform(compteur):
    cptTrans = []
    cpt3 = int(compteur[-3])
    cpt2 = int(compteur[-2])
    cpt1 = int(compteur[-1])
    cpt2 += cpt1 // 256
    cpt3 += cpt2 // 256
    cptTrans.append(cpt3)
    cpt2 = cpt2 % 256
    cptTrans.append(cpt2)
    cpt1 = cpt1 % 256
    cptTrans.append(cpt1)
    return cptTrans

# vérifie si un compteur donné est valide en fonction du nombre d'hôtes
def verifCompteur(compteur, decoupHote):
    verifCompteur = []
    verifCompteur.append(compteur[-3])
    verifCompteur.append(compteur[-2])
    verifCompteur.append(compteur[-1])
    verifCompteur[-1] = verifCompteur[-1] + decoupHote
    verifCompteur2 = compteurTransform(verifCompteur)
    return verifCompteur2





def IPaddr():
    compteur = [0, 0, 0]
    nbReseau = 1

    # demande à l'utilisateur de saisir une adresse IP
    adresse = str(input("Saisir une adresse Ip au format décimal pointé:"))
    addrDecoup = decoupIp(adresse)
    # vérifie si l'adresse saisie est valide
    if adresse == "":
        print("Veuillez entrez une adresse Ip")
        return IPaddr()
    elif len(adresse) > 15 or len(adresse) < 7:
        print("Veuillez entrer une adresse Ip valide")
        return IPaddr()
    for elt in addrDecoup:
        try:
            int(elt)
        except ValueError:
            print("Veuillez entrer une adresse Ip valide")
            return IPaddr()
        if int(elt) > 255 or int(elt) < 0:
            print("L'adresse IP n'est pas valide. Elle doit être comprise en 0.0.0.0 et 255.255.255.255")
            return IPaddr()

    # demande à l'utilisateur de saisir un masque
    verifMask = 1
    while verifMask != 0:
        masque = str(input("Saisir un masque au format décimal pointé ou CIDR (/nb):"))
        # vérifie si le masque saisie est valide
        verifMask = 0
        verifErreur = 0
        maskDecoup = decoupIp(masque)
        if masque == "":
            print("Veuillez entrez un masque")
            verifMask += 1
        elif masque[0] == "/":
            nb0 = 0
            nbMask = masque[1:]
            try:
                int(nbMask)
            except ValueError:
                print("Veuillez entrer un masque valide")
                verifMask = 1
            else:
                if int(nbMask) < 0 or int(nbMask) > 32:
                    print("Le masque doit être compris entre 0 et 32, veuillez entrer un masque valide")
                    verifMask = 1
                else:
                    masque = SRMask(masque)
                    mskDcp = decoupIp(masque)
                    for cpt in range(len(mskDcp)):
                        if int(mskDcp[cpt]) == 0:
                            nb0 += 1
        else:
            nb0 = 0
            # vérifie si un masque est saisi
            if masque == "":
                print("Veuillez entrez un masque")
                verifMask += 1
            elif len(masque) > 15 or len(masque) < 7:
                print("Veuillez entrer une masque valide")
                verifMask += 1
                continue
            # vérifie si le masque saisi est valide
            for cpt in range(len(maskDecoup)):
                try:
                    int(maskDecoup[cpt])
                except ValueError:
                    print("Veuillez entrer un masque valide")
                    verifErreur = 1
                if int(maskDecoup[cpt]) > 255 or int(maskDecoup[cpt]) < 0:
                    verifErreur = 1
                elif int(maskDecoup[-1]) == 255:
                    verifErreur = 1
                elif int(maskDecoup[cpt]) != 255 and int(maskDecoup[cpt]) != 0:
                    verifErreur = 1
                elif int(maskDecoup[cpt]) == 255 and int(maskDecoup[cpt-1]) == 0 and cpt != 0:
                    verifErreur = 1
                if verifErreur != 0:
                    verifMask += 1
                    print("Le masque n'est pas valide")
                else:
                    if int(maskDecoup[cpt]) == 0:
                        nb0 += 1

    # demande si l'utilisateur souhaite définir le nombre des sous-réseaux ou le nombre d'hôtes
    verifChoix = 1
    while verifChoix != 0:
        choix = str(input("Souhaitez-vous définir le nombre des sous-réseaux? (1) ou le nombre d'hôtes ? (2)'"))
        verifChoix = 0
        if str(choix) != "1" and str(choix) != "2":
            verifChoix += 1
            print("Veuillez entrer une option valide: 1 ou 2")

    choix = int(choix)

    #choix de la définition des hôtes
    if choix == 1:
        verifHote = 1
        # Demande le nombre d'hôte
        while verifHote != 0:
            # Vérifie si l'entrée est valide
            nbHote = input("Combien voulez-vous d'hôtes?")
            verifHote = 0
            try:
                int(nbHote)
            except ValueError:
                print("Veuillez entrer un Dans ce cas, une entree non valide est entree, veuillez entrer un nombre d'hôte valide")
                verifHote += 1
                continue
            if int(nbHote) > (254**nb0) or int(nbHote) < 0:
                print("Le nombre d'hôte doit être compris entre 0 et", 254**nb0)
                verifHote += 1


        #calcule le nombre de sous-réseaux
        nbHote = int(nbHote)
        decoupHote = nombreH(nbHote)
        print("Nombre maximal d'hôtes pour chaque sous-réseau:", decoupHote)
        print("")
        #calcule le nombre d'octets disponibles
        if nb0 < 3:
            compteur[-3] = 255
            if nb0 < 2:
                compteur[-2] = 255
        verifBoucle = verifCompteur(compteur, decoupHote)

        #boucle principale d'affichage des sous-réseaux
        while verifBoucle[-3] < 256:

            #affichage des différentes caractéristiques du sous-réseaux
            print("***Réseau n°", nbReseau, "***", sep="")
            print("Adresse réseaux :", joindre(addrRes(addrDecoup, compteurTransform(compteur), nb0)))
            compteur[-1] += 1
            compteur = compteurTransform(compteur)
            print("Première adresse :", joindre(addrRes(decoupIp(adresse), compteurTransform(compteur), nb0)))
            compteur[-1] += (decoupHote - 1)
            compteur = compteurTransform(compteur)
            print("Dernière adresse :", joindre(addrRes(decoupIp(adresse), compteurTransform(compteur), nb0)))
            compteur[-1] += 1
            compteur = compteurTransform(compteur)
            AddrDiff = joindre(addrRes(decoupIp(adresse), compteurTransform(compteur), nb0))
            print("Adresse de diffusion :", AddrDiff)
            verifBoucle = verifCompteur(compteur, decoupHote)

            #calcul du masque
            if nbReseau == 1:
                addrMask = AddrDiff

            MaskDecoup = decoupIp(str(SRMask(masque)))
            DecoupAddrDiff = decoupIp(addrMask)
            MaskDecoup[-1] = str(255 - int(DecoupAddrDiff[-1]))
            print("Masque réseau", joindre(MaskDecoup))
            nbReseau += 1
            compteur[-1] += 1
            compteur = compteurTransform(compteur)
            print("")
        return


#choix de la définition des sous-réseaux
    else:
        verifRes = 1
        while verifRes != 0:
            #demande et vérifie le nombre de sous-réseaux
            verifRes = 0
            nbSR = input("Combien voulez-vous de sous-réseaux?")
            if nbSR == "":
                verifRes += 1
            try:
                int(nbSR)
            except ValueError:
                verifRes +=1
            else:
                nbSR = int(nbSR)
                if nb0 == 1:
                    if nbSR > 64:
                        verifRes += 1
                elif nb0 == 2:
                    if nbSR > 16384:
                        verifRes +=1
                elif nb0 == 3:
                    if nbSR > 4194304:
                        verifRes +=1
            if verifRes != 0:
                print("Votre entrée n'est pas valide.")

        #calcule le nombre d'hôte de chaque sous-réseau
        nbReseaux = nombreRS(nombreH(nbSR))
        print("Nombre maximal d'hôtes pour chaque sous-réseau:", int(nbReseaux))
        print("")
        #calcule le nombre d'octets disponibles
        if nb0 < 3:
            compteur[-3] = 0
            if nb0 < 2:
                compteur[-2] = 0
        nbSR = nombreH(nbSR) + 2

        #boucle principale
        for cpt in range(int(nbSR)):
            #affichage des éléments principaux des sous-réseaux
            print("***Réseau n°", nbReseau, "***", sep="")
            print("Adresse réseaux :", joindre(addrRes(addrDecoup, compteurTransform(compteur), nb0)))
            compteur[-1] += 1
            compteur = compteurTransform(compteur)
            print("Première adresse :", joindre(addrRes(decoupIp(adresse), compteurTransform(compteur), nb0)))
            compteur[-1] += int((256**nb0)/(int(nbSR))) - 3
            compteur = compteurTransform(compteur)
            print("Dernière adresse :", joindre(addrRes(decoupIp(adresse), compteurTransform(compteur), nb0)))
            compteur[-1] += 1
            compteur = compteurTransform(compteur)
            AddrDiff = joindre(addrRes(decoupIp(adresse), compteurTransform(compteur), nb0))
            print("Adresse de diffusion :", AddrDiff)
            verifBoucle = verifCompteur(compteur, nbSR)


            #définition du masque
            if nbReseau == 1:
                addrMask = AddrDiff
            MaskDecoup = decoupIp(str(SRMask(masque)))
            DecoupAddrDiff = decoupIp(addrMask)
            MaskDecoup[-1] = str(255 - int(DecoupAddrDiff[-1]))
            print("Masque réseau", joindre(MaskDecoup))
            nbReseau += 1
            compteur[-1] += 1
            compteur = compteurTransform(compteur)
            print("")
        return

IPaddr()





