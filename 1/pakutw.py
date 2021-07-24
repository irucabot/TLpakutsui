import tweepy
import MeCab
import sys

def main():
    consumer_key = ""
    consumer_secret = ""
    access_key = ""
    access_secret = ""

    endtext = ""
 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    m = MeCab.Tagger("-Owakati")

    for status in api.home_timeline(count=50,exclude_replies=True):
        text = status.text
        name = status.user.screen_name
        id = status.id_str
        if not 'RT' in text[0:2]:
            if not 'http' in text:
                node = m.parseToNode(text)
                words=[]
                while node:
                    hinshi = node.feature.split(",")[0]
                    if hinshi in ["動詞"]:
                        origin = node.feature.split(",")[6]
                        words.append(node.surface)
                    node = node.next
                if not len(words) == 0:
                    words = words[0]
                    if len(words) > 1:
                        textFind = text.find(words)
                        pl = textFind + len(words)
                        otext = text[0:pl]
                        node = m.parseToNode(otext)
                        words2=[]
                        while node:
                            hinshi = node.feature.split(",")[0]
                            if hinshi in ["動詞"]:
                                origin = node.feature.split(",")[10]
                                words2.append(origin)
                            node = node.next
                        if len(words2) > 0 and not len(words2) > 1:
                            words2 = words2[0]
                            twtext = otext[0:textFind]
                            twtext = twtext + words2
                            api.update_status(twtext+endtext)
                            userinfo = api.get_user(screen_name=name)
                            sys.exit()

if __name__ == '__main__':
    main()