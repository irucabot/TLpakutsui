import tweepy
import MeCab
import sys


def main():
    try:
        consumer_key = ""
        consumer_secret = ""
        access_key = ""
        access_secret = ""

        starttext = ""
        endtext = ""

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
        m = MeCab.Tagger("-Owakati")

        for status in api.home_timeline(count=100, exclude_replies=True):
            text = status.text
            name = status.user.screen_name
            id = status.id_str
            me = api.me()
            if not 'RT @' in text[0:4] and not 'http' in text and not name == me.screen_name and not '@' in text:
                node = m.parseToNode(text)
                words = []
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
                        words2 = []
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
                            node = m.parseToNode(twtext)
                            wordst=[]
                            while node:
                                wordst.append(node.surface)
                                node = node.next
                            try:
                                wordpl = wordst.index(words2)
                            except ValueError:
                                continue
                            else:
                                btext = wordst[wordpl - 1]
                                m = MeCab.Tagger("")
                                #if '助動詞' in m.parse(btext) or '助詞' in m.parse(btext):
                                if not '名詞' in m.parse(btext):
                                    btext = wordst[wordpl - 2]
                                    if not '名詞' in m.parse(btext):
                                        continue
                                    else:
                                        ctext = btext + wordst[wordpl - 1]
                                else:
                                    ctext = btext
                                word = wordst[wordpl]
                                node = m.parseToNode(word)
                                words3 = []
                                while node:
                                    hinshi = node.feature.split(",")[0]
                                    if hinshi in ["動詞"]:
                                        origin = node.feature.split(",")[10]
                                        words3.append(origin)
                                    node = node.next
                                if len(words3) > 0 and not len(words3) > 1:
                                    words3 = words3[0]
                                    twtext = ctext + words3
                                    replyText = starttext + twtext + endtext
                                    api.update_status(replyText)
                                    sys.exit()
        print('拾える文章が見つかりません。')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
