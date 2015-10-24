## bbgps (short for Big Brother GPS)

### About
A very simple web interface for the great Android application called [Big Brother GPS](https://play.google.com/store/apps/details?id=org.gnarf.bigbrother.gps) that regularly sends the phone position to a server via a POST request. It supports authentication via a **secret** and reports various parameters (*latitude, longitude, speed, bearing, altitude, battery level, accuracy, provider etc.*)

### Demo
You can check a running version of this application [here](http://bbgps.rssind.com/). Some details:

* I used an old [Google Nexus S](https://en.wikipedia.org/wiki/Nexus_S) phone that I kept in the car and charged it only while driving
* had to manually switch mobile providers a few times (usually at border crossings)
* I set-up the Android application to send the position every 3 minutes; it worked quite OK and the battery usually lasted around two days 
* the application is hosted on a [Raspberry PI 2](https://www.raspberrypi.org/products/raspberry-pi-2-model-b/) running in my house
* I have a dynamic IP from my ISP so there might be some update delay (usually due to power outages), the domain is hosted at [Free DNS](http://freedns.afraid.org/)

Some screenshots:

![Path](http://rssind.com/images/path.png)

![Source](http://rssind.com/images/source.png)

![Battery](http://rssind.com/images/battery.png)

### Requirements
This web interface is written in [Python](https://www.python.org/) and uses the following packages:

 * [Tornado](http://www.tornadoweb.org/en/stable/) for the webserver part
 * [pymongo](https://api.mongodb.org/python/current/) for the database part
 * optionally [pyproj](https://github.com/jswhit/pyproj) for cartographic transformations utility function (not used for the web interface)
 * other APIs used: [Google Maps Javascript](https://developers.google.com/maps/documentation/javascript/), [Google Charts](https://developers.google.com/chart/?hl=en), [jQuery](https://jquery.com/) 
 
### Installation

 * install the above packages
 * copy the settings file (```cp settings_default.py settings.py```)
 * edit the settings (mainly ```SECRET``` and ```DB_URI```) 
 * make sure you have [MongoDB](https://www.mongodb.org/) running or use a hosted service (I used the free version from [MongoLab](https://mongolab.com/) mainly because getting MongoDB to run on RaspberryPi is tedious)
 * start the application ```python bbgps.py```