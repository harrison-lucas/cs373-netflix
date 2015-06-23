#!/usr/bin/env python3

avgRatingCache = [0] * 17770

# -------------
# netlix_load_avg_rating_cache
# -------------

def netflix_load_avg_rating_cache ():
    global avgRatingCache
    avgMovieRatingFile = open('./BRG564-Average_Movie_Rating_Cache.json')
    i = 0
    for line in avgMovieRatingFile.readlines():
        t = line.split(":")
        if(len(t) > 1):
            temp = t[1].split(",")
            temp = temp[0].split(" ")
            avgRatingCache[i] = temp[1]
            i += 1
    #print(type(avgRatingCache))
    #print(type(avgRatingCache[0]))
    #print(avgRatingCache[0])
    #print(len(avgRatingCache))

# -------------
# netlix_solve
# -------------

def netflix_solve (r, w) :
    """
    r a reader
    w a writer
    """
    global avgRatingCache
    print("initial commit")

    avgMovieRating = open('./BRG564-Average_Movie_Rating_Cache.json')
    netflix_load_avg_rating_cache()

    for i in range(0,17770):
    	w.write(avgRatingCache[i] + "\n")
