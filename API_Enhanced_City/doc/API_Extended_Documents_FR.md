# Introduction : 
L’API Extended Document est une API reliée à une base de données permettant le stockage de documents et de leurs données (ex : métadonnées, données de visualisation, …).

L’API permet aussi de récupérer de différentes manières les informations stockées sous le format JSON.
Les données sont stockées dans une base donnée postgreSQL. Cependant, nous n’aurons (normalement) jamais besoin d’aller modifier le schéma de données à la main dans la base de données.

Une table en base de données est un ensemble de champs qui permettrons de stocker nos données.
Les tables peuvent être reliées entre elles en créant des associations. Ces associations peuvent êtres uniques, multiples.
Une table possède des attributs / champs qui représentent les données. Chaque champ possède un type et peut être obligatoire ou non. On peut aussi lui assigner une valeur par défaut.

Dans le modèle d’origine, un document possède une table de métadonnée et une table de visualisation. La relations entre la table document et la table de visualisation ainsi que celle de métadonnée est une relation « OneToOne », c’est-à-dire qu’un document possède une table de visualisation, un document possède une table de métadonnées.

![Class diagram for the Extended Document API](./Pictures/ClassDiagramAPIExtendedDocument.png)

L’API Extended Document est un projet Symfony. Les projets Symfony ont une structure basée sur le design pattern MVC (Modèle, Vue, Contrôleur). Le modèle est la partie qui définit les données, dans Symfony un modèle est composé d’entité, chaque entité est décrite par une classe PHP. Ici, chaque entité représentera une table en base de données. 

Le contrôleur va être la partie qui va manipuler les données, c’est une classe PHP dans Symfony. La vue est la partie affichage, dans Symfony on utilise Twig afin de créer des « templates » de page html. Dans l’API Extended Document la vue ne nous intéresse pas car elle ne renvoie pas de page HTML mais juste des codes d’erreur, de succès ou du JSON. 

Ce document va détailler comment modifier le projet afin de modifier le modèle de données. Juste modifier les entités n’est pas toujours suffisant car le fonctionnement du contrôleur dépend aussi du modèle de donnés dans certains cas (Exemple : getDocuments par date avec les différents types de dates).

# Installation : 
- Installer le serveur web :

Pour tester les modifications il est possible d’utiliser le serveur web RICT en modifiant directement les fichiers sources sur le serveur.

Cependant si l’on veut effectuer des tests en local avant de déployer le projet sur le serveur, il est nécessaire d’installer un serveur web sur sa machine.

Un serveur web est en général composé d’un serveur Apache, un interpréteur PHP et une base de données. Des logiciels proposent la mise en place rapide de ces composants : WAMP (Windows Apache MySQL PHP) pour Windows, LAMP pour Linux, MAMP pour Macintosh … 

Il est aussi possible d’installer tous les composants séparément mais cela requiert plus de configuration.

- Récupérer le repository git et le placer dans le bon répertoire : 

````
git clone https://github.com/JorisMillot/APIExtendedDocument.git
````
Si vous utiliser WAMP ou un logiciel du même type, il devrait y avoir un dossier nommé « www » dans le répertoire où vous avez installé WAMP (ou son équivalent). Placer le repository git dans ce répertoire « www ».

Le répertoire « www » est en fait la racine de notre serveur web. On peut accéder aux fichiers s’y trouvant en ouvrant un navigateur et en tapant « localhost/{chemin du fichier} » dans l’url.

Si vous n’utilisez pas WAMP ou de logiciel du genre il sera nécessaire de configurer Apache pour mettre en place un routage de l’utilisateur vers un répertoire où se trouverons les fichiers de notre serveur web.

Pour accéder aux routes de notre projet Symfony on utilise l'URL suivante (le chemin peut varier si vous avez placé le repository git dans un sous dossier) :

Pour le développement :
````
http://localhost/APIExtendedDocument/web/app_dev.php/{route}
````

