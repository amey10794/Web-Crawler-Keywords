Description :
This code can extract keywords from a provided website URL.
It takes a site url as the input and provides with 5 keywords for the site
The following is a list of steps used:
    
    1. Download the html for the given webpage using the requests library
    2. Extract all the parts of the site using beautifulsoup library
        - Title
        - URL
        - Meta keywords
        - Meta description
        - Headings
        - Content
        (Executed in 2 parts: Title,URL,Meta's & Headings are treated as one while content is treated as the other)
        
    The following steps are done for both the above mentioned parts
    
    3. Process all the text
        - make every word lowercase.
        - remove non-alphanumeric character, except space bar & '-' to ensure collection words like cpt-122 are used for keyword extraction. e.g. !,@,#,$,\r,\t,\n
    4. Remove stopwords from the text
    5. Lemmatize the text to ensure words like friends & campings are converted to their root formats for better word matching & count i.e friend and camping in this case
    6. Get the word count for unigrams
        - single words from the text eg: [echo,dot,amazon,alexa] 
        - Generate a bag of words or word count type of representation
    7. Get the word count for bigrams
        - word combinations from the text eg: [echo dot, amazon alexa] 
        - I feel bigrams are more useful for keyword determination since words repeating together even after removal of stop words have more chances of being a keyword
        - double weight is given to bigram words in the bag of words representation
    8. Bags for content and other Meta's are merged together 
    and sorted in descending order on the basis of their counts or weights,
    triple weight is given to top keywords from the meta info.
    9. The first 5 words of the sorted array are reported as keywords

File Structure :
	The project is divided into 2 major parts: 
		Keywords Class : Responsible for web crawling, text processin,word countings, and analysis. 
		Main Program   : Responsible for taking user input and perform program execution.


Tests:

The following are different links I used while testing and their results

1. http://www.amazon.com/Cuisinart-CPT-122-Compact-2-Slice-Toaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster  
Keywords: toaster, cusinart, compact, 2slice, cpt122

2. http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/
Keywords: friend, indoorsy, outdoors, introduce, hike

3. http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/
Keywords: nsa, leak, privacy, safeguard, man

4. https://www.amazon.com/All-new-Echo-Dot-3rd-Gen/dp/B0792K2BK6/ref=redir_mobile_desktop?_encoding=UTF8&ref_=ods_gw_dg1_ha_dt_092018
Keywords:echo, dot, amazon, alexa, speaker

5. https://medium.com/s/nerd-processor/how-to-save-the-dc-superhero-movie-universe-b9f9a9004847
Keywords: movie, dc, universe, superhero, bros

6. https://medium.com/s/story/inside-apples-iphone-xs-camera-technology-50d47ba7be8f
Keywords: Apple, x, Iphone, Camera, inside