from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import nltk
nltk.download('vader_lexicon',quiet=True)
from nltk.sentiment import SentimentIntensityAnalyzer

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    # fetch number of messages
    num_messages = df.shape[0]

    # fetch total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] =='<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))



    return num_messages, len(words), num_media_messages, len(links)

# Most busiest users
def most_busy_users(df):

    x = df['user'].value_counts().head()

    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percent'})

    return x, df


#WORDCLOUD
def create_wordcloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # nested function to check stop words
    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=''))
    return df_wc

# MOST COMMON WORDS
def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

# EMOJI ANALYSIS
def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


# MONTHLY TIMELINE
def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month', 'month_num']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    # creating a new column in "timeline" df
    timeline['time'] = time

    return timeline

# DAILY TIMELINE
def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('timeline_date').count()['message'].reset_index()

    return daily_timeline


# ACTIVITY MAP
def week_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts() ##This will return a series

def month_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts() ##This will return a series


# HEATMAP
def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap


# Sentiment analysis of each user based on the text and emojis used



def analyze_sentiment(selected_user, df):
    sia = SentimentIntensityAnalyzer()
    user_sentiments = {}

    for index, row in df.iterrows():
        user = row['user']
        message = row['message']

        if user not in user_sentiments:
            user_sentiments[user] = {'compound': 0.0, 'pos': 0.0, 'neu': 0.0, 'neg': 0.0}

        # Analyze text sentiment
        text_sentiment = sia.polarity_scores(message)
        for key in user_sentiments[user].keys():
            user_sentiments[user][key] += text_sentiment[key]

        # Analyze emoji sentiment
        emojis = [c for c in message if emoji.demojize(c) != c]
        for emo in emojis:
            emoji_sentiment = {
                '😀': 1.0,  # Positive sentiment
                '😢': -1.0,  # Negative sentiment
                '😠': -1.0,  # Negative sentiment
                '😍': 1.0,  # Positive sentiment
                '😐': 0.0,  # Neutral sentiment
            }
            if emo in emoji_sentiment:
                user_sentiments[user]['compound'] += emoji_sentiment[emo]

    # Average the sentiment scores
    for user, sentiment_scores in user_sentiments.items():
        total_messages = df[df['user'] == user].shape[0]
        for key in sentiment_scores.keys():
            sentiment_scores[key] /= total_messages

    if selected_user == 'Overall':
        return user_sentiments
    else:
        return {
            selected_user: user_sentiments.get(selected_user, {'compound': 0.0, 'pos': 0.0, 'neu': 0.0, 'neg': 0.0})}


def sentiment_score(user_sentiments, selected_user):
    if selected_user == 'Overall':
        pos = sum([user['pos'] for user in user_sentiments.values()]) / len(user_sentiments)
        neg = sum([user['neg'] for user in user_sentiments.values()]) / len(user_sentiments)
        neu = sum([user['neu'] for user in user_sentiments.values()]) / len(user_sentiments)
    elif selected_user in user_sentiments:
        sentiment_scores = user_sentiments[selected_user]
        pos = sentiment_scores['pos']
        neg = sentiment_scores['neg']
        neu = sentiment_scores['neu']
    else:
        return "No sentiment analysis results for the selected user"

    if (pos > neg) and (pos > neu):
        return "Positive 😊"
    elif (neg > pos) and (neg > neu):
        return "Negative 😠"
    else:
        return "Neutral 🙂"




