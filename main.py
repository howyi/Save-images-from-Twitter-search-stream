# coding: utf-8

# Python 3.4.3
# tweepy 3.3.0

import os
import sys
import webbrowser
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
import shelve
import urllib
import tkinter
import tkinter.filedialog

root = tkinter.Tk()
root.withdraw()
default_dir = '.'
save_directory = ''

f = open(os.path.dirname(os.path.abspath(__file__))+'\consumer_key.txt')

consumer_key = f.readline().rstrip('\n')
consumer_secret = f.readline().rstrip('\n')
keyword = '#image'  #searchstreamでtrackするワード

class streamListener(StreamListener):   #StreamingAPI
    def on_status(self, status):
        if not hasattr(status, 'retweeted_status'): #RTを除外
            try:
                print ('   ' + status.author.name + ':'+  status.text)
            except:
                print ('error')
            if u'media' in status.entities.keys():
                for i in status.entities[u'media']:
                    try:
                        getImage(save_directory,i['media_url'])
                        print ('success:' + i['media_url'])
                    except Exception as e:
                        print ('failed:' + e.message)



    def on_error(self, status):
        print (status)

def getImage(directory,url):
    img = urllib.request.urlopen(url)
    localfile = open(directory + url[url.rfind('/')+1:], 'wb')
    localfile.write(img.read())
    img.close()
    localfile.close()

if __name__ == "__main__":

    save_directory = tkinter.filedialog.askdirectory(initialdir=default_dir) + "/"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    dic = shelve.open('./key')

    if 'access_token' in dic.keys():
        access_token = dic['access_token']
        access_token_secret = dic['access_token_secret']

        dic['access_token'] = token[0]
        dic['access_token_secret'] = token[1]
    else:
        webbrowser.open(auth.get_authorization_url())
        pin = input('PIN: ').strip()
        token = auth.get_access_token(verifier=pin)
        print(token[0])
        dic['access_token'] = token[0]
        dic['access_token_secret'] = token[1]
        access_token = token[0]
        access_token_secret = token[1]

    dic.close()

    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth_handler=auth)

    l = streamListener()
    stream = Stream(auth, l)
    stream.filter(track=[keyword])
