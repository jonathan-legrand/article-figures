#### AVANT PROPOS #####

# Ceci est un exemple de script que vous pouvez réutiliser/modifier à loisir au
# fil des séances, en faisant File>Save as et en nommant le fichier .R à votre
# convenance.

# Toute ligne commençant par # n'est pas interprétée par R et vous permet donc
# de mettre autant de commentaires qui vous aideront à garder des traces de ce
# que vous faites.

# Dans R, il est possible d'écrire chaque instruction sur plusieurs lignes pour
# plus de lisibilité. Si la ligne se termine par une virugle, R sait qu'il doit
# passer à la suivante pour la suite de l'instruction.

# C'est maintenant à vous d'adapter la suite des instructions pour faire les
# exercices...


#### IMPORTER LES DONNEES #####

# Garder une trace de l'importation dans votre script, en utilisant la fonction
# read.delim:

exoX <- read.delim(file = "fichier.txt", # dans quel fichier sont les données
                   sep = "\t", # quel est le séparateur des colonnes (\t=tabulation)
                   stringsAsFactors = T) # Transforme les colonnes contenant des caractères en VI (factor)



#### VERIFIER LES DONNEES #####

# Chaque instruction nécessite d'indiquer où se trouvent les données sur lesquelles
# on travaille. Cela se fait en donnant le nom de l'objet et la colonne où est
# l'information sur laquelle on veut travailler: exoX$Nom_de_colonne

table(exoX$VI)  #donne le nombre de mesures pour la VI (remplacez "exoX" et "VI"
                #par ce qui vous intéresse dans votre cas )

# Faire un boxplot des valeurs de la VD
# Permet de regarder la distribution des données
boxplot(VD)

# Séparer les boxplot en fonction des modalités de notre VI
# Faites le pour afficher les valeurs de TR en fonction de la drogue
boxplot(VD~VI)

# calculez la moyenne de la VD avec la fonction "mean"

# Vous pouvez utiliser cette notation avec le tilde dans "aggregate" qui
# permettra d'utiliser une fonction ("mean" pour nous) pour différents groupes.
# pour connaitre les moyennes par modalité de votre VI
moyennes<-aggregate(VD~VI, data=exoX, mean)# on crée un vecteur avec les moyennes et stocke le résultat dans moyennes


#### FAIRE UN HISTOGRAMME DES DONNEES #####


#On charge une library qui permet de faire des pirateplots
library(yarrr)#si cette library n'est pas présente, l'installer: install.packages("yarrr")
pirateplot(data=exoX, #on indique sur quel objet de données on travaille
           VD~VI,  #~veut dire en fonction: on demande à regarder la VD en fonction de la VI
           point.o = 1, #on lui dit de représenter les données individuelles par un point opaque
           main="Rédigez le titre", # main: permet d'ajouter un titre au graphique
           xlab="qu'est-ce qui est en abcisse", # xlab: ajoute un titre pour l'axe des X
           ylab="qu'est-ce qui est en ordonnée (avec l'unité)", # ylab: ajoute un titre pour l'axe des Y
           sortx="mean") # sortx permet de déterminer l'ordre de tri sur l'axe des x (ici, par moyenne ascendante)


############# VERIFICATION DES CONDITIONS D'APPLICATION DE L'ANOVA

library(stats) # ce package contient des tests dont on a besoin (comme le shapiro ou le Tukey)

# Shapiro.test(VD) fait un test de normalité sur la variable

# la fonction "by" (par en anglais) qui va permettre d'éxécuter une instruction en fonction d'un critère: *
# by(ce sur quoi on veut appliquer la fonction, le critère, la fonction)
# Combinez cette fonction avec shapiro.test pour obtenir un test de shapiro pour chacun de vos groupes experimentaux et stockez le résultat dans "shap"

shap<-by(...) # on stocke le résultat du test pour pouvoir le rappeler au besoin plus tard
print(shap) # Afficher le contenu de shap dans la console

library("car") # ce package contient le test de Levène dont on a besoin pour tester l'homogénéité des variances

lev<-leveneTest(VD, VI) #test de Levène pour l'homogénétié des variances des TR entre drogues
print(lev) # afficher le résultat


############## CALCUL DE L'ANOVA

library(ez) #chargement du package ezANOVA

#Calcul:
anova3<-ezANOVA(data= nom_objet ,dv=VD, wid=sujet , within = VIintra, between= VIinter, type=3, return_aov=T) # on stocke le résultat dans un objet anova3
# type=3 s'assure que le calcul est fait comme vous l'avez appris à la main
# return_aov=T crée un objet aov (= analysis of variance) sur lequel d'autres fonctions bien pratiques s'appuient

#affichage du tableau d'ANOVA:
summary(anova3$aov)

# Si on explore l'objet anova3, on peut voir qu'il y a un test de Levène qui a été fait automatiquement par ezANOVA:
anova3$Levene #Pas besoin de le faire à part, donc.

#On a aussi toutes les infos concernant l'ANOVA (y compris le éta carré) stocké dans ges
anova3$ANOVA


