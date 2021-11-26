#!/usr/bin/python3
"""

This reducer aggregates the counts related to each subreddit, user, and topic. Its output is in the following format:
a-subredditname c count 
a-subredditname t topic count
b-username c count  
b-username t topic count   
c-controversiality replycount
d topic count sumUpvotes sumDownvotes sumPositivity sumNegativity 

"""


import sys
import re

# Initialize all the required local variables
subreddit = None  
subredditTopic = None 
subredditCount = 0 
subredditTopicCount = 0
author = None
authorTopic = None 
authorCount = 0 
authorTopicCount = 0
commentid = None 
commentReplyCount = 0 
controversiality = 0 
topic = None 
topicCount = 0
upsCount = 0 
downsCount = 0 
posSum = 0
negSum = 0

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
            print('a-',subreddit,'\tc\t', subredditCount, sep='')
            print('a-',subreddit,'\tt\t', subredditTopic, '\t', subredditTopicCount, sep='')
            subreddit = words[1]
            subredditCount = 0 
            subredditTopicCount = 0
            subredditTopic = None 

        # If this line is related to the subreddit's count, add one to the subreddit's total count
        if words[2] == 'c':
            subredditCount += 1 
        # If otherwise, the line is related to the subreddit's topic
        else:
            # Initialize if this is the first subreddit topic to read
            if subredditTopic is None: 
                subredditTopic = words[3]
            # If this is a different subreddit topic than the one we've been working on, print the previous subreddit topic's data
            elif words[3] != subredditTopic:
                print('a-',subreddit,'\tt\t', subredditTopic, '\t', subredditTopicCount, sep='')
                subredditTopic = words[3]
                subredditTopicCount = 0
            # If this is the same subreddit topic, increment its count
            subredditTopicCount += 1
    
    # If the input line is related to a user
    elif words[0] == 'b':
        # Initialize if this is the first username to read
        if author is None:
            # Print the last subreddit entries if there were any
            if subreddit is not None: 
                print('a-',subreddit,'\tc\t', subredditCount, sep='')
                print('a-',subreddit,'\tt\t', subredditTopic, '\t', subredditTopicCount, sep='')
            author = words[1]
        # If this is a different user than the one we've been working on, print the previous user's data
        elif author != words[1]:
            print('b-',author,'\tc\t', authorCount, sep='')
            print('b-',author,'\tt\t', authorTopic, '\t', authorTopicCount, sep='')
            author = words[1]
            authorCount = 0 
            authorTopicCount = 0
            authorTopic = None 

        # If this line is related to the user's comment count, add one to the user's total count
        if words[2] == 'c':
            authorCount += 1 
        # If otherwise, the line is related to the user's comment topic
        else:
            # Initialize if this is the first user topic to read
            if authorTopic is None: 
                authorTopic = words[3]
            # If this is a different user topic than the one we've been working on, print the previous user topic's data
            elif words[3] != authorTopic:
                print('b-',author,'\tt\t', authorTopic, '\t', authorTopicCount, sep='')
                authorTopic = words[3]
                authorTopicCount = 0
            # If this is the same user topic, increment its count
            authorTopicCount += 1
             
    # If the input line is related to controversilaity
    elif words[0] == 'c':
        # Initialize if this is the first controversiality data to read
        if commentid is None:
            # Print the last user entries if there were any
            if author is not None:
                print('b-',author,'\tc\t', authorCount, sep='')
                print('b-',author,'\tt\t', authorTopic, '\t', authorTopicCount, sep='')
            commentid = words[1]
        # If this is a different comment than the one we've been working on, print the previous comment's controversiality data
        elif commentid != words[1]:
            print('c-',controversiality,'\t', commentReplyCount, sep='')
            commentid = words[1]
            commentReplyCount = 0
 
        # If this is the comment's controversiality, save it
        if words[2] == 'a': 
            controversiality = words[3]
        # If this is an entry related to the comment's replies, increment its reply count
        elif words[2] == 'b':
            commentReplyCount += 1

    # If the input line is related to topic's votes and sentiment
    elif words[0] == 'd':
        # Initialize if this is the first topic votes and sentiment data to read
        if topic is None:
            # Print the last controversilaity entries if there were any
            if commentid is not None: 
                print('c-',controversiality,'\t', commentReplyCount, sep='')
            topic = words[1]
        # If this is a different topic than the one we've been working on, print the previous topic's votes and sentiment data
        elif topic != words[1]:
            print('d','\t', topic,'\t',  topicCount, '\t', upsCount,'\t', downsCount,'\t', posSum,'\t', negSum, sep='')
            topic = words[1]
            topicCount = 0
            upsCount = 0
            downsCount = 0 
            posSum = 0
            negSum = 0

        # Increment the votes and sentiment counters
        topicCount += 1        
        upsCount += int(words[2])
        downsCount += int(words[3])
        posSum += int(words[4])
        negSum += int(words[5])

# Handle the last entry
if words[0] == 'a': 
    print('a-',subreddit,'\tc\t', subredditCount, sep='')
    print('a-',subreddit,'\tt\t', subredditTopic, '\t', subredditTopicCount, sep='')
elif words[0] == 'b': 
    print('b-',author,'\tc\t', authorCount, sep='')
    print('b-',author,'\tt\t', authorTopic, '\t', authorTopicCount, sep='')
elif words[0] == 'c': 
    print('c-',controversiality,'\t', commentReplyCount, sep='')
else: 
    print('d','\t', topic,'\t',  topicCount, '\t', upsCount,'\t', downsCount,'\t', posSum,'\t', negSum, sep='')


            









