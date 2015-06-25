#!/usr/bin/env python3

from urllib.request import urlopen
from math import sqrt
import json

avgRatingCache = [0] * 17771

# -------------
# netlix_load_avg_rating_cache
# -------------

def netflix_load_avg_rating_cache ():
    global avgRatingCache
    url = urlopen("http://www.cs.utexas.edu/~ebanner/netflix-tests/BRG564-Average_Movie_Rating_Cache.json")
    avgRatingCache = json.loads(url.read().decode(url.info().get_param('charset') or 'utf-8'))
    


def netflix_predict (r, w):
    """
    r is expecting probe.txt
    w is going to convert the input customer id's to predicted movie rating
        and then output the RMSE
    """
    global avgRatingCache
    global probeSolution
    curMovie = ""
    n = 1
    rootMeanSum = 0.0
    for line in r.readlines():
        if(":" in line):
            #print(line)
            
            curMovie = line[:len(line)-2]
            #w.write("line = %s.  Current Movie = %s\n" %(line,curMovie))
            w.write(line)
        else:
            if(line[len(line)-1] == '\n'):
                curCustId = line[:len(line)-1]
            else:
                curCustId = line[:len(line)]
            curRating = str(avgRatingCache.get(curMovie))
            expRating = str(probeSolution.get(curMovie).get(curCustId))
            #print("%s %s %s\n" % (type(curCustId),type(curRating),type(expRating)))
            n += 1
            try:
                rootMeanSum += netflix_rmse(float(curRating), float(expRating))
                w.write("curCust = %s.  curRating = %s.  expRating = %s\n" %(curCustId, curRating, expRating))
            except TypeError:
                w.write("TypeError\n")

    rootMeanSum /= n
    w.write(str(sqrt(rootMeanSum)))
            
# -------------
# netlix_rmse
# -------------
def netflix_rmse (predicted, expected) :
    return (expected - predicted) ** 2



# -------------
# netlix_solve
# -------------

def netflix_solve (r, w) :
    """
    r a reader
    w a writer
    """
    global avgRatingCache
    global probeSolution

    url = urlopen("http://www.cs.utexas.edu/~ebanner/netflix-tests/pam2599-probe_solutions.json")
    probeSolution = json.loads(url.read().decode(url.info().get_param('charset') or 'utf-8'))
    #print(probeSolution.get("1").get("30878"))

    netflix_load_avg_rating_cache()
    netflix_predict(r, w)



