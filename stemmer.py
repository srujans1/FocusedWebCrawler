import Stemmer

# Method for stemming tokens
def stemmer ( array ):
    stemmer = Stemmer.Stemmer('english')
    try:
        print "Stemming"
        return stemmer.stemWords(array)
    except:
        print "Stemming error"