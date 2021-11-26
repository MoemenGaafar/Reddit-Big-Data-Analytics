#!/usr/bin/python3
"""
This reducer finally aggregates and presents the required statistics. Its output is in the following format:
a subredditname count topic topic topic (for the 5 most popular subreddits)
b username count topic topic topic (for the 5 most popular users)
c controversality count replycount
d topic count (for the 5 most popular topics)
e topic ups (for the 5 most upvoted topics)
f topic downs (for the 5 most downvoted topics)
g topic positivity (for the 5 most positive topics)
h topic negativity (for the 5 most negative topics)

"""

import sys
import re

# Initialize all the required local variables
subreddit = None
subredditCount = 0
subredditMaxTopic = [None, None, None]
subredditMax = [None, None, None, None, None, None, None, None, None, None]
subredditMaxCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
subredditMaxTopics = [ [ None for i in range(3) ] for j in range(10)] 
author = None
authorCount = 0
authorMaxTopic = [None, None, None]
authorMax = [None, None, None, None, None, None, None, None, None, None]
authorMaxCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
authorMaxTopics = [ [ None for i in range(3) ] for j in range(10)] 

# Variables to be used in max-finding processes
tempTopic = None
tempCount = 0
place = 0
i = 0


for line in sys.stdin:

    # Strip and split the input line
    line_stripped = line.strip()
    words = re.split('-|\t', line_stripped)

    # If the input line is related to a subreddit
    if words[0] == 'a':
            subreddit = words[1]
            subredditCount = int(words[2])
            subredditMaxTopic = [words[3], words[4], words[5]]
            
            # Find if this is one of the 5 most popular subreddits
            place = -1
            i = 0
            while subredditCount > subredditMaxCount[i]:
                place = i
                i += 1
                if i == len(subredditMaxCount): 
                    break
        
            if place > 0: 
                i = 1
                while i <= place: 
                    subredditMaxCount[i-1] = subredditMaxCount[i]
                    subredditMax[i-1] = subredditMax[i]
                    subredditMaxTopics[i-1] = subredditMaxTopics[i]
                    i += 1
                subredditMaxCount[place] = subredditCount
                subredditMax[place] = subreddit
                subredditMaxTopics[place] = subredditMaxTopic  
            elif place == 0:   
                subredditMaxCount[place] = subredditCount
                subredditMax[place] = subreddit
                subredditMaxTopics[place] = subredditMaxTopic  

    # If the input line is related to a username
    elif words[0] == 'b':
            author = words[1]
            authorCount = int(words[2])
            authorMaxTopic = [words[3], words[4], words[5]]

            # Find if this is one of the 5 most popular users
            place = -1
            i = 0
            while authorCount > authorMaxCount[i]:
                place = i
                i += 1
                if i == len(authorMaxCount): 
                    break
            if place > 0: 
                i = 1
                while i <= place: 
                    authorMaxCount[i-1] = authorMaxCount[i]
                    authorMax[i-1] = authorMax[i]
                    authorMaxTopics[i-1] = authorMaxTopics[i]
                    i += 1
                authorMaxCount[place] = authorCount
                authorMax[place] = author
                authorMaxTopics[place] = authorMaxTopic
            elif place == 0:
                authorMaxCount[place] = authorCount
                authorMax[place] = author
                authorMaxTopics[place] = authorMaxTopic

    else:
        # Print all other statistics as is
        print(line.strip())


# Print Max subreddits
for i in range(len(subredditMaxCount)): 
    print('a',subredditMax[i], subredditMaxCount[i], subredditMaxTopics[i][0], subredditMaxTopics[i][1], subredditMaxTopics[i][2], sep='\t')


# Print Max authors
for i in range(len(authorMaxCount)): 
    print('b',authorMax[i], authorMaxCount[i], authorMaxTopics[i][0], authorMaxTopics[i][1], authorMaxTopics[i][2], sep='\t')
 




