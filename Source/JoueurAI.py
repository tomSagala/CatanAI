#!/usr/bin/python
#-*- coding: latin-1 -*-


from Joueur import *
from Mappe import *
from random import randint
import random
import copy


################## Joueur Intelligent
class JoueurAI(Joueur):

    
    def __init__(self,id):
        super(JoueurAI,self).__init__(id)

        self.gamePhase = 0;
        self.premiereColonie = {}
        self.premiereIntersectionRoute = {}
        self.deuxiemeColonie = {}
        self.deuxiemeIntersectionRoute = {}
        self.modeColonieRoute = True
        self.phase = "COLONIEROUTE"
        self.constructionOuAchat = "COLONIE"
        self.valeurGeneralePrecedente = 100
        self.noRand = 0
        self.noDefiened = 0

        self.priorite = {}
        self.priorite[Ressource.ARGILE] = 10.0
        self.priorite[Ressource.BLE] = 9.0
        self.priorite[Ressource.BOIS] = 10.0
        self.priorite[Ressource.MINERAL] = 5.0
        self.priorite[Ressource.LAINE] = 7.0
        import json
        with open('catan.json', 'r') as fichierCatan:
            self.dictCatan = json.load(fichierCatan)

        debutValActionEchanger = self.dictCatan["debutPartie"]["actionEchanger"]
        debutValActionVille = self.dictCatan["debutPartie"]["actionVille"]
        debutValActionColonie = self.dictCatan["debutPartie"]["actionColonie"]
        debutValActionRoute = self.dictCatan["debutPartie"]["actionRoute"]
        debutValActionAcheterCarte = self.dictCatan["debutPartie"]["actionAcheterCarte"]
        debutValActionJouerCarteChevalier = self.dictCatan["debutPartie"]["actionJouerCarteChevalier"]

        miValActionEchanger = self.dictCatan["miPartie"]["actionEchanger"]
        miValActionVille = self.dictCatan["miPartie"]["actionVille"]
        miValActionColonie = self.dictCatan["miPartie"]["actionColonie"]
        miValActionRoute = self.dictCatan["miPartie"]["actionRoute"]
        miValActionAcheterCarte = self.dictCatan["miPartie"]["actionAcheterCarte"]
        miValActionJouerCarteChevalier = self.dictCatan["miPartie"]["actionJouerCarteChevalier"]

        finValActionEchanger = self.dictCatan["finPartie"]["actionEchanger"]
        finValActionVille = self.dictCatan["finPartie"]["actionVille"]
        finValActionColonie = self.dictCatan["finPartie"]["actionColonie"]
        finValActionRoute = self.dictCatan["finPartie"]["actionRoute"]
        finValActionAcheterCarte = self.dictCatan["finPartie"]["actionAcheterCarte"]
        finValActionJouerCarteChevalier = self.dictCatan["finPartie"]["actionJouerCarteChevalier"]

        #tableau des valeurs des actions
        valeursDebut = {}
        valeursDebut["2"] = sorted([(debutValActionEchanger["2"], "actionEchanger"), (debutValActionVille["2"], "actionVille"), (debutValActionColonie["2"], "actionColonie"), (debutValActionRoute["2"], "actionRoute"), (debutValActionAcheterCarte["2"], "actionAcheterCarte"), (debutValActionJouerCarteChevalier["2"], "actionJouerCarteChevalier")], key=lambda x:x[0], reverse=True)
        valeursDebut["3"] = sorted([(debutValActionEchanger["3"], "actionEchanger"), (debutValActionVille["3"], "actionVille"), (debutValActionColonie["3"], "actionColonie"), (debutValActionRoute["3"], "actionRoute"), (debutValActionAcheterCarte["3"], "actionAcheterCarte"), (debutValActionJouerCarteChevalier["3"], "actionJouerCarteChevalier")], key=lambda x:x[0], reverse=True)
        valeursDebut["4"] = sorted([(debutValActionEchanger["4"], "actionEchanger"), (debutValActionVille["4"], "actionVille"), (debutValActionColonie["4"], "actionColonie"), (debutValActionRoute["4"], "actionRoute"), (debutValActionAcheterCarte["4"], "actionAcheterCarte"), (debutValActionJouerCarteChevalier["4"], "actionJouerCarteChevalier")], key=lambda x:x[0], reverse=True)

        valeursMi = {}
        valeursMi["2"] = sorted([(miValActionEchanger["2"], "actionEchanger"), (miValActionVille["2"], "actionVille"), (miValActionColonie["2"], "actionColonie"), (miValActionRoute["2"], "actionRoute"), (miValActionAcheterCarte["2"], "actionAcheterCarte"), (miValActionJouerCarteChevalier["2"], "actionJouerCarteChevalier")], key=lambda x:x[0], reverse=True)
        valeursMi["3"] = sorted([(miValActionEchanger["3"], "actionEchanger"), (miValActionVille["3"], "actionVille"), (miValActionColonie["3"], "actionColonie"), (miValActionRoute["3"], "actionRoute"), (miValActionAcheterCarte["3"], "actionAcheterCarte"), (miValActionJouerCarteChevalier["3"], "actionJouerCarteChevalier")], key=lambda x:x[0], reverse=True)
        valeursMi["4"] = sorted([(miValActionEchanger["4"], "actionEchanger"), (miValActionVille["4"], "actionVille"), (miValActionColonie["4"], "actionColonie"), (miValActionRoute["4"], "actionRoute"), (miValActionAcheterCarte["4"], "actionAcheterCarte"), (miValActionJouerCarteChevalier["4"], "actionJouerCarteChevalier")], key=lambda x:x[0], reverse=True)
        valeursMi["5"] = sorted([(miValActionEchanger["5"], "actionEchanger"), (miValActionVille["5"], "actionVille"), (miValActionColonie["5"], "actionColonie"), (miValActionRoute["5"], "actionRoute"), (miValActionAcheterCarte["5"], "actionAcheterCarte"), (miValActionJouerCarteChevalier["5"], "actionJouerCarteChevalier")], key=lambda x:x[0], reverse=True)
        valeursMi["6"] = sorted([(miValActionEchanger["6"], "actionEchanger"), (miValActionVille["6"], "actionVille"), (miValActionColonie["6"], "actionColonie"), (miValActionRoute["6"], "actionRoute"), (miValActionAcheterCarte["6"], "actionAcheterCarte"), (miValActionJouerCarteChevalier["6"], "actionJouerCarteChevalier")], key=lambda x:x[0], reverse=True)

        valeursFin = {}
        valeursFin["2"] = sorted([(finValActionEchanger["2"], "actionEchanger"), (finValActionVille["2"], "actionVille"), (finValActionColonie["2"], "actionColonie"), (finValActionRoute["2"], "actionRoute"), (finValActionAcheterCarte["2"], "actionAcheterCarte"), (finValActionJouerCarteChevalier["2"], "actionJouerCarteChevalier")], key=lambda x:x[0], reverse=True)
        valeursFin["3"] = sorted([(finValActionEchanger["3"], "actionEchanger"), (finValActionVille["3"], "actionVille"), (finValActionColonie["3"], "actionColonie"), (finValActionRoute["3"], "actionRoute"), (finValActionAcheterCarte["3"], "actionAcheterCarte"), (finValActionJouerCarteChevalier["3"], "actionJouerCarteChevalier")], key=lambda x:x[0], reverse=True)
        valeursFin["4"] = sorted([(finValActionEchanger["4"], "actionEchanger"), (finValActionVille["4"], "actionVille"), (finValActionColonie["4"], "actionColonie"), (finValActionRoute["4"], "actionRoute"), (finValActionAcheterCarte["4"], "actionAcheterCarte"), (finValActionJouerCarteChevalier["4"], "actionJouerCarteChevalier")], key=lambda x:x[0], reverse=True)
        valeursFin["5"] = sorted([(finValActionEchanger["5"], "actionEchanger"), (finValActionVille["5"], "actionVille"), (finValActionColonie["5"], "actionColonie"), (finValActionRoute["5"], "actionRoute"), (finValActionAcheterCarte["5"], "actionAcheterCarte"), (finValActionJouerCarteChevalier["5"], "actionJouerCarteChevalier")], key=lambda x:x[0], reverse=True)
        valeursFin["6"] = sorted([(finValActionEchanger["6"], "actionEchanger"), (finValActionVille["6"], "actionVille"), (finValActionColonie["6"], "actionColonie"), (finValActionRoute["6"], "actionRoute"), (finValActionAcheterCarte["6"], "actionAcheterCarte"), (finValActionJouerCarteChevalier["6"], "actionJouerCarteChevalier")], key=lambda x:x[0], reverse=True)
        valeursFin["7"] = sorted([(finValActionEchanger["7"], "actionEchanger"), (finValActionVille["7"], "actionVille"), (finValActionColonie["7"], "actionColonie"), (finValActionRoute["7"], "actionRoute"), (finValActionAcheterCarte["7"], "actionAcheterCarte"), (finValActionJouerCarteChevalier["7"], "actionJouerCarteChevalier")], key=lambda x:x[0], reverse=True)
        valeursFin["8"] = sorted([(finValActionEchanger["8"], "actionEchanger"), (finValActionVille["8"], "actionVille"), (finValActionColonie["8"], "actionColonie"), (finValActionRoute["8"], "actionRoute"), (finValActionAcheterCarte["8"], "actionAcheterCarte"), (finValActionJouerCarteChevalier["8"], "actionJouerCarteChevalier")], key=lambda x:x[0], reverse=True)
        valeursFin["9"] = sorted([(finValActionEchanger["9"], "actionEchanger"), (finValActionVille["9"], "actionVille"), (finValActionColonie["9"], "actionColonie"), (finValActionRoute["9"], "actionRoute"), (finValActionAcheterCarte["9"], "actionAcheterCarte"), (finValActionJouerCarteChevalier["9"], "actionJouerCarteChevalier")], key=lambda x:x[0], reverse=True)
        valeursFin["10"] = sorted([(finValActionEchanger["10"], "actionEchanger"), (finValActionVille["10"], "actionVille"), (finValActionColonie["10"], "actionColonie"), (finValActionRoute["10"], "actionRoute"), (finValActionAcheterCarte["10"], "actionAcheterCarte"), (finValActionJouerCarteChevalier["10"], "actionJouerCarteChevalier")], key=lambda x:x[0], reverse=True)

        self.valeursActions = [valeursDebut, valeursMi, valeursFin]

        #tableau des actions du tour precedent
        self.actionsPrecedentes = [[],[],[]]

    def premierTour(self,mappe):
        
        self.premiereColonie = self.trouverMeilleureIntersectionColonie(mappe)
        self.premiereIntersectionRoute = self.trouverMeilleureIntersectionRoute(self.premiereColonie,mappe)
                           
        return (self.premiereColonie._id,self.premiereIntersectionRoute._id)
        
    
    def deuxiemeTour(self,mappe):

        self.deuxiemeColonie = self.trouverMeilleureIntersectionColonie(mappe)
        self.deuxiemeIntersectionRoute = self.trouverMeilleureIntersectionRoute(self.deuxiemeColonie,mappe)

        return (self.deuxiemeColonie._id,self.deuxiemeIntersectionRoute._id)


    def choisirAction(self,mappe,infoJoueurs,paquetCartesVide):

        actionsPossibles = []

        if self.quantiteRessources(Ressource.BLE) >= 2 or self.quantiteRessources(Ressource.ARGILE) >= 2 or self.quantiteRessources(Ressource.BOIS) >= 2 or self.quantiteRessources(Ressource.MINERAL) >= 2 or self.quantiteRessources(Ressource.LAINE) >= 2:
            if self.echangesPossibles():
                for e in self.echangesPossibles():
                    actionsPossibles.append((Action.ECHANGER_RESSOURCES,[e[0],e[1],e[2]]))
        
        if self.possibleAjouterVille(mappe):
            for v in self.possibleAjouterVille(mappe):
                if v is int:
                    actionsPossibles.append((Action.AJOUTER_VILLE,[v._id]))

        if self.possibleAjouterColonie(mappe):
            for c in self.possibleAjouterColonie(mappe):
                if c is int:
                    actionsPossibles.append((Action.AJOUTER_COLONIE,[c._id]))

        if self.possibleAjouterRoute(mappe):
            for r in self.possibleAjouterRoute(mappe):
                actionsPossibles.append((Action.AJOUTER_ROUTE,[r[0],r[1]]))

        if self.peutJouerCarteChevalier():
            actionsPossibles.append((Action.JOUER_CARTE_CHEVALIER, self.deciderJouerCarteChevalier(mappe,infoJoueurs)))

        if self.possibleAcheterCarte():
            actionsPossibles.append(Action.ACHETER_CARTE)

        leaderPoints = max(infoJoueurs,key=lambda x:x[0])[0]

        if (leaderPoints >= 7 or self._pointsVictoire >= 7) and self.gamePhase != 2:
            self.gamePhase = 2
            self.priorite[Ressource.MINERAL] +=2.0
            self.priorite[Ressource.BOIS] -=1.0
            self.priorite[Ressource.ARGILE] -=1.0

        elif ((leaderPoints >= 5 and leaderPoints < 7) or (self._pointsVictoire >= 5 and self._pointsVictoire < 7)) and self.gamePhase == 0:
            self.gamePhase = 1
            self.priorite[Ressource.BOIS] -=1.0
            self.priorite[Ressource.ARGILE] -=1.0
            self.priorite[Ressource.MINERAL] +=3.0

        elif leaderPoints < 5 and self._pointsVictoire < 5 and self.gamePhase != 0:
            self.gamePhase = 0

        action = None
        valeurs = copy.deepcopy(self.valeursActions[self.gamePhase][str(min(self._pointsVictoire,10))])
        favoriteAction = ""

        while len(valeurs) > 0 and action is None and len(actionsPossibles) > 0:

            favoriteAction = valeurs[0][1]

            randomChance = math.exp(-valeurs[0][0]/100.0)
            #if (float(valeurs[0][0])+100.0)> 0:
             #  randomChance = 100.0/(float(valeurs[0][0])+100.0)
            #else:
             #   randomChance = 1

            if random.uniform(0.0, 1.0) < randomChance:
                rand = randint(0,len(valeurs)-1)
                favoriteAction = valeurs[rand][1]
                self.noRand += 1
                valeurs.pop(rand)
            else :
                valeurs.pop(0)
                self.noDefiened +=1

            if favoriteAction is "actionVille":
                action = self.actionAjouterVille(actionsPossibles)

            elif favoriteAction is "actionColonie":
                action = self.actionAjouterColonie(actionsPossibles)

            elif favoriteAction is "actionRoute":
                action = self.actionAjouterRoute(actionsPossibles)

            elif favoriteAction is "actionAcheterCarte" and not paquetCartesVide:
                action = self.actionAcheterCarte(actionsPossibles)

            elif favoriteAction is "actionJouerCarteChevalier":
                action = self.actionJouerChevalier(actionsPossibles)

            elif favoriteAction is "actionEchanger":
                action = self.actionEchangerRessources(actionsPossibles)


        if action is not None:


            self.actionsPrecedentes[self.gamePhase].append((favoriteAction, leaderPoints, str(min(self._pointsVictoire,10))))
            return action

        return Action.TERMINER

    def actionAjouterVille(self, actionsPossibles):
        for a in actionsPossibles:
            if type(a) is not int:
                if a[0] == Action.AJOUTER_VILLE:
                    return a
        return None

    def actionAjouterColonie(self, actionsPossibles):
        for a in actionsPossibles:
            if type(a) is not int:
                if a[0] == Action.AJOUTER_COLONIE:
                    return a
        return None

    def actionAjouterRoute(self, actionsPossibles):
        for a in actionsPossibles:
            if type(a) is not int:
                if a[0] == Action.AJOUTER_ROUTE:
                    return a
        return None

    def actionAcheterCarte(self, actionsPossibles):
        for a in actionsPossibles:
            if type(a) is int:
                if self.possibleAcheterCarte():
                    return (Action.ACHETER_CARTE,[])
        return None

    def actionJouerChevalier(self, actionsPossibles):
        for a in actionsPossibles:
            if type(a) is not int:
                if a[0] == Action.JOUER_CARTE_CHEVALIER:
                    return a
        return None

    def actionEchangerRessources(self, actionsPossibles):
        for a in actionsPossibles:
            if type(a) is not int:
                if a[0] == Action.ECHANGER_RESSOURCES:
                    if self.deciderCommerce() != False:
                        return (Action.ECHANGER_RESSOURCES, self.deciderCommerce())
                    else:
                        return a

    def finDePartie(self,mappe,joueurID):
        self.calculFinDePartie()
        import json
        with open('catan.json', 'w') as fichierCatan:
            json.dump(self.dictCatan, fichierCatan)

        import csv
        with open('catan.csv', 'ab') as f:
            csvWriter = csv.writer(f, delimiter=' ', skipinitialspace=True)
            if self._id == joueurID:
                print "I Win"
                csvWriter.writerow([1])
            else:
                csvWriter.writerow([0])

    def calculFinDePartie(self):
        #bonus pour le resultat final
        rewardPartie=-1
        if self._pointsVictoire >= 10:
            rewardPartie=1

        if len(self.actionsPrecedentes[1]) > 0:
            rewardDebut = -1.0
            if int(self.actionsPrecedentes[1][0][2]) >= 5:
                rewardDebut = 1.0

            for i in range (0, len(self.actionsPrecedentes[0])):
                self.dictCatan['debutPartie'][self.actionsPrecedentes[0][i][0]][str(self.actionsPrecedentes[0][i][2])] += rewardDebut

        if len(self.actionsPrecedentes[2]) > 0:
            rewardMid = -1.0
            if int(self.actionsPrecedentes[2][0][2]) >= 7:
                rewardMid = 1.0

            for i in range (0, len(self.actionsPrecedentes[1])):
                self.dictCatan['miPartie'][self.actionsPrecedentes[1][i][0]][str(self.actionsPrecedentes[1][i][2])] += rewardMid

        if len(self.actionsPrecedentes[2]) > 0:
            rewardEnd = -1.0
            if self._pointsVictoire >= 10:
                rewardEnd = 1.0

            for i in range (0, len(self.actionsPrecedentes[2])):
                self.dictCatan['finPartie'][self.actionsPrecedentes[2][i][0]][str(self.actionsPrecedentes[2][i][2])] += rewardEnd

    def trouverMeilleureIntersectionColonie(self,mappe):

        meilleureValeurProduction = 0
        meilleureIntersection = 0

        for i in mappe.obtenirToutesLesIntersections(): #pour toutes les intersections

            if mappe.peutConstruireOccupationInitial(i._id): #si on peut poser une colonie sur l'intersection
                if not i.occupe():
                            
                    valeurProduction = 0
                                        
                    for t in i.obtenirTerritoiresVoisins(): #pour tous les territoires de l'intersection
                        if t._valeur != 0:
                            valeurProduction += self.priorite[t.ressource()]*self.obtenirValeurProductionChiffre(t._valeur) #on accumule les valeurs de production

                    if valeurProduction > meilleureValeurProduction: #comparaison avec la meilleure valeure actuelle
                        meilleureValeurProduction = valeurProduction
                        meilleureIntersection = i
                            
                    elif valeurProduction == meilleureValeurProduction and valeurProduction != 0: #si on egale la meilleure valeur de production
                        for t in meilleureIntersection.obtenirTerritoiresVoisins():
                            if t._valeur == 6 or t._valeur == 8: #si la meilleure actuelle a un 6 ou un 8 (a eviter pour eloigner le brigand)
                                meilleureValeurProduction = valeurProduction
                                meilleureIntersection = i

        for t in meilleureIntersection.obtenirTerritoiresVoisins(): #pour tous les territoires de l'intersection
                        if t._valeur != 0:
                            self.priorite[t.ressource()] -=1

        return meilleureIntersection

    def trouverMeilleureIntersectionRoute(self,intersection,mappe):

        coinsInteressants = []
        
        for i in intersection.obtenirVoisins():
            if [j for j in i.obtenirVoisins() if not j.occupe() and j != intersection] != []:
                coinsInteressants.append(i)

        if coinsInteressants:
            for i in coinsInteressants:
                if isinstance(i,PortGenerique) or isinstance(i,PortSpecialise):
                    return i
            return coinsInteressants[0]  
        else:
            meilleureIntersection = intersection.obtenirVoisins()[0]
            meilleureValeurProduction = 0
            for i in intersection.obtenirVoisins():
                if mappe.peutConstruireOccupationInitial(i._id): #si on peut poser une colonie sur l'intersection
                    valeurProduction = 0
                                            
                    for t in i.obtenirTerritoiresVoisins(): #pour tous les territoires de l'intersection
                        valeurProduction += self.obtenirValeurProductionChiffre(t._valeur) #on accumule les valeurs de production

                    if valeurProduction >= meilleureValeurProduction: #comparaison avec la meilleure valeure actuelle
                        meilleureValeurProduction = valeurProduction
                        meilleureIntersection = i
            return meilleureIntersection


        assert(False)


                                        
    def obtenirValeurProductionChiffre(self,chiffre):

        if chiffre == 2 or chiffre == 12:
            return 1
        elif chiffre == 3 or chiffre == 11:
            return 2
        elif chiffre == 4 or chiffre == 10:
            return 3
        elif chiffre == 5 or chiffre == 9:
            return 4
        elif chiffre == 0:
            return 0
        else:
            return 5
        

    def deciderJouerCarteChevalier(self,mappe,infoJoueurs):

        tableauJoueur = [];


        for i in range(0, len(infoJoueurs), 1):
            if i is not self._id:
                tableauJoueur.append([i, infoJoueurs[i]])

        tableauJoueur = sorted(tableauJoueur,key=lambda x:x[1][0], reverse = True)

        for i in range(0, len(tableauJoueur)):
            for t in mappe.obtenirTousLesTerritoires():
                if t._valeur == 6 or t._valeur == 8:
                    if t is not mappe.obtenirTerritoireContenantVoleurs():
                        for j in t.obtenirVoisins():
                            if j.obtenirOccupant() != self._id and j.obtenirOccupant() == tableauJoueur[i][0]:
                                return[t._id, tableauJoueur[i][0]]


        # si on ne trouve pas de case approprié
        territoire = mappe.obtenirNumerosIntersectionsJoueur(tableauJoueur[i][0])
        return [territoire[0]._id, tableauJoueur[i][0]]



        

    def deciderCommerce(self):

        ressourceEnManque = self.ressourceEnManque()

        if ressourceEnManque != False:
            
            if ressourceEnManque == Ressource.BOIS:
                
                if self.choisirEchange(Ressource.MINERAL, Ressource.BOIS) != False:
                    return self.choisirEchange(Ressource.MINERAL,Ressource.BOIS)

                if self.choisirEchange(Ressource.LAINE, Ressource.BOIS) != False:
                    return self.choisirEchange(Ressource.LAINE, Ressource.BOIS)

                if self.choisirEchange(Ressource.BLE, Ressource.BOIS) != False:
                    return self.choisirEchange(Ressource.BLE, Ressource.BOIS)

                if self.choisirEchange(Ressource.ARGILE, Ressource.BOIS) != False:
                    return self.choisirEchange(Ressource.ARGILE, Ressource.BOIS)
                
                return False
                
            elif ressourceEnManque == Ressource.ARGILE:

                if self.choisirEchange(Ressource.MINERAL, Ressource.ARGILE) != False:
                    return self.choisirEchange(Ressource.MINERAL,Ressource.ARGILE)

                if self.choisirEchange(Ressource.LAINE, Ressource.ARGILE) != False:
                    return self.choisirEchange(Ressource.LAINE, Ressource.ARGILE)

                if self.choisirEchange(Ressource.BLE, Ressource.ARGILE) != False:
                    return self.choisirEchange(Ressource.BLE, Ressource.ARGILE)

                if self.choisirEchange(Ressource.BOIS, Ressource.ARGILE) != False:
                    return self.choisirEchange(Ressource.BOIS, Ressource.ARGILE)

                return False
                
            elif ressourceEnManque == Ressource.MINERAL:

                if self.choisirEchange(Ressource.BOIS, Ressource.MINERAL) != False:
                    return self.choisirEchange(Ressource.BOIS,Ressource.MINERAL)

                if self.choisirEchange(Ressource.ARGILE, Ressource.MINERAL) != False:
                    return self.choisirEchange(Ressource.ARGILE, Ressource.MINERAL)

                return False
                                        

            elif ressourceEnManque == Ressource.BLE:

                if self.choisirEchange(Ressource.BOIS, Ressource.BLE) != False:
                    return self.choisirEchange(Ressource.BOIS, Ressource.BLE)
                
                if self.choisirEchange(Ressource.LAINE, Ressource.BLE) != False:
                    return self.choisirEchange(Ressource.LAINE, Ressource.BLE)

                if self.choisirEchange(Ressource.ARGILE, Ressource.BLE) != False:
                    return self.choisirEchange(Ressource.ARGILE, Ressource.BLE)

                if self.choisirEchange(Ressource.MINERAL, Ressource.BLE) != False:
                    return self.choisirEchange(Ressource.MINERAL, Ressource.BLE)

                return False
            
            elif ressourceEnManque == Ressource.LAINE:

                if self.choisirEchange(Ressource.MINERAL, Ressource.LAINE) != False:
                    return self.choisirEchange(Ressource.MINERAL, Ressource.LAINE)

                if self.choisirEchange(Ressource.ARGILE, Ressource.LAINE) != False:
                    return self.choisirEchange(Ressource.ARGILE, Ressource.LAINE)

                return False
            
        return False
                            
    
    def ressourceEnManque(self):


        if self.quantiteRessources(Ressource.BLE) == 0:
            return Ressource.BLE
        if self.quantiteRessources(Ressource.ARGILE) == 0:
            return Ressource.ARGILE
        if self.quantiteRessources(Ressource.BOIS) == 0:
            return Ressource.BOIS
        if self.quantiteRessources(Ressource.LAINE) == 0:
            return Ressource.LAINE
        if self.quantiteRessources(Ressource.MINERAL) == 0:
            return Ressource.MINERAL


        return False


        valeurs = copy.deepcopy(self.valeursActions[self.gamePhase])

        while len(valeurs) > 0:

            favoriteAction = valeurs[0][1]

            valeurs.pop(0)

            if favoriteAction is "actionVille" and (not self.quantiteRessources(Ressource.BLE) >= 2 or not self.quantiteRessources(Ressource.MINERAL) >= 3):
                if self.quantiteRessources(Ressource.BLE) >= 2 :
                    return Ressource.BLE
                return Ressource.MINERAL

            elif favoriteAction is "actionColonie" and (not self.quantiteRessources(Ressource.BLE) >= 1 or not self.quantiteRessources(Ressource.ARGILE) >= 1 or not self.quantiteRessources(Ressource.BOIS) >= 1 or not self.quantiteRessources(Ressource.LAINE) >= 1):
                if self.quantiteRessources(Ressource.BLE) >= 1:
                    return Ressource.BLE
                if self.quantiteRessources(Ressource.ARGILE) >= 1:
                    return Ressource.ARGILE
                if self.quantiteRessources(Ressource.BOIS) >= 1:
                    return Ressource.BOIS
                return Ressource.LAINE

            elif favoriteAction is "actionRoute" and (not self.quantiteRessources(Ressource.BOIS) >= 1 or not self.quantiteRessources(Ressource.ARGILE) >= 1):
                if self.quantiteRessources(Ressource.BOIS) >= 1:
                    return Ressource.BOIS
                return Ressource.ARGILE

            elif favoriteAction is "actionAcheterCarte" and (not self.quantiteRessources(Ressource.BLE) >= 1 or not self.quantiteRessources(Ressource.LAINE) >= 1 or not self.quantiteRessources(Ressource.MINERAL) >= 1):
                if self.quantiteRessources(Ressource.BLE) >= 1:
                    return Ressource.BLE
                if self.quantiteRessources(Ressource.LAINE) >= 1:
                    return Ressource.LAINE
                return Ressource.MINERAL

        return False


    def choisirEchange(self,ressourceOfferte,ressourceDemandee):
        
        if self.quantiteRessources(ressourceOfferte) < 2:
            return False
        
        elif self.quantiteRessources(ressourceOfferte) == 2:

            if ressourceOfferte in self._peutEchanger:
                return [2, ressourceOfferte, ressourceDemandee]           
            
        elif self.quantiteRessources(ressourceOfferte) >= 3 and self.quantiteRessources(ressourceOfferte) < 5:

            if ressourceOfferte in self._peutEchanger:
                return [2, ressourceOfferte, ressourceDemandee]

            if self._possedePortGenerique:
                return [3, ressourceOfferte, ressourceDemandee]
            

        elif self.quantiteRessources(ressourceOfferte) >= 5:

            if ressourceOfferte in self._peutEchanger:
                return [2, ressourceOfferte, ressourceDemandee]

            if self._possedePortGenerique:
                return [3, ressourceOfferte, ressourceDemandee]

            return [4, ressourceOfferte, ressourceDemandee]
        

        return False

    def echangesPossibles(self):

        echangesPossibles = []
        
        
        if self._peutEchanger:

            
            if Ressource.BOIS in self._peutEchanger:
                
                if self.quantiteRessources(Ressource.BOIS) >= 2:
                    echangesPossibles.append([2, Ressource.BOIS, Ressource.ARGILE])
                    echangesPossibles.append([2, Ressource.BOIS, Ressource.MINERAL])
                    echangesPossibles.append([2, Ressource.BOIS, Ressource.BLE])
                    echangesPossibles.append([2, Ressource.BOIS, Ressource.LAINE])

            if Ressource.ARGILE in self._peutEchanger:
                
                if self.quantiteRessources(Ressource.ARGILE) >= 2:
                    echangesPossibles.append([2, Ressource.ARGILE, Ressource.BOIS])
                    echangesPossibles.append([2, Ressource.ARGILE, Ressource.MINERAL])
                    echangesPossibles.append([2, Ressource.ARGILE, Ressource.BLE])
                    echangesPossibles.append([2, Ressource.ARGILE, Ressource.LAINE])

            if Ressource.MINERAL in self._peutEchanger:
                
                if self.quantiteRessources(Ressource.MINERAL) >= 2:
                    echangesPossibles.append([2, Ressource.MINERAL, Ressource.BOIS])
                    echangesPossibles.append([2, Ressource.MINERAL, Ressource.ARGILE])
                    echangesPossibles.append([2, Ressource.MINERAL, Ressource.BLE])
                    echangesPossibles.append([2, Ressource.MINERAL, Ressource.LAINE])

            if Ressource.BLE in self._peutEchanger:
                
                if self.quantiteRessources(Ressource.BLE) >= 2:
                    echangesPossibles.append([2, Ressource.BLE, Ressource.BOIS])
                    echangesPossibles.append([2, Ressource.BLE, Ressource.ARGILE])
                    echangesPossibles.append([2, Ressource.BLE, Ressource.MINERAL])
                    echangesPossibles.append([2, Ressource.BLE, Ressource.LAINE])

            if Ressource.LAINE in self._peutEchanger:
                
                if self.quantiteRessources(Ressource.LAINE) >= 2:
                    echangesPossibles.append([2, Ressource.LAINE, Ressource.BOIS])
                    echangesPossibles.append([2, Ressource.LAINE, Ressource.ARGILE])
                    echangesPossibles.append([2, Ressource.LAINE, Ressource.MINERAL])
                    echangesPossibles.append([2, Ressource.LAINE, Ressource.BLE])
                

        if self._possedePortGenerique:

            if self.quantiteRessources(Ressource.BOIS) >= 3:
                echangesPossibles.append([3, Ressource.BOIS, Ressource.ARGILE])
                echangesPossibles.append([3, Ressource.BOIS, Ressource.MINERAL])
                echangesPossibles.append([3, Ressource.BOIS, Ressource.BLE])
                echangesPossibles.append([3, Ressource.BOIS, Ressource.LAINE])

            if self.quantiteRessources(Ressource.ARGILE) >= 3:
                echangesPossibles.append([3, Ressource.ARGILE, Ressource.BOIS])
                echangesPossibles.append([3, Ressource.ARGILE, Ressource.MINERAL])
                echangesPossibles.append([3, Ressource.ARGILE, Ressource.BLE])
                echangesPossibles.append([3, Ressource.ARGILE, Ressource.LAINE])

            if self.quantiteRessources(Ressource.MINERAL) >= 3:
                echangesPossibles.append([3, Ressource.MINERAL, Ressource.BOIS])
                echangesPossibles.append([3, Ressource.MINERAL, Ressource.ARGILE])
                echangesPossibles.append([3, Ressource.MINERAL, Ressource.BLE])
                echangesPossibles.append([3, Ressource.MINERAL, Ressource.LAINE])

            if self.quantiteRessources(Ressource.BLE) >= 3:
                echangesPossibles.append([3, Ressource.BLE, Ressource.BOIS])
                echangesPossibles.append([3, Ressource.BLE, Ressource.ARGILE])
                echangesPossibles.append([3, Ressource.BLE, Ressource.MINERAL])
                echangesPossibles.append([3, Ressource.BLE, Ressource.LAINE])

            if self.quantiteRessources(Ressource.LAINE) >= 3:
                echangesPossibles.append([3, Ressource.LAINE, Ressource.BOIS])
                echangesPossibles.append([3, Ressource.LAINE, Ressource.ARGILE])
                echangesPossibles.append([3, Ressource.LAINE, Ressource.MINERAL])
                echangesPossibles.append([3, Ressource.LAINE, Ressource.BLE])
            

        if self.quantiteRessources(Ressource.BOIS) >= 4:
            echangesPossibles.append([4, Ressource.BOIS, Ressource.ARGILE])
            echangesPossibles.append([4, Ressource.BOIS, Ressource.MINERAL])
            echangesPossibles.append([4, Ressource.BOIS, Ressource.BLE])
            echangesPossibles.append([4, Ressource.BOIS, Ressource.LAINE])

        if self.quantiteRessources(Ressource.ARGILE) >= 4:
            echangesPossibles.append([4, Ressource.ARGILE, Ressource.BOIS])
            echangesPossibles.append([4, Ressource.ARGILE, Ressource.MINERAL])
            echangesPossibles.append([4, Ressource.ARGILE, Ressource.BLE])
            echangesPossibles.append([4, Ressource.ARGILE, Ressource.LAINE])

        if self.quantiteRessources(Ressource.MINERAL) >= 4:
            echangesPossibles.append([4, Ressource.MINERAL, Ressource.BOIS])
            echangesPossibles.append([4, Ressource.MINERAL, Ressource.ARGILE])
            echangesPossibles.append([4, Ressource.MINERAL, Ressource.BLE])
            echangesPossibles.append([4, Ressource.MINERAL, Ressource.LAINE])

        if self.quantiteRessources(Ressource.BLE) >= 4:
            echangesPossibles.append([4, Ressource.BLE, Ressource.BOIS])
            echangesPossibles.append([4, Ressource.BLE, Ressource.ARGILE])
            echangesPossibles.append([4, Ressource.BLE, Ressource.MINERAL])
            echangesPossibles.append([4, Ressource.BLE, Ressource.LAINE])

        if self.quantiteRessources(Ressource.LAINE) >= 4:
            echangesPossibles.append([4, Ressource.LAINE, Ressource.BOIS])
            echangesPossibles.append([4, Ressource.LAINE, Ressource.ARGILE])
            echangesPossibles.append([4, Ressource.LAINE, Ressource.MINERAL])
            echangesPossibles.append([4, Ressource.LAINE, Ressource.BLE])


        if echangesPossibles:
            return echangesPossibles

        return False

            

    def deciderConstructionAchat(self,mappe):


        if not self._peutEchanger:
            if not self._possedePortGenerique:
                versPort = self.allerVersPort(mappe)

                if versPort != False:
                    return versPort

        self.constructionOuAchat = "VILLE"

        futureVille = self.choisirFutureVille(mappe)

        if futureVille != False:
            return futureVille._id

        self.constructionOuAchat = "COLONIE"

        futureColonie = self.choisirFutureColonie(mappe)

        if futureColonie != False:
            return futureColonie._id

        self.constructionOuAchat = "ROUTE"
        futureRoute = self.choisirFutureRoute(mappe)

        if futureRoute != False:
            return futureRoute

        self.constructionOuAchat = "ACHETER CARTE"

        if self.possibleAcheterCarte():
            return (Action.ACHETER_CARTE,[])

        self.constructionOuAchat = "RIEN"

        return False

        

    def choisirFutureVille(self,mappe):
        
        colonies = self.possibleAjouterVille(mappe)
        meilleureValeurProduction = 0
        futureVille = 0

        if colonies != False:

            futureVille = colonies[0]

            for i in colonies:
                
                valeurProduction = 0      #demarche pour trouver la meilleure valeur de production

                for t in i.obtenirTerritoiresVoisins():
                    if t._valeur !=0:
                        valeurProduction += self.priorite[t.ressource()]*self.obtenirValeurProductionChiffre(t._valeur)

                if valeurProduction > meilleureValeurProduction:
                    meilleureValeurProduction = valeurProduction
                    futureVille = i

            if futureVille !=0:
                for t in futureVille.obtenirTerritoiresVoisins():
                    if t._valeur !=0:
                        self.priorite[t.ressource()] -=1

            return futureVille._id

        return False

    

    def possibleAjouterVille(self,mappe):

        colonies = []

        if self.quantiteRessources(Ressource.BLE) >= 2 and self.quantiteRessources(Ressource.MINERAL) >= 3:
            for i in mappe.obtenirToutesLesIntersections():
                if i.occupe() and i.obtenirOccupant() == self._id and i.occupation() == 1:
                    colonies.append(i)

        if colonies:
            return colonies
        
        else:
            return False



    def choisirFutureColonie(self,mappe):

        possiblesIntersections = self.possibleAjouterColonie(mappe)

        meilleureValeurProduction = 0
        futureColonie = 0

        if possiblesIntersections != False:

            for i in possiblesIntersections:

                valeurProduction = 0

                for t in i.obtenirTerritoiresVoisins():
                    if t._valeur !=0:
                        valeurProduction += self.priorite[t.ressource()]*self.obtenirValeurProductionChiffre(t._valeur)

                if valeurProduction > meilleureValeurProduction:
                    meilleureValeurProduction = valeurProduction
                    futureColonie = i

            if futureColonie != 0:
                for t in futureColonie.obtenirTerritoiresVoisins():
                    if t._valeur !=0:
                        self.priorite[t.ressource()] -=1

                return futureColonie._id

        return False

                    
                                                                                        
    def possibleAjouterColonie(self,mappe):

        possiblesIntersections = []
        
        if self.quantiteRessources(Ressource.BLE) >= 1 and self.quantiteRessources(Ressource.ARGILE) >= 1 and self.quantiteRessources(Ressource.BOIS) >= 1 and self.quantiteRessources(Ressource.LAINE) >= 1:
            for i in mappe.obtenirToutesLesIntersections():
                if mappe.peutConstruireOccupation(i._id,self._id):
                    if not i.occupe():
                        if i!=None:
                            possiblesIntersections.append(i)

        if possiblesIntersections:
            return possiblesIntersections
                
        return False

    

    def choisirFutureRoute(self,mappe):

        possiblesRoutes = []
        meilleureValeurProduction = 0
        futureRoute = 0

        if self.possibleAjouterRoute(mappe):
            for i in mappe.obtenirToutesLesIntersections():
                if mappe._accesRoute(i._id,self._id):
                    for j in i.obtenirVoisins():
                        if mappe.peutConstruireRoute(i._id,j._id,self._id):
                            if not mappe.intersectionPossedeRoute(i._id,j._id):
                                possiblesRoutes.append([i._id,j._id])

        if possiblesRoutes:
            
            for r in possiblesRoutes:
                
                valeurProduction = 0

                for t in r[1].obtenirTerritoiresVoisins():
                    valeurProduction += self.obtenirValeurProductionChiffre(t._valeur)

                if valeurProduction > meilleureValeurProduction:
                    meilleureValeurProduction = valeurProduction
                    futureRoute = [r[0],r[1]]

            return futureRoute
                

        return False
                            
                
        

    def possibleAjouterRoute(self,mappe):

        emplacementsPossibles = []
        
        if self.quantiteRessources(Ressource.BOIS) >= 1 and self.quantiteRessources(Ressource.ARGILE) >= 1:
            for i in mappe.obtenirToutesLesIntersections():
                for j in i.obtenirVoisins():
                    if mappe.peutConstruireRoute(i._id,j._id,self._id):
                        if [j._id,i._id] not in emplacementsPossibles:
                            emplacementsPossibles.append([i._id,j._id])

        if emplacementsPossibles:
            return emplacementsPossibles
            
        return False
            

    def possibleAcheterCarte(self):
        
        if self.quantiteRessources(Ressource.BLE) >= 1 and self.quantiteRessources(Ressource.LAINE) >= 1 and self.quantiteRessources(Ressource.MINERAL) >= 1:
            return True

        else:
            return False
    

    def allerVersPort(self,mappe):

        for i in mappe.obtenirToutesLesIntersections():
            
            if isinstance(i, PortGenerique):

                self.constructionOuAchat = "COLONIE"
                if self.quantiteRessources(Ressource.BLE) >= 1 and self.quantiteRessources(Ressource.ARGILE) >= 1 and self.quantiteRessources(Ressource.BOIS) >= 1 and self.quantiteRessources(Ressource.LAINE) >= 1:
                    if mappe.peutConstruireOccupation(i._id, self._id):
                        if i != None:
                            return i._id

                self.constructionOuAchat = "ROUTE"
                
                if self.possibleAjouterRoute(mappe):
                    
                    for j in i.obtenirVoisins():
                        
                        if mappe._accesRoute(j._id,self._id):
                            if mappe.peutConstruireRoute(j._id,i._id,self._id):
                                return [j._id,i._id]
                        else:
                            for k in j.obtenirVoisins():
                                if k != i:
                                    if k.obtenirOccupant() == self._id:
                                        if mappe.peutConstruireRoute(k._id,j._id,self._id):
                                            return [k._id,j._id]

                                    else:
                                        for l in k.obtenirVoisins():
                                            if l != j:
                                                if l.obtenirOccupant() == self._id:
                                                    if mappe.peutConstruireRoute(l._id,k._id,self._id):
                                                        return [l._id,k._id]
                                                    

        for i in mappe.obtenirToutesLesIntersections():
                            
            if isinstance(i, PortSpecialise):

                
                self.constructionOuAchat = "COLONIE"
                if self.quantiteRessources(Ressource.BLE) >= 1 and self.quantiteRessources(Ressource.ARGILE) >= 1 and self.quantiteRessources(Ressource.BOIS) >= 1 and self.quantiteRessources(Ressource.LAINE) >= 1:
                    if mappe.peutConstruireOccupation(i._id, self._id):
                        return i._id

                    
                self.constructionOuAchat = "ROUTE"
                if self.possibleAjouterRoute(mappe):
                    for j in i.obtenirVoisins():
                        if mappe._accesRoute(j._id,self._id):
                            if mappe.peutConstruireRoute(j._id,i._id,self._id):
                                return [j._id,i._id]
                        else:
                            for k in j.obtenirVoisins():
                                if k != i:
                                    if k.obtenirOccupant() == self._id:                                        
                                        if mappe.peutConstruireRoute(k._id,j._id,self._id):
                                            return [k._id,j._id]
                                    else:
                                        for l in k.obtenirVoisins():
                                            if l != j:
                                                if l.obtenirOccupant() == self._id:
                                                    if mappe.peutConstruireRoute(l._id,k._id,self._id):
                                                        return [l._id,k._id]

        
        return False


    # Retire un nombre de ressources égal à la quantité fournie en paramètre
    def volerRessources(self,quantite):

        if not self._ressources[Ressource.BLE] == 0:
            importanceBle = self.priorite[Ressource.BLE] / self._ressources[Ressource.BLE]
        else:
            importanceBle = 0

        if not self._ressources[Ressource.ARGILE] == 0:
            importanceArgile = self.priorite[Ressource.ARGILE] / self._ressources[Ressource.ARGILE]
        else:
            importanceArgile = 0

        if not self._ressources[Ressource.BOIS] == 0:
            importanceBois = self.priorite[Ressource.BOIS] / self._ressources[Ressource.BOIS]
        else:
            importanceBois = 0

        if not self._ressources[Ressource.MINERAL] == 0:
            importanceMineral = self.priorite[Ressource.MINERAL] / self._ressources[Ressource.MINERAL]
        else:
            importanceMineral = 0

        if not self._ressources[Ressource.LAINE] == 0:
            importanceLaine =  self.priorite[Ressource.LAINE] / self._ressources[Ressource.LAINE]
        else:
            importanceLaine = 0

        tableauImportance = [[Ressource.BLE, importanceBle], [Ressource.ARGILE, importanceArgile], [Ressource.BOIS, importanceBois], [Ressource.MINERAL, importanceMineral], [Ressource.LAINE, importanceLaine]]

        for i in range(len(tableauImportance) - 1, 0, -1):
            for j in range(i):
                if tableauImportance[j][1] > tableauImportance[j + 1][1]:
                    valTemporaire = tableauImportance[j]
                    tableauImportance[j] = tableauImportance[j + 1]
                    tableauImportance[j + 1] = valTemporaire

        for k in range(0, len(tableauImportance) - 1, 1):
             while quantite > 0 and self._ressources[tableauImportance[k][0]] > 1:
                self._ressources[tableauImportance[k][0]] -= 1
                quantite -= 1



                 
            
            


                
            
            
            
            
        




        
        
        
        

                
            
        
        
        
        
        
                    
                


