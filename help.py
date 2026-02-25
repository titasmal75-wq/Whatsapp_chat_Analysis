from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import emoji
from collections import Counter
def fetch_stats(selected_name , df):

    if selected_name != "Overall":

        df = df[df['user'] == selected_name]

        #fetch number of messages 

    num = df.shape[0]
        #number of word 

    word = []
    for message in df['message']:
        word.extend(message.split())


        # fetch number of media
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

        # fetch number of linked 
    
    link = []

    extract = URLExtract()

    for message in df['message']:
        link.extend(extract.find_urls(message))

    return num , len(word) , num_media , len(link)

# most active member

def most_active_member(df):

    x = df['user'].value_counts().head()

    df = round((df['user'].value_counts() / df.shape[0]) * 100 , 2).reset_index().rename(columns = {'index' : 'name' , 'user' : 'percent'})

    return x , df

#create wordcloude

def create_word_cloud(selected_name , df):

    if selected_name != 'Overall':
        df = df[df['user'] == selected_name]
    
    wc = WordCloud(width=500 , height= 500 , min_font_size= 20 , max_font_size= 100 , background_color= 'white')

    df_wc = wc.generate(df['message'].str.cat(sep = " "))

    return df_wc


#   Emoji

def emoji_helper(selected_user , df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emoji_list = []

    for message in df['message']:

        for char in message:

            if char in emoji.EMOJI_DATA:
                emoji_list.append(char)


    emoji_count = Counter(emoji_list)

    emoji_df = pd.DataFrame(emoji_count.most_common(),columns=['emoji', 'count'])
    
    return emoji_df


# activity timeline on basic month

def month_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + timeline['year'][i].astype(str))

    timeline['time'] = time

    return timeline


# activity timeline on bais date

def date_timeline(selected_name , df):
     
    if selected_name != 'Overall':
        df = df[df['user'] == selected_name]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


# Activity map

def weekly_activity(selected_name , df):
    if selected_name != 'Overall':
        df = df[df['user'] == selected_name]
    
    return df['day_name'].value_counts()

def monthly_activity(selected_name , df):

    if selected_name != 'Overall':
        df = df[df['user'] == selected_name]
    
    return df['month'].value_counts()

# activity Heatmap


def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
      
