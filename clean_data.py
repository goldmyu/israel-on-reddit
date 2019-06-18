import pandas as pd
import re  # regular expression
import preprocessor as p
from nltk.tokenize import word_tokenize
import string

# import nltk
# nltk.download()

# =================================================================================================
data = pd.read_csv("data-sets/fortnite.csv")
clean_data = data['text'][0:10000].copy()

# =================================================================================================

# HappyEmoticons
emoticons_happy = {':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}', ':^)', ':-D', ':D', '8-D',
                   '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D', '=-3', '=3', ':-))', ":'-)", ":')", ':', ':^', '>:P',
                   ':-P', ':P', 'X-P', 'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)', '<3'}

# Sad Emoticons
emoticons_sad = {':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<', ':-[', ':-<', '=\\', '=/',
                 '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c', ':c', ':{', '>:\\', ';('}

# Emoji patterns
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
# combine sad and happy emoticons
emoticons = emoticons_happy.union(emoticons_sad)


def clean_tweets(tweet):
    # after tweepy preprocessing the colon symbol left remain after      #removing mentions
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
    tweet = re.sub(r'\'', '', tweet)
    tweet = re.sub(r'’', '', tweet)
    tweet = re.sub(r'\\"', '', tweet)
    tweet = re.sub(r'\.', '', tweet)
    tweet = re.sub(r'…', '', tweet)
    tweet = re.sub(r'\*', '', tweet)

    # replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+', ' ', tweet)

    # remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)
    # filter using NLTK library append it to a string
    filtered_tweet = []

    # looping through conditions
    word_tokens = word_tokenize(tweet)
    for w in word_tokens:
        # check tokens against stop words , emoticons and punctuations
        if w not in emoticons and w not in string.punctuation:
            filtered_tweet.append(w)
    return ' '.join(filtered_tweet)
    # print(word_tokens)
    # print(filtered_sentence)return tweet


p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.EMOJI, p.OPT.SMILEY, p.OPT.RESERVED)

for i in range(10000):
    print(data['text'][i])
    clean_data[i] = p.clean(data['text'][i])
    clean_data[i] = clean_tweets(clean_data[i])
    print(clean_data[i])
    # print("\n")
    # if i%10000==0:
    #     print("iteration {}".format(i))

clean_data.to_csv("data-sets/clean_fortnite_data.csv", index=False)