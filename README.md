# iframe
A Full-fledged forum build upon the Django framework. 

## Introduction
The forum features a category based system. In these categories users can create threads and
comment on newly start threads by users. There is also the possiblity 
to interact with the profiles of other users, aswell of using administrative rights
if those have been granted to the user.

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

## Getting started (manually)
