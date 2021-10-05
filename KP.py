# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 21:18:45 2020

@author: Loba
"""
import numpy as np

class Knapsack:
        
    sac = np.zeros(0)
    
    resultat = 0
    
    def __init__(self, nb_objets):
        self.sac = np.zeros(nb_objets)
    
    '''Fonction qui initialise le problème du sac a dos'''
    def bb(self, T, capacite_max):
        ''' Initialisation '''
        
        # initialisation de le borne inferieur avec l'heuristique gloutonne
        borne_inf = self.init_borne_inf(T, capacite_max)
        self.resultat = borne_inf
        # Array de la meme taille que le sac, si un element vaut 1 alors il est imposé 
        objets_impose = np.zeros(len(T[0]))
        # Array representant le sac
        sac = np.zeros(len(T[0])).astype(np.float)
        #poids du sac
        poids_sac = 0.
        #utilite du sac
        utilite_sac = 0.
        # variable qui sert a imposer la mise a un ou a zero du prochain objet
        nb_iter = 0
        
        result_init = self.init_sac(T, capacite_max, sac)
    
        # initialisation de la borne sup
        borne_sup = result_init[0]
        # index de l'objet partitionné pour etre ajouté au sac
        id_modif = result_init[1]
        
        objets_impose[id_modif] = 1
        
        # si notre borne sup est inferieur a la borne inf inutile de continuer
        if(borne_inf >= borne_sup):
            #print('Borne inferieur (', borne_inf, ') > Borne Superieur (', borne_sup, ')')
            return 
        # Notre première brone sup est notre solution continue
        solution_continue = borne_sup
        
        if (solution_continue - int(solution_continue) == 0):
            #1print('La solution optimale en variable continues est entière :',solution_continue)
            return 
        
        #print('La borne inferieure est:',borne_inf)
        print("The optimal utility in continious variables is:", solution_continue)
        # la solution optimal est pour commencer l'arrondis entier de notre solution continue
        self.resultat = int(borne_sup)
        
        """ fin de l'init"""
        
        # on impose à zero l'objet ajouté en partie
        sac[id_modif] = 0 
        # on rentre dans la première branche
        self.calcul_branche(T, sac, borne_inf, borne_sup, poids_sac, utilite_sac, capacite_max, nb_iter, self.resultat, objets_impose)
        
        # on impose a 1 l'objet ajouté en partie
        sac[id_modif] = 1 
        utilite_sac += T[1][id_modif]
        poids_sac += T[0][id_modif]
        #on rentre dans la seconde branche
        self.calcul_branche(T, sac, borne_inf, borne_sup, poids_sac, utilite_sac, capacite_max, nb_iter, self.resultat, objets_impose)
        
        return
    
    '''init : calcule de la borne inferieure (utilité) grâce à une heuristique gloutonne'''
    def init_borne_inf(self, T, capacite_max):#T est un tableau :[[poids],[utilité]]
        sac = self.sac #np.zeros(len(T[0]))
        poids_sac, utilite_sac, utilite_max, id_utilite_max, i = [0,0,0,0,0]
        
        while (i < len(T[0])):
            
            # on cherche l'utilité max 
            for j in range (len(T[1])):
                
                # on cherche l'objet le plus utile qui n'est pas encore dans le sac
                if (T[1][j] > utilite_max and sac[j] == 0):
                    utilite_max = T[1][j]
                    id_utilite_max = j
            
            if (poids_sac + T[0][id_utilite_max] <= capacite_max):# si le poids actuel du sac plus le poids de l'objet d'utilité max <= a la capacité max du sac...
                
                sac[id_utilite_max] = 1 #on ajoute l'objet au sac
                poids_sac += T[0][id_utilite_max]# on augmente le poids du sac 
                utilite_sac += utilite_max# on augmente l'utilité du sac
                
            else:# si l'objet le plus utile est trop lourd, alors on le note à -1 dans le sac
                sac[id_utilite_max] =- 1
            
            i += 1
            utilite_max = 0
            id_utilite_max = 0
        #on remet tous les -1 a 0
        for k in range(len(sac)):
            if (sac[k]==-1):
                sac[k] = 0
        # print('Solution initial (gloubonne):', sac)
        return utilite_sac
        
    
    
        # ceci est la premiere iteration --> trouver la premiere borne sup en valeur continue
    def init_sac(self, T, capacite_max, sac):
        
        # Array de la meme taille que le sac, si un element vaut 1 alors il est imposé 
        objets_impose = np.zeros(len(T[0]))
        #poids temoraire du sac
        poids_temp = 0.
        #utilité temporaire du sac
        utilite_sac_temp = 0.
        # index de l'objet partitionné pour etre ajouté au sac
        id_modif = 0 
        
        # ceci est la permiere itartion --> touver la premiere borne sup en valeur continue
        
        # on ajoute autant d'éléments que possible jusqu'a ce que le sac soit plein
        for j in range (len(T[0])):
            
            # si l'objet n'est pas dans le sac j'essai de le mettre 
            if (sac[j] ==.0 and capacite_max >= T[0][j] + poids_temp):
                poids_temp += T[0][j]
                utilite_sac_temp += T[1][j]
                
            # si je ne peux pas, alors je le met en partie
            elif (sac[j] == .0 and capacite_max < T[0][j] + poids_temp):
                # j'ai ajouté beaucoup de "float(..)" pour eviter les arrondis ... cela reste inéficace dans certains cas  
                utilite_sac_temp += ((float(float(capacite_max) - float(poids_temp))/float(T[0][j])*float(T[1][j])))
                # on récupere l'indice de l'objet a imposé
                id_modif = j
                # on impose l'objet
                objets_impose[id_modif] = 1
                break
            
        return utilite_sac_temp, id_modif
        
    '''Fonction qui calcule les noeuds fils et qui fait le Branch and Band'''
    def calcul_branche(self, T, sac, borne_inf, borne_sup, poids_sac, utilite_sac, capacite_max, nb_iter, resultat, objets_impose):# fonction récursive qui fait la relaxation continue
      

        '''initialisation des variables locales'''
        
        #repésente l'utilité que l'on va calculer dans cette branche
        utilite_temp = 0
        
        #repésente le poids que l'on va calculer dans cette branche
        poids_temp = 0
        
        #sert a récuperer l'indice de l'objet ajouté en partie
        id_modif = 0
    
        #on incrémente le nombre d'iteration 
        nb_iter+=1 
        
        #copie de notre sac sur laquelle nous allons travailler
        sac_temp = np.copy(sac)
        ''' verifications préliminaires '''
        
        # si le nombre d'iterations est superieur à la taille du sac, cela veut dire qu'on a déja parcouru toutes les combinaisons possibles.
        if (nb_iter>len(sac)):
    
             self.update_resultat(min(resultat, self.resultat))
             
             return
        
        ''' On ajoute les objets dans le sac en fonction du rapport utilité/ poids jusqu'a ne plus avoir de place '''
        
        # on prend en compte les éléments déja présents dans le sac (ceux où on a imposé le 1 pas besoin de prendre encompte les autres)
        for i in range(len(T[0])):
            
            if (sac[i]==1):
                poids_temp+=T[0][i]
                utilite_temp+=T[1][i]
        
        resultat_add = self.add_objets(sac_temp, T, objets_impose, capacite_max, poids_temp, utilite_temp, nb_iter)
        utilite_temp = resultat_add[0]
        objets_impose = resultat_add[1]
        id_modif = resultat_add[2]
        sac_temp = resultat_add[3]
        
        '''Branch and Band'''
        
        # on s'arrete si on tombe sur un resultat entier
        if(utilite_temp - int(utilite_temp) == 0):
            
            if(utilite_temp >= borne_inf ):
                
                self.update_resultat(min(utilite_temp, self.resultat))
                
                return 
            else:
            
                return 
        
                
        # si l'utilité que l'on vient de calculer est comprise entre la borne sur et la borne inf alors on actualise la borne sup
        if (utilite_temp<borne_sup and utilite_temp>=borne_inf) :
            
            # mise a jour de la borne sup
            borne_sup = utilite_temp
            
            # le resultat final est le minimum est bornes sup calculés
            resultat = min(resultat, borne_sup)
            
            # le resultat final est le minimum est bornes sup calculés
            self.update_resultat(min(resultat, self.resultat))
            
            self.next_iter(T, sac ,utilite_sac, poids_sac,capacite_max, id_modif, borne_inf, borne_sup, objets_impose, nb_iter, resultat)
           
        #si l'utilité calculé est superieure a la borne sup, alors on fait une recursion sans mettre a jour la borne sup
        elif(utilite_temp>=borne_sup):
           
            self.next_iter(T, sac ,utilite_sac, poids_sac,capacite_max, id_modif, borne_inf, borne_sup, objets_impose, nb_iter, resultat)
    
        #Sinon, on s'arrête car l'utilité est inferieure a la borne inf
        else:
            return
        
    def update_resultat(self, value):
        self.resultat = value
        
    def next_iter(self, T, sac , utilite_sac, poids_sac, capacite_max, id_modif, borne_inf, borne_sup, objets_impose, nb_iter, resultat):
        
        # on impose l'objet qui a été fractionné à 1
            sac[id_modif] = 1 
            utilite_sac +=T [1][id_modif]
            poids_sac += T[0][id_modif]
            #print(Bag)
            
            #si le poids du sac est inferieur a la capacité max, on rentre dans une nouvelle branche avec l'objet imposé a 1
            if (capacite_max>poids_sac):
                #print(Bag)
                self.calcul_branche(T, sac, borne_inf, borne_sup, poids_sac, utilite_sac, capacite_max, nb_iter, resultat, objets_impose)
                
            
            # on impose l'objet qui a été fractionné à 1
            sac[id_modif] = 0
            utilite_sac -= T[1][id_modif]
            poids_sac -= T[0][id_modif]
            #print(Bag)
            #on rentre dans une nouvelle branche
            self.calcul_branche(T, sac, borne_inf, borne_sup, poids_sac, utilite_sac, capacite_max, nb_iter, resultat, objets_impose)
        
    def add_objets(self, sac, T, objets_impose, capacite_max, poids_temp, utilite_temp, nb_iter):
        
        l = nb_iter
        # on cherche maintenant à ajouter les objets qui ne sont pas imposés
        while (l<len(sac)):
            id_modif = 0
            id_max = self.find_max(sac, T, objets_impose)
            
            #on incrémente le compteur
            
            l+=1
            
            #si on peut ajouter l'objet qui as le ratio max, on le fait
            if (capacite_max >= T[0][id_max] + poids_temp):
                
                poids_temp+=T[0][id_max]
                utilite_temp+=T[1][id_max]
                sac[id_max]=1
                
            # si je ne peux pas, alors je le met en partie
            elif (capacite_max<=T[0][id_max]+poids_temp ):
                
                    sac[id_max] = (capacite_max-poids_temp)/T[0][id_max]
                    
                    utilite_temp += sac[id_max]*T[1][id_max]
                    poids_temp += sac[id_max]*T[0][id_max]
                    
                    # on recupere l'indice de notre objet
                    id_modif = id_max
                    #on ajoute notre objet aux objets imposés
                    objets_impose[id_modif]=1
                    break
        return utilite_temp, objets_impose, id_modif, sac
    
    def find_max(self, sac, T, objets_impose):
        max = 0
        id_max = 0
        
        for k in range(len(T[0])):
                
                # Si un element est imposé, je ne l'ajoute pas.
                if(objets_impose[k]==1):
                    
                    break
                
                # on recherche le ratio max des objets qui ne sont ni imposés ni dans le sac
                if (T[1][k]/T[0][k] > max and sac[k] != 1):
                    
                    max = T[1][k]/T[0][k]
                    id_max=k
        return id_max
    
def main():
    print('\nKnapsack: We want to maximize the bag utility')
    print('\nPLEASE INPUT INTERGERS')
    capacite_max = int(input('What is your bag capability?'))
        
    nb_objets = int(input("How many object do you have?"))
        
    kp = Knapsack(nb_objets)
        
    Tab = np.zeros((2,int(nb_objets)))#T est un tableau :dim1=poids,dim2= utilité
        
    for i in range(len(Tab[0])):#range(len(Tab[0])):
        print("Please enter the weight of object n°",i)
        Tab[0][i] = int(input())
        print("Please enter the utility of object n°",i)
        Tab[1][i] = int(input())
            
    print('The weight of your objects are: ', Tab[0][:])
    print('The utilities of your objects are: ', Tab[1][:],'\n')
    print('---------------------------------\n')
        
    kp.bb(Tab, capacite_max)
        
    print('The optimal utility  is:', (kp.resultat))
    print('The final bag is: ', kp.sac)

main()
    
    
    
    
    