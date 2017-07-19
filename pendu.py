import os
import sys
import pickle
from random import choice

def pendu():
    nom_fichier_scores = "scores"

    menu = 5

    jeu = 1
    afficheScores = 2
    quitte = 5
    maz = 3
    autreUtilisateur = 4

    nombre_coups = 8

    liste_mots = [
    "armoire",
    "boucle",
    "buisson",
    "bureau",
    "chaise",
    "carton",
    "couteau",
    "fichier",
    "garage",
    "glace",
    "journal",
    "kiwi",
    "lampe",
    "liste",
    "montagne",
    "remise",
    "sandale",
    "taxi",
    "vampire",
    "volant",
    ]

    #***************************************************************************
    def choix_nom_utilisateur():
        """ Get the user's name """

        return raw_input("What's your name? ")

    #***************************************************************************
    def charger_scores():
        """ Loading scores """

        if os.path.exists(nom_fichier_scores):
            with open(nom_fichier_scores, 'rb') as fichier:
                scores = pickle.Unpickler(fichier).load()
        else:
            scores = {}

        return scores

    #***************************************************************************
    def sauvegarder_scores(scores):
        """ Saving scores """

        with open(nom_fichier_scores, 'wb') as fichier:
            pickle.Pickler(fichier).dump(scores)


    #***************************************************************************
    def maz_scores(scores):
        """ Delete the scores' file """

    #    with open(nom_fichier_scores, 'rb') as fichier:
    #        scores = pickle.Unpickler(fichier).load()
        scores = {}

        sauvegarder_scores(scores)

        print"Scores deleted"

        return scores


    #***************************************************************************
    def generation_mot():
        """ Genere un mot aleatoire pour le jeu en fonction de la liste de
        mots
        """

        return choice(liste_mots)


    #***************************************************************************
    def masque_mot(mot_a_trouver, lettres_trouvees):
        """Affiche le mot a trouver avec les lettres manquantes masquees"""

        mot_masque = ''

        for lettre in mot_a_trouver:
            if lettre in lettres_trouvees:
                mot_masque += lettre
            else:
                mot_masque += '*'

        return mot_masque


    #***************************************************************************
    def choix_lettre(lettres_trouvees):
        """Recupere la lettre selectionnee par l'utilisateur"""

        lettre = raw_input("What letter? ")
        lettre = lettre.lower()

        if len(lettre) > 1 or not lettre.isalpha():
            print("You didn't pick a valid letter")
            return choix_lettre(lettres_trouvees)
        elif lettre in lettres_trouvees:
            print("You've already found this letter")
            return choix_lettre(lettres_trouvees)
        else:
            return lettre


    #***************************************************************************
    def afficher_menu(utilisateur):
        """Affiche un menu en debut de partie"""

        print("*************************").center(20)
        print("Pendu CocoPanda 2017\n".center(20))
        print("Welcome {}".format(utilisateur))
        print"{}. Play".format(jeu)
        print"{}. Display scores".format(afficheScores)
        print"{}. Delete scores".format(maz)
        print"{}. Change user".format(autreUtilisateur)
        print"{}. Quit".format(quitte)


    #***************************************************************************
    def choix_utilisateur():
        """Recuperation du choix de l'utilisateur"""

        choix = raw_input("Select: ")
        if not choix.isdigit():
            print("You didn't select a valid input for the menu")
            return choix_utilisateur
        else:
            choix = int(choix)
            if choix > menu:
                print("You didn't select a valid input for the menu")
                return choix_utilisateur
            else:
                return choix

    #***************************************************************************
    def afficher_scores(scores):
        """ Display scores """

        print("***********************************")
        print"* ",
        print"HALL OF FAME".center(29),
        print" *"

        for utilisateur, score in scores.items():
            print"* ",
            if score > 1:
                print"{} : {} points".format(utilisateur, score).center(29),
            else:
                print"{} : {} point".format(utilisateur, score).center(29),
            print(" *")
        print("***********************************")


    #***************************************************************************
    def afficher_score(utilisateur, scores):
        """ Display the user's socre"""

        if scores[utilisateur] > 1:
            print("{} a {} points".format(utilisateur, scores[utilisateur]))
        else:
            print("{} a {} point".format(utilisateur, scores[utilisateur]))


    #***************************************************************************
    def jouer(utilisateur, scores):
        """ Call the game """

        coups_restants = nombre_coups
        lettres_trouvees = []

        afficher_score(utilisateur, scores)

        # Generaion aleatoire d'un mot a partir de la liste de mots
        mot_a_trouver = generation_mot()
    #    print(mot_a_trouver)

        # Creation du mot avec masque
        mot_trouve = masque_mot(mot_a_trouver, lettres_trouvees)

        # Boucle de jeu tant qu'il reste des coups et que le mot n'est pas trouv
        while coups_restants > 0 and mot_trouve != mot_a_trouver:
            # Actualisation et affichage de la progression dans le mot a trouver

            print(mot_trouve)

            lettre = choix_lettre(lettres_trouvees)

            if lettre in mot_a_trouver:
                lettres_trouvees.append(lettre)
            else:
                coups_restants -= 1
                if coups_restants > 1:
                    print('You screwed up! Try again! {} hits left'.format(
                        coups_restants))
                elif coups_restants == 1:
                    print("You screwed up! Try again! Only 1 hit left")
                else:
                    print("Too many tries! You totally screwed up!")

            mot_trouve = masque_mot(mot_a_trouver, lettres_trouvees)

        # Actualisation du score du joueur
        scores[utilisateur] += coups_restants
        sauvegarder_scores(scores)

        afficher_score(utilisateur, scores)

        rejouer = raw_input("Would you like to play again? (Y/n) ")
        rejouer = rejouer.lower()
        if rejouer == '':
            rejouer = 'y'

        return rejouer


    #***************************************************************************
    def effacer_entree_scores(scores, utilisateur):
        """Permet d'effacer une entree du Hall of Fame en fonction du nom
        d'utilsateur indique
        """

        del scores[utilisateur]

        sauvegarder_scores(scores)

        return scores

    # Chargement des scores
    scores = charger_scores()

    # Choix du nom de l'utilisateur
    utilisateur = choix_nom_utilisateur()

    # Si l'utilisateur n'existe pas, on le cree
    if utilisateur not in scores.keys():
        scores[utilisateur] = 0

    while(1):
        rejouer = 'y'
        # Affichage du menu
        afficher_menu(utilisateur)
        # Recuperation choix utilisateur
        choix = choix_utilisateur()
        # Actions en fonction du choix de l'utilisateur
        if choix == jeu:
            while rejouer == 'y':
                rejouer = jouer(utilisateur, scores)

        elif choix == afficheScores:
            afficher_scores(scores)
            supprimer_score = raw_input("Would like to delete a score? (y/N) : ")
            supprimer_score = supprimer_score.lower()
            if supprimer_score == 'y':
                utilisateur_a_supprimer = raw_input(
    		"Write the name of the player: ")
                scores = effacer_entree_scores(scores, utilisateur_a_supprimer)
                if utilisateur not in scores.keys():
                    scores[utilisateur] = 0

        elif choix == maz:
            maz_scores(scores)
    #        scores = charger_scores()
    #        if scores == {}:
            scores[utilisateur] = 0

        elif choix == autreUtilisateur:
            utilisateur = choix_nom_utilisateur()
            if utilisateur not in scores.keys():
                scores[utilisateur] = 0

        elif choix == quitte:
            sys.exit(0)

if __name__ == "__main__":
    pendu()
