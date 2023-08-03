# 6.0001/6.00 Problem Set 5 - RSS Feed Filter

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        
        try:
            description = translate_html(entry.description)
        except Exception:
            description = ''
        pubdate = translate_html(entry.published)

        try:
            ## Beware DateFormatting!! 
            pubdate = datetime.strptime(pubdate, '%Y-%m-%dT%H:%M:%SZ')
          #  pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=pytz.UTC)
        except ValueError:
            pubdate = datetime.strptime(pubdate, '%a, %d %b %Y %H:%M:%S %Z')

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

class NewsStory(object):
    
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate.replace(tzinfo=pytz.UTC)
        
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower().split()
        
    def is_phrase_in(self, inputText):
        #InputClean
        
        newString = ''
        for letter in inputText:
            if letter in string.punctuation or letter == ' ':
                newString = newString + ' '
            else: 
                newString = newString + letter.lower() 
                
        inputList = newString.split()
        
        for part in inputList:
            part = part.strip()
        
        for word in inputList:
            if word == self.phrase[0]:
                start = inputList.index(word)
                check = inputList[start:start+len(self.phrase)]
                if check == self.phrase:
                    return True
        return False
                
# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower().split()
        
    def evaluate(self, story):
        if self.is_phrase_in(story.get_title()): return True
        else: return False

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower().split()
        
    def evaluate(self, story):
        if self.is_phrase_in(story.get_description()): return True
        else: return False

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
    def __init__(self, time):
        self.time = datetime.strptime(time, '%d %b %Y %H:%M:%S').replace(tzinfo=pytz.UTC)

# Problem 6
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        if story.get_pubdate() < self.time:
            return True
        return False
    
class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        if story.get_pubdate() > self.time:
            return True
        return False

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
        
    def evaluate(self, story):
        if self.trigger.evaluate(story): return False
        
        return True

# Problem 8
class AndTrigger(Trigger):
    def __init__(self, triggerA, triggerB):
        self.triggerA = triggerA
        self.triggerB = triggerB
        
    def evaluate(self, story):
        if self.triggerA.evaluate(story) and self.triggerB.evaluate(story): return True
        
        return False

# Problem 9
class OrTrigger(Trigger):
    def __init__(self, triggerA, triggerB):
        self.triggerA = triggerA
        self.triggerB = triggerB
        
    def evaluate(self, story):
        if self.triggerA.evaluate(story) or self.triggerB.evaluate(story): return True
        
        return False

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    returnList = list()

    for trigger in triggerlist:
        for story in stories:
            if trigger.evaluate(story):
                returnList.append(story)

    return returnList

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
            
    triggerDict = dict()
    triggerlist = list()
    for line in lines:
        tmp = line.split(',')
        
        if tmp[1] == 'DESCRIPTION':
            toAdd = DescriptionTrigger(tmp[2])
            triggerDict[tmp[0]] = toAdd
        elif tmp[1] == 'TITLE':
            toAdd = TitleTrigger(tmp[2])
            triggerDict[tmp[0]] = toAdd
        elif tmp[1] == 'AFTER':
            toAdd = AfterTrigger(tmp[2])
            triggerDict[tmp[0]] = toAdd
        elif tmp[1] == 'AND':
            toAdd = AndTrigger(triggerDict[tmp[2]], triggerDict[tmp[3]])
            triggerDict[tmp[0]] = toAdd
            
        elif tmp[0] == 'ADD':
            for trigger in tmp[1:]:
                triggerlist.append(triggerDict[trigger])
                return triggerlist
            
SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