Pour la production :
````
http://localhost/APIExtendedDocument/web/{route}
````

- Installer php:

Pour vérifier si php est installé et quelle version vous possédez, lancez:

````
php -v
````
Si php n'est pas installé, faites:

````
 apt-get install php5-common libapache2-mod-php5 php5-cli
````
- Installer composer:

Depuis var/www/html/APIVilo3D/APIExtendedDocument faire :

````
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php -r "if (hash_file('SHA384', 'composer-setup.php') === '544e09ee996cdf60ece3804abc52599c22b1f40f4323403c44d44fdfdd586475ca9813a858088ffbc1f233e9b180f061') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
php composer-setup.php
php -r "unlink('composer-setup.php');"
composer require apache-pack
````

- Installer postgreSQL:

Note : attention, sur la deuxième ligne, remplacer X.X par la bonne version de php:

````
apt-get install postgresql postgresql-client
apt-get install phpX.X-pgsql
su - postgres
psql
\q
````
- Configurer l'accès à la base de données:

Il faut ouvrir le fichierapp/config/parameters.yml et mettre les bonnes valeurs aux lignes commençant par 'database_': serveur, nom de la base, nom d'utilisateur et mot de passe. 

Par exemple:
````
   parameters:
    database_host: 127.0.0.1 (if you want to use localhost)
    database_port: 5432
    database_name: your_db_name
    database_user: postgres
    database_password: root
    mailer_transport: smtp
    mailer_host: 127.0.0.1
    mailer_user: null
    mailer_password: null
    secret: ThisTokenIsNotSoSecretChangeIt
````

La commande suivante va générer la base de données:
````
php bin/console doctrine:database:create
````

Vous obtiendrez:

"Created database "<your_db_name>" for connection named default" à l'exécution de php bin/console doctrine:database:create

Mettre à jour la base de données:

```` 
php bin/console doctrine:schema:update --force
````

Vérifications:


Ouvrez votre navigateur et lancez l'url suivante:
{path_to_your_project}/APIExtendedDocument/web/app_dev.php/displayDocuments

Vous devriez avoir:

![](./Pictures/DBtable.png)

- Autorisations:

Il faut autoriser l'écriture de fichiers dans le repertoire 'documetnsDirectory':

````
HTTPDUSER=$(ps axo user,comm | grep -E '[a]pache|[h]ttpd|[_]www|[w]ww-data|[n]ginx' | grep -v root | head -1 | cut -d\  -f1)
sudo setfacl -dR -m u:"$HTTPDUSER":rwX -m u:$(whoami):rwX var
sudo setfacl -R -m u:"$HTTPDUSER":rwX -m u:$(whoami):rwX var
sudo setfacl -dR -m u:"$HTTPDUSER":rwX -m u:$(whoami):rwX web/documentsDirectory
sudo setfacl -R -m u:"$HTTPDUSER":rwX -m u:$(whoami):rwX web/documentsDirectory 
````

# Structure du projet : 
Les modèles de données sont stockés dans : …/APIExtendedDocument/src/ExtendedDocument/APIBundle/Entity

Le contrôleur est dans : …/APIExtendedDocument/src/ExtendedDocument/APIBundle/Controller

Ce contrôleur est associé à un fichier de routage qui va permettre de savoir vers quelle méthode rediriger les requêtes utilisateurs. Le fichier de routage de trouve dans …/APIExtendedDocument/src/ExtendedDocument/APIBundle/Ressources/config/routing.yml

Par exemple si j’entre l’url /getDocument/1 que va faire le serveur ?
L’image ci-dessous indique que lors de la réception d’une requête de la forme /getDocument/{idDocument} il va faire appel à la méthode getDocument du controlleur.

![](./Pictures/api1bis.png)

Le paramètre idDocument sera transmis à la methode du controlleur.

Note : lors de l’ajout d’une méthode dans le controlleur, le mot clé « Action » doit être ajouté à la fin du nom de la méthode.

