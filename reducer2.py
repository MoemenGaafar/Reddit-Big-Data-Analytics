#!/usr/bin/python3

"""
This reducer finds and prints the most popular 3 topics for each subreddit and each user. It also finds the top 5 upvoted,
downvoted, positive sentiment, and negative sentiment topics. Its output is in the following format:
a subredditname count topic topic topic
b username count topic topic topic
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
subredditMaxTopicCount = [0, 0, 0]

author = None
authorCount = 0
authorMaxTopic = [None, None, None]
authorMaxTopicCount = [0, 0, 0]

controversiality = None
controversialityCount = 0
controversialityReplyCount = 0 

maxTopics = [None, None, None, None, None, None, None, None, None, None]
maxTopicsCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
maxUpsTopics = [None, None, None, None, None, None, None, None, None, None]
maxUpsTopicsCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
maxDownsTopics = [None, None, None, None, None, None, None, None, None, None]
maxDownsTopicsCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
maxPosTopics = [None, None, None, None, None, None, None, None, None, None]
maxPosTopicsCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
maxNegTopics = [None, None, None, None, None, None, None, None, None, None]
maxNegTopicsCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Variables to be used in max-finding processes
tempTopic = None
tempCount = 0
tempUps = 0
tempDowns = 0
tempPos = 0
tempNeg = 0
place = 0
i = 0

key0 = 1 # Just a flag to show if we exited from area c to area d 


for line in sys.stdin:

    # Strip and split the input line
    line_stripped = line.strip()
    words = re.split('-|\t', line_stripped)

    # If the input line is related to a subreddit
    if words[0] == 'a':
        # Initialize if this is the first subreddit to read
        if subreddit is None:
            subreddit = words[1]
        # If this is a different subreddit than the one we've been working on, print the previous subreddit's data
        elif subreddit != words[1]:
            print('a\t',subreddit,'\t', subredditCount,'\t', subredditMaxTopic[0],'\t', subredditMaxTopic[1], '\t',subredditMaxTopic[2] , sep='')              
            subreddit = words[1]
            subredditMaxTopic = [None, None, None]
            subredditMaxTopicCount = [0, 0, 0]

        # If this line is related to the subreddit count, save it
        if words[2] == 'c':
            subredditCount = words[3]
        # If otherwise, the line is related to the subreddit's topic, compare the topic count with the existing top counts
        else:
            tempTopic = words[3]
            tempCount = int(words[4])
            place = -1
            i = 0
            while tempCount > subredditMaxTopicCount[i]:
                place = i
                i += 1
                if i == len(subredditMaxTopicCount): 
                    break
            if place > 0: 
                i = 1
                while i <= place: 
                    subredditMaxTopicCount[i-1] = subredditMaxTopicCount[i]
                    subredditMaxTopic[i-1] = subredditMaxTopic[i]
                    i += 1
                subredditMaxTopicCount[place] = tempCount
                subredditMaxTopic[place] = tempTopic
            elif place == 0:
                subredditMaxTopicCount[place] = tempCount
                subredditMaxTopic[place] = tempTopic

    # If the input line is related to a username
    elif words[0] == 'b':
        # Initialize if this is the first user to read
        if author is None:
            # Print the last subreddit entries if there were any
            if subreddit is not None: 
                print('a\t',subreddit,'\t', subredditCount,'\t', subredditMaxTopic[0],'\t', subredditMaxTopic[1], '\t',subredditMaxTopic[2] , sep='')
            author = words[1]
        # If this is a different user than the one we've been working on, print the previous user's data
        elif author != words[1]:
            print('b\t',author, '\t',authorCount,'\t', authorMaxTopic[0],'\t', authorMaxTopic[1],'\t', authorMaxTopic[2] , sep='')                 
            author = words[1]
            authorMaxTopic = [None, None, None]
            authorMaxTopicCount = [0, 0, 0]

        # If this line is related to the user count, save it
        if words[2] == 'c':
            authorCount = words[3]
        # If otherwise, the line is related to the user's comment topic, compare the topic count with the existing top counts
        else:
            tempTopic = words[3]
            tempCount = int(words[4])
            place = -1
            i = 0
            while tempCount > authorMaxTopicCount[i]:
                place = i
                i += 1
                if i == len(authorMaxTopicCount): 
                    break
            if place > 0: 
                i = 1
                while i <= place: 
                    authorMaxTopicCount[i-1] = authorMaxTopicCount[i]
                    authorMaxTopic[i-1] = authorMaxTopic[i]
                    i += 1
                authorMaxTopicCount[place] = tempCount
                authorMaxTopic[place] = tempTopic
            elif place == 0:
                authorMaxTopicCount[place] = tempCount
                authorMaxTopic[place] = tempTopic

    # If the input line is related to controversilaity
    elif words[0] == 'c':
        # Initialize if this is the first controversiality data to read
        if controversiality is None:
            # Set the key0 flag to 1 because we are in the 'c' section
            key0 = 1
            # Print the last user entries if there were any
            if author is not None: 
                print('b\t',author, '\t',authorCount,'\t', authorMaxTopic[0],'\t', authorMaxTopic[1],'\t', authorMaxTopic[2] , sep='')
            controversiality = words[1]
        # If this is a different controversiality value than the one we've been working on, print the previous controversiality data
        elif controversiality != words[1]:
            print('c',controversiality, controversialityCount, controversialityReplyCount, sep='\t')
            controversiality = words[1]
            controversialityCount = 0
            controversialityReplyCount = 0
        # If this is the same controversiality value, increment its counter and reply count
        controversialityCount += 1
        controversialityReplyCount += int(words[2])
    
    # If the input line is related to topic's votes and sentiment
    elif words[0] == 'd':
            # Print the last controversiality entry if there were any
            if key0 == 1:
                print('c',controversiality, controversialityCount, controversialityReplyCount, sep='\t')
                key0 = 2
            tempTopic = words[1]
            tempCount = int(words[2])
            tempUps = int(words[3])
            tempDowns = int(words[4])
            tempPos = int(words[5])
            tempNeg = int(words[6])

            # Find if this is one of the 5 max used topics 
            place = -1
            i = 0
            while tempCount > maxTopicsCount[i]:
                place = i
                i += 1
                if i == len(maxTopicsCount): 
                    break
            if place > 0: 
                i = 1
                while i <= place: 
                    maxTopicsCount[i-1] = maxTopicsCount[i]
                    maxTopics[i-1] = maxTopics[i]
                    i += 1
                maxTopicsCount[place] = tempCount
                maxTopics[place] = tempTopic
            elif place == 0:
                maxTopicsCount[place] = tempCount
                maxTopics[place] = tempTopic


            # Find if this is one of the 5 max upvoted topics
            place = -1
            i = 0
            while tempUps > maxUpsTopicsCount[i]:
                place = i
                i += 1
                if i == len(maxUpsTopicsCount): 
                    break
            if place > 0: 
                i = 1
                while i <= place: 
                    maxUpsTopicsCount[i-1] = maxUpsTopicsCount[i]
                    maxUpsTopics[i-1] = maxUpsTopics[i]
                    i += 1
                maxUpsTopicsCount[place] = tempUps
                maxUpsTopics[place] = tempTopic
            elif place == 0:
                maxUpsTopicsCount[place] = tempUps
                maxUpsTopics[place] = tempTopic


            # Find if this is one of the 5 max downvoted topics
            place = -1
            i = 0
            while tempDowns > maxDownsTopicsCount[i]:
                place = i
                i += 1
                if i == len(maxDownsTopicsCount): 
                    break
            if place > 0: 
                i = 1
                while i <= place: 
                    maxDownsTopicsCount[i-1] = maxDownsTopicsCount[i]
                    maxDownsTopics[i-1] = maxDownsTopics[i]
                    i += 1
                maxDownsTopicsCount[place] = tempDowns
                maxDownsTopics[place] = tempTopic
            elif place == 0: 
                maxDownsTopicsCount[place] = tempDowns
                maxDownsTopics[place] = tempTopic


            # Find if this is one of the 5 max positive topics 
            place = -1
            i = 0
            while tempPos > maxPosTopicsCount[i]:
                place = i
                i += 1
                if i == len(maxPosTopicsCount): 
                    break
            if place > 0: 
                i = 1
                while i <= place: 
                    maxPosTopicsCount[i-1] = maxPosTopicsCount[i]
                    maxPosTopics[i-1] = maxPosTopics[i]
                    i += 1
                maxPosTopicsCount[place] = tempPos
                maxPosTopics[place] = tempTopic
            elif place == 0:
                maxPosTopicsCount[place] = tempPos
                maxPosTopics[place] = tempTopic


            # Find if this is one of the 5 max negative topics 
            place = -1
            i = 0
            while tempNeg > maxNegTopicsCount[i]:
                place = i
                i += 1
                if i == len(maxNegTopicsCount): 
                    break
            if place > 0: 
                i = 1
                while i <= place: 
                    maxNegTopicsCount[i-1] = maxNegTopicsCount[i]
                    maxNegTopics[i-1] = maxNegTopics[i]
                    i += 1
                maxNegTopicsCount[place] = tempNeg
                maxNegTopics[place] = tempTopic
            elif place == 0:
                maxNegTopicsCount[place] = tempNeg
                maxNegTopics[place] = tempTopic


# Handle the last entry
if words[0] == 'a':
    print('a\t',subreddit,'\t', subredditCount,'\t', subredditMaxTopic[0],'\t', subredditMaxTopic[1], '\t',subredditMaxTopic[2] , sep='')     

elif words[0] == 'b': 
    print('b\t',author, '\t',authorCount,'\t', authorMaxTopic[0],'\t', authorMaxTopic[1],'\t', authorMaxTopic[2] , sep='')

elif words[0] == 'c':
    print('c',controversiality, controversialityCount, controversialityReplyCount, sep='\t') 

# Print topics with Max values 
for i in range(len(maxTopics)): 
    print('d', maxTopics[i], maxTopicsCount[i], sep='\t')
for i in range(len(maxUpsTopics)): 
    print('e',maxUpsTopics[i], maxUpsTopicsCount[i], sep='\t')
for i in range(len(maxDownsTopics)): 
    print('f',maxDownsTopics[i], maxDownsTopicsCount[i], sep='\t')
for i in range(len(maxPosTopics)): 
    print('g',maxPosTopics[i], maxPosTopicsCount[i], sep='\t')
for i in range(len(maxNegTopics)): 
    print('h',maxNegTopics[i], maxNegTopicsCount[i], sep='\t')










