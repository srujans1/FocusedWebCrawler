Focused Web Crawler- by Srujan Saggam and Anshul Mehra

The list of files :

1) crawler.py - This is the main file which runs the crawler it co-ordirantes between all the components of the crawler. It should be run from command line as follows:
 python crawler.py <Query> <Number of result pages>

2) gQuery.py - this file contains code to fetch the top 10 results of google search query.

3) MyPriorityQueue - this file contains a class which extends the PriorityQueue.(Added extra counter variable)

4) priorityCalculator.py - this file contains code which takes url and it tokenizes the page content by passing it to a tokenizer and then it passes the tokens to a stemmer. The tokens generated are then used to calculate the relevance of the page to the search query..

5) tokenizer.py - this file contains methods to tokenize the page content which is passes from priorityCalculator.py. NLTK libraries were used for stopwords and removing punctuations.

6) stemmer.py - this contains the code to generate stemmed tokens for an array of tokens passed as input.

 