![](./Pictures/api2bis.png)

# Modifier le modèle de donnée :
## Rajouter une table (entité) : 
1. Se placer dans le répertoire du projet avec un invite de commande.

![](./Pictures/api3.png)

2. Exécuter la commande 
````
php bin/console doctrine:generate:entity
````

![](./Pictures/api4.png)

3. Entrer le nom de l’entité de la manière suivante : {Nom Projet}{Nom Bundle} :{Nom Entité}

Par exemple : ExtendedDocumentAPIBundle:maTable (ExtendedDocument est le nom du projet et APIBundle le bundle dans lequel se trouvent les entités).

![](./Pictures/api5.png)

4. Choisissez « annotation » comme format de mapping. (Entrée sans saisie permet de valider le choix par défaut qui ici est « annotation »).

![](./Pictures/api6.png)

5. Ajouter des champs. Entrée sans saisie mettra fin à l’ajout de champs. Il sera possible plus tard d’ajouter, modifier et supprimer des champs

a. Saisissez le nom du champ.

b. Saisir le type du champ.

c. Saisir si le champ peut être vide ou non (true = peut être vide).

d. Saisir si le champ doit être unique ou non (true = doit être unique).

![](./Pictures/api7.png)

Note : il n’est pas nécessaire d’ajouter un champ « id » à la classe car il sera ajouté tout seul par l’ORM.

6. A la fin de l’ajout de champ, si tout ce passe bien vous avez quelque chose ressemblant à ça :

![](./Pictures/api8.png)

## Ajouter / modifier des champs :

1. Se placer dans la classe de l’entité à modifier : APIExtendedDocument/src/ExtendedDocument/APIBundle/Entity/{Entité à modifier}

![](./Pictures/api9bis.png)
 
2. Rajouter la variable correspondant au champ à ajouter : (une variable en php s’écrit avec un $ devant le nom de la variable. On ne type pas nos variables en php. On se doit de rajouter le mot clé private ici pour définit le niveau d’accès à la variable car elle se trouve dans une classe php.)  

![](./Pictures/api10.png)

3. Rajouter les annotations pour définir la variable au niveau de la base de données. Les annotations vont permettre à l’ORM (Object-Relational Mapping) de savoir comment faire le lien entre les entité php et les tables en base de données.

![](./Pictures/api11.png)

Types disponibles : 
https://www.doctrine-project.org/projects/doctrine-dbal/en/2.7/reference/types.html

4. Ajouter les accesseurs/mutateurs : 

a. Se placer dans le répertoire du projet avec un invite de commande.

b. Exécuter la commande afin de générer l’entité modifiée :
````
php bin/console doctrine:generate:entities {Projet}{Bundle}:{Entité}
````

![](./Pictures/api12bis.png)

Note : Cette commande permet d’ajouter dans l’entité les méthodes afin d’accéder aux variables que l’on à définit précédemment. Cependant, elle ne supprime pas les méthodes des champs que l’on a supprimé, il faudra le faire manuellement.

Exemple de méthode d’accès et de modification générée dans Metadata : 

![](./Pictures/api12.png)

Mettre à jour les migrations :

C’est l’étape finale, celle où l’on met à jour la base de données. Il faut donc que le projet se trouve sur le même serveur que la base de données à mettre à jour.
Note : Si c’est la première mise à jour des données il faut créer la base de données :
````
php bin/console doctrine:database:create
````

Note : La configuration de la base de données se trouve dans le fichier « APIExtendedDocument/app/config/parameters.yml ». Pour des raisons de sécurité évidentes, ce fichier ne doit JAMAIS être partagé sur un git public. Il est normalement créé à l’installation de composer. S’il n’existe pas il faut le rajouter :
````
parameters:
    database_host: adresse de la base de données (Le plus souvent c’est le serveur lui-même : 127.0.0.1)
    database_port: port de la base de données 
    database_name: nom de la base de données
    database_user: utilisateur base de données
    database_password: mot de passe base de données
