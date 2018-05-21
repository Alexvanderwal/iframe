# Iframe

## Wat is Django?
Django is een 'high-level' python web-framework, ontworpen om snelle ontwikkeling d.m.v een pragmatisch ontwerp aan te moedigen.
Zoals bij de meeste frameworks is hier het doel om ontwikkelaars de mogelijkheid te geven om zich te focusen op de nieuwe en unieke delen van hun project. Dit wordt behaald door veel van de lastige en vervelende aspecten van web-design uit handen te nemen, zonder dat deze aspecten niet aangepast kunnen worden.

Net zoals de meeste webframeworks, volgt django het MVC pattroon nauw, maar gebruikt wel hun eigen logica in de implementatie. Omdat django veelal wordt gebruikt met Models, Templates & Views wordt het dan ook een MTV framework genoemt:

* M (Models) - De data access laag. Deze laag bevat alles over de data, hoe het aangeroepen moet worden, hoe het gevalideert moet worden, welk gedrag het heeft en welke relaties het heeft. Hier valt dus ook het uitgeschrijven naar een persistent datalaag onder.

* T (Template) - De presentatie laag. Deze laag bevat presentatie logica, hoe iets gepresenteert moet worden op een webpagina.

* V (View) - De business logica laag. Deze laag bevat de logica welke de modellen aanroept en deze data verwijst naar de juiste template. 

## Veiligheid
Django streeft ervoor om 'out of the box' veiligheids maatregelen aan te bieden, bijvoorbeeld voor:
* SQL Injectie.  De formulieren worden automatisch gecontroleerd of de input wel correct is en vervolgens gecleaned (waardoor SQL queries worden verwijderd)
* Clickjacking. D.M.V een [middleware](https://docs.djangoproject.com/en/2.0/ref/middleware/#django.middleware.clickjacking.XFrameOptionsMiddleware) geeft django de X-Frame header mee welke site rendering in een frame tegen gaat.
* SSL/HTTPs forcering
* Host header - Accepteert alleen maar requests van betrouwbare hosts  
Django is vaak 1 van de eerste frameworks om te reageren op een nieuwe gevonden kwetsbaarheid. 

In het volgende [artikel](https://www.contextis.com/blog/make-a-django-app-insecure-its-not-easy-and-thats-a-good-thing) wordt er gefocust op het onveilig maken van Django, wat vrij moeilijk leek te zijn.


## Waarom Django?
### Tijds getest
Django bestaat (vanaf 2018) 13 jaar, wat een erg lange tijd is voor een project, laat staan voor 1 welke nog zoveel gebruikt wordt. Dit betekend ook dat er al veel tutorials & blogs zijn geschreven over complexere use cases in django.

### Schaalbaarheid & combineerbaarheid
Over de jaren heen hebben verschillende groten projecten zoals [disqus](https://stackshare.io/disqus/disqus
), [instagram](https://stackshare.io/instagram/instagram) en [pinterest]() Django in hun technologie stack gebruikt. Dit brengt als bonus met zich mee dat er door zulke partijen veel middleware (en of dergelijke pakketen) ontwikkelt zijn voor de intergratie met andere frameworks. 

### Het ecosysteem
Zoals de Python gemeenschap in het algemeen, voegt de Django gemeenschap veel utilities & pakketten toe aan PyPI (python package manager) voor gratis gebruik. Ook merk ik dat de gemeenschap van Django veel vriendelijker is op plaatsen zoals IRC, dan andere gemeenschappen (Node bijvoorbeeld). Dit is mede mogelijk door DSF (Django Software Foundation), welke duidelijk aangeven wat voor'n gemeenschap zijn ogen te zijn. Hierdoor zie je veel gemeenschappen zoals [Django Girls](https://djangogirls.org/). Ook zie ik veel begrip vanuit de gemeenschap voor nieuwe Django ontwikkelaars.  

# Oefeningen vanuit de Udemy course
Omdat de Udemy course meer gericht is op het conceptuele achter django functies etc dan op een daadwerkelijke project en de context. Om deze reden hebben ik besloten de geleerde concepten in een `cookbook` over te nemen, waar per concept het ideologie staat uitgelegt. 

# iframe
A Full-fledged forum build upon the Django framework.
![Image](http://puu.sh/A3Bbn/614b5ccc92.png) 

## Introduction
The forum features a category based system. In these categories users can create threads and
comment on newly start threads by users. There is also the possiblity 
to interact with the profiles of other users, aswell of using administrative rights
if those have been granted to the user.

## Requirements
[`Python`](https://www.python.org/),  v3.4+ since these have pip by default   
`Pip` v1.8+  
[`Virtualenv`](https://virtualenv.pypa.io/en/stable/)   
Unix subsystems:  ```Pip install virtualenv```   
Windows : ```py -m pip install virtualenv```

## Getting started (manually)
### Unix subsystems
1. ```virtualenv venv``` in the main folder
2. ```source venv/bin/activate```
3. ```pip install -r requirements.txt```   
Now you can start the app 

### Windows
1. ```py -m virtualenv venv``` in the main folder
2. ```call venv/Scripts/activate``` 
3. ```pip install -r requirements.txt```   
Now you can start the app 
### Starting the app
It's recommended you always do ``python src/manage.py migrate`` to ensure your
database reflects all changes in the migrations before
starting the server by ```python src/manage.py runserver```

Once you have started the server, you can visit the forum on localhost:8000
## Features

### Current Features

* User accounts w/ user profiles
* A navigatable history of the user his activity on the server
* The ability to create posts with a WYSIWYG editor
* The ability to edit posts
* Persistent data storage

### Wanted features

- [ ] A revamp of the user interface. This because right now the UI is created using the
css framework [bootstrap v4](https://getbootstrap.com/docs/4.1/getting-started/introduction/). However, it lacks
UX, the usage of various design patterns
& a style that shows my personality ( I want to do this for my minor's course [webdesign](https://github.com/cmda-minor-web/web-design)
- [ ] The usage of [NodeJS](https://nodejs.org/en/) & [socket.io](https://socket.io/) to give real-time feedback to the user.
This should increase the user feedback by a huge margin, and will also be very interesting to
see how the intergration between 2 backends work. Hopefully this will also improve my knowledge about the difference between 
node & django

#### Argumentation NodeJS intergration
First of all, i'm taking inspiration of Pinterest & Instagram, who both use NodeJS in combination with Django
in their backend. There is also a basic [tutorial](http://www.cuelogic.com/blog/how-to-use-both-django-nodejs-as-backend-for-your-application/)
about it, together with multiple [helpful](https://stackoverflow.com/questions/35056302/implementing-django-and-socket-io-to-work-together)
resources. 

I feel that doing something architectural like this could be a huge asset for me in terms of knowledge about NodeJS,
aswell as how it can be used in combination with other Backends, and how the realtime aspect can be leveraged
even with these technologies. 

The implementation also seems quite plausible as I've already exposed various API points,
from which I can fetch data, and possibly can leverage to make the dispatching and receiving messages from Socket.io
a reality. 

This will be without a doubt a difficult project, but seeing as it will most likely be able to keep me busy for 2 weeks,
and will test my knowledge further. 



### Web Sockets
https://channels.readthedocs.io/en/latest/installation.html
Weaves Asynch code within the Django synchronous core. Replaces the webserver so you'll be able to server; webkSockets along side http


