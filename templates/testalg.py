def swipeupdate(userid, movieid)
    c = connect()
    c.execute("select start_year, genres from title_basics where title_id = '?'", movieid) #TODO: quotes in placeholder might be wrong here
    movie = c.fetchone()

    # Can i use fetchone in succession like this??

    c.execute("select director, genre, year from attributes where user_id = '?'", userid)
    useratt = c.fetchone()

    #TODO: Pseudocode starts here
    for moviegenre in movie[genres]:
        checkTrue = 0
        for selectedgenre in useratt[genre]:
            if selectedgenre == moviegenre:
                useratt[genre].selectedgenre += 1
                checkTrue += 1
        if checkTrue = 0:
            Add a new genre to the user attributes with score = 1

    checkTrueY = 0
    for selectedyear in useratt[year]:
        if selectedyear == movie[start_year]:
            useratt[year].selectedyear += 1
            checkTrueY += 1
    if checkTrueY = 0:
        Add a new year to the user attributes with score = 1

    Update SQL database, plugging in new values from useratt
        






def indivsuggest(UserID):
    GenV = 1
    DirV = 1
    YearV = 1
    RatM = 2
    
    c = connect()
    userlist = c.execute("select director, genre, year from attributes where user_id = '?'", UserID) #TODO: quotes in placeholder might be wrong here
    movielist = c.execute("select title_id, start_year, genres from title_basics")
    movieratings = c.execute("select title_id, average_rating from title_ratings")
    
    user = userlist.fetchone()
    movie = movielist.fetchone()
    while user is not None:
        scoreranking = {}
        while movie is not None:
            MovieScore = 0
            #TODO: Pseudocode starts here
            for director in user[director]: 
                if director == movie[director]:
                    MovieScore += director.score * DirV
            for genre in user[genre]: 
                if genre == movie[genre]:
                    MovieScore += genre.score * GenV
            for year in user[year]: 
                if year + n == movie[year]:
                    MovieScore += year.score * YearV
            scoreranking[movie[title_id]] = MovieScore
    Truncate the existing scoreranking dict to include only the top 10 scores
      disconnect(c)
    return scoreranking
        
        
                
            



def groupsuggest(groupcode):
    c = connect()
    userlist = c.execute('select director, genre, year, movies_seen, movies_swiped from attributes where user_id in (select users from groups where code = ?)', groupcode) 
                # TODO: Fix fetching users from database, because Dylan said it's stored as a string
    NewUserID = Make a new User #TODO: Make a new user
    for user in userlist:
        total = int(user[movies_seen]) + int(user[movies_swiped])
        for category in user.items(): #TODO Don't know if .items() is appropriate here
            #TODO: Pseudocode begins here
            for item in category:
                scaleditem = item / total
                Append/add item value to NewUser (This has to take into account whether the item is already in newuser) #TODO: add item to newuser
    disconnect(c)
    return indivsuggest(NewUserID)
    # Ther eMight be a better/easier idea than making a new user here.
                



    
    







for user in group:
    for each category in user:
        Divide all values by lowest value in category OR divide by sum of movies seen+swiped. Where does movies seen come from?
        Add to running sum in dict
    
Run algorithm on resulting dict


# merge users into 1 for group
