#!/usr/bin/env python3

from urllib.request import urlopen
from math import sqrt
import json

#avgRatingCache = [0] * 17771

# -------------
# netlix_load_avg_rating_cache
# -------------

def netflix_load_avg_rating_cache ():
    global avgRatingCache
    url = urlopen("http://www.cs.utexas.edu/~ebanner/netflix-tests/BRG564-Average_Movie_Rating_Cache.json")
    avgRatingCache = json.loads(url.read().decode(url.info().get_param('charset') or 'utf-8'))
    
def netflix_load_avg_viewer_rating ():
    global avgViewerRatingCache
    url = urlopen("http://www.cs.utexas.edu/~ebanner/netflix-tests/ezo55-Average_Viewer_Rating_Cache.json")
    avgViewerRatingCache = json.loads(url.read().decode(url.info().get_param('charset') or 'utf-8'))
    #print("avg rating for cust 1585790 = %s" % avgViewerRatingCache.get("1585790"))

def netflix_load_movie_yrs_cache ():
    global movieYearsCache
    url = urlopen("http://www.cs.utexas.edu/~ebanner/netflix-tests/mw23845-movie_years.json")
    movieYearsCache = json.loads(url.read().decode(url.info().get_param('charset') or 'utf-8'))
    #print(movieYearsCache.get("19"))

def netflix_load_cust_years_cache ():
    global custYearsCache
    url = urlopen("http://www.cs.utexas.edu/~ebanner/netflix-tests/drc2582-customer_decade_dict.json")
    custYearsCache = json.loads(url.read().decode(url.info().get_param('charset') or 'utf-8'))

def netflix_get_viewer_avg_by_decade (custId, movieId):
    global custYearsCache
    global movieYearsCache
    movieYear = movieYearsCache.get(movieId)
    if(movieYear >= 1900 and movieYear < 1910):
        decade = "1900"
    elif(movieYear >= 1910 and movieYear < 1920):
        decade = "1910"
    elif(movieYear >= 1920 and movieYear < 1930):
        decade = "1920"
    elif(movieYear >= 1930 and movieYear < 1940):
        decade = "1930"
    elif(movieYear >= 1940 and movieYear < 1950):
        decade = "1940"
    elif(movieYear >= 1950 and movieYear < 1960):
        decade = "1950"
    elif(movieYear >= 1960 and movieYear < 1970):
        decade = "1960"
    elif(movieYear >= 1970 and movieYear < 1980):
        decade = "1970"
    elif(movieYear >= 1980 and movieYear < 1990):
        decade = "1980"
    elif(movieYear >= 1990 and movieYear < 2000):
        decade = "1990"
    elif(movieYear >= 2000 and movieYear < 2010):
        decade = "2000"
    elif(movieYear >= 2010 and movieYear < 2020):
        decade = "2010"
    else:
        return -1

    try:
        count = custYearsCache.get(custId).get(decade).get("count")
        total = custYearsCache.get(custId).get(decade).get("total")
        avgDecadeRating = total / count
    except AttributeError:
        avgDecadeRating = -1
    return avgDecadeRating

def netflix_predict (r, w):
    """
    r is expecting probe.txt
    w is going to convert the input customer id's to predicted movie rating
        and then output the RMSE
    """
    global avgRatingCache
    global avgViewerRatingCache
    global custYearsCache
    global movieYearsCache
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
            curMovieRating = str(avgRatingCache.get(curMovie))
            curViewerRating = str(avgViewerRatingCache.get(curCustId))
            expRating = str(probeSolution.get(curMovie).get(curCustId))
            #print("%s %s %s\n" % (type(curCustId),type(curRating),type(expRating)))
            n += 1
            try:
                decadeRating = netflix_get_viewer_avg_by_decade(curCustId, curMovie)
                if(decadeRating == -1):
                    predictedRating = (float(curMovieRating) + float(curViewerRating)) / 2
                else:
                    predictedRating = (float(curMovieRating) + float(curViewerRating) + float(decadeRating)) / 3
                rootMeanSum += netflix_rmse(float(predictedRating), float(expRating))
                w.write("curCust = %s.  curMovieRating = %s.  expRating = %s\n" %(curCustId, curMovieRating, expRating))
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
    netflix_load_avg_viewer_rating()
    netflix_load_movie_yrs_cache()
    netflix_load_cust_years_cache()
    netflix_predict(r, w)

    #dec = netflix_get_viewer_avg_by_decade("1048577","1") expect 4.466666666666667
    #print(dec)