````

c. Se placer dans le répertoire du projet avec un invite de commande.

d. Mettre à jour la base de données avec la commande :
````
php bin/console doctrine:schema:update--force
````
Note importante : Si cela est nécessaire, la base de données va supprimer des entrées de la base de données.

## Lier des tables : 

Il existe différents types de liaisons de tables en fonction des cardinalités que l’on souhaite avoir, par exemple :
 
OneToMany / ManyToOne : Une entité est associée à plusieurs entités

OneToOne : Une entité est associée à une seule autre entité.

ManyToMany : Plusieurs entités sont associées à plusieurs autres entités.

Pour plus d’informations sur les associations : 

https://www.doctrine-project.org/projects/doctrine-orm/en/2.6/reference/association-mapping.html

Exemple d’ajout d’association : Un document possède une visualisation 

Dans la classe Visualization : 

On rajoute dans les annotations une association OneToOne.

targetEntity : nom de l’entité cible de l’association.

mappedBy : nom de la colonne primaire de l’entité cible.

![](./Pictures/api13.png)

Dans la classe Document : 

On rajoute dans les annotations une association OneToOne.

targetEntity : nom de l’entité cible de l’association.

invesedBy : la variable qui va contiendra le document dans l’entité Visualization. 

Note : « fetch =  « EAGER » » permet de récupérer les entités en cascade.

![](./Pictures/api14.png)

## Implémentation de l’interface JsonSerializable :

Afin de renvoyer les données sous le format Json, il est nécessaire pour chaque entité d’implémenter l’interface JsonSerializable.

![](./Pictures/api15.png)

Il faudra ensuite implémenter la méthode jsonSerialize(). 

Cette méthode retourne un tableau clé valeur qui sera converti au format JSON.

Par exemple celle de Document :
````
public function jsonSerialize()
{
return [
   'idDocument'=>$this->getId(),
   'metadata'=>$this=>getMetadata()->jsonSerialize(),
   'visualization'=>$this->getVisualization()->jsonSerialize()
   ];
}
````
## Implémentation de l’interface DoctrineEntity :

Cette interface permet d’instancier et modifier des entités sans avoir à modifier la méthode à chaque fois que l’on modifie le modèle. Cependant, les méthodes de l’interface doivent êtres implémentés dans chaque entité lors de leurs créations.

Méthode initEntity : (Cas général à adapter en fonction de l’entité)
````
public function initEntity($request, $controller){
   if($request==null)
     return 'Error:request wasn\'t provided';
   $metadata=$controller->getManager()->getClassdMetadata('ExtendedDocument\APIBundleEntity\{Nom_de_lentite});
   foreach($metadata->getFieldNames() as $key=>$filedName){
   //if the field is required but not provided, return error 400: Bad Request
   if($filedName!='id'&& !$metadata->isNullable($filedName) && $request->get($fieldName,null)==null){
      return 'Error: some parameters are missing: '.$filedName;
   }
   if($fieldName != 'id'){
       $methodSet='set'.ucfirst($fieldName);
       $this->$methodSet($request->get($fieldName,null));
    }
  }
  return 1;
}
````

Attention : il est difficile de rendre le code totalement générique (par exemple avec le cas spécial de Metadata qui nécessite l’upload d’un fichier sur le serveur). Dans ce cas là il faut adapter le code des méthodes (voir les implémentations dans Document et initEntity de Metadata).

Méthode editEntity (Cas général à adapter en fonction de l’entité) :
````
public function editEntity($request, $controller)
{
   $metadata = $controller->getManager()->getClassMetadata('ExtendedDocument\APIBundle\Entity\{Nom de l’entité}');
   foreach ($metadata->getFieldNames() as $key => $fieldName){
      if($fieldName != 'id'){
         $methodSet = 'set'.ucfirst($fieldName); //contains the name of the method to call for each field
         $this->$methodSet($request->get($fieldName,null));
      }
   }
}
````

