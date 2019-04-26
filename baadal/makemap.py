import gmplot 
#lat_list = []
#long_list= []
#birdlist= ['No bird','No bird','No bird','No bird','No bird']
#import gmplot
def make(birdlist):
    lat = [28.5456577, 28.5456090, 28.5455228,28.5453143,28.5455250]
    long = [ 77.1907005, 77.1903190,77.1905399,77.1906073,77.1902370]
    gmap3 = gmplot.GoogleMapPlotter(28.5455,77.19046,20)
# scatter method of map object
# scatter points on the google map
    birdnames=['sparrow','maina','crow','bulbul','pigeon','No bird']
    gmap3.marker(lat[0],long[0],title=("location 1: "+birdnames[birdlist[0]]))
    gmap3.marker(lat[1],long[1],title=("location 2: "+birdnames[birdlist[1]]))
    gmap3.marker(lat[2],long[2],title=("location 3: "+birdnames[birdlist[2]]))
    gmap3.marker(lat[3],long[3],title=("location 4: "+birdnames[birdlist[3]]))
    gmap3.marker(lat[4],long[4],title=("location 5: "+birdnames[birdlist[4]]))
#    gmap3.marker(lat[2],long[2],title="location3")


# Plot method Draw a line in
# between given coordinates
    gmap3.plot(lat, long,'cornflowerblue', edge_width = 2.5)
    gmap3.draw( "map1.html" )
