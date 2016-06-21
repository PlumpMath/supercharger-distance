# Calculating Tesla Supercharger distances.

I've always admired Tesla's cars. The design, the technology, commitment
to the environment. It's all great. I live in a city, and park on the
street and will likely not drive one (at least for some time). Even so,
I was curious about something.

Tesla provides the Supercharger stations, allowing owners of Tesla vehicles
to refuel for free (?). I wanted to see if these were placed close enough that
one could reasonably rely on them for travel.

The minimum range for a Tesla is 215 miles on a charge for the Model 3. Using
this as my metric, I used [Requests](http://docs.python-requests.org/en/master),
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup), and
[GeoPy](http://geopy.readthedocs.io/en/latest) to figure this out.

I grabbed the Tesla Supercharger lists page with Requests. I then pulled each
of the address sections out using BeautifulSoup. Finally, I used GeoPy to
convert the addresses to geographic coordinates. This was the only part that
caused me any issues. Different geocoding services differ in their knowledge
base (Google was the best in my experience). Also, some of the addresses were
loose (ex. Mile Marker X on 95) and wouldn't return a coordinate pair.

With all of this information, it was pretty trivial to calculate.

I could probably optimize the pair generation a bit. But the volume of data here
was so small that it didn't even seem worth it.