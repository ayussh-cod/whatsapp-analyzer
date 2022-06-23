from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
extract=URLExtract()

def fetch_stats(selected_user,df):
    if(selected_user!='Overall'):
        df=df[df['users']==selected_user]
    num_messages = df.shape[0]
    words = []
    for messages in df['message']:
        words.extend(messages.split())
    media_count=0
    for media in words:
        if(media=='omitted'):
            media_count+=1
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_messages, len(words),media_count,len(links)


def most_busy_users(df):
    x = df['users'].value_counts().head()
    df=round((df['users'].value_counts()/df['users'].shape[0])*100,2).reset_index().rename(columns={'index':'name','users':'precent'})

    return x,df
def create_wordcloud(selected_user,df):
    if selected_user !='Overall':
        df=df[df['users']==selected_user]
    wc=WordCloud(width=500,height=500,background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc
def  emoji_helper(selected_user,df):
    if selected_user !='Overall':
        df=df[df['users']==selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
        emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
def monthly_timeline(selected_user,df):
    if selected_user !='Overall':
        df=df[df['users']==selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline
def daliy_Time_line(selected_user,df):
    if selected_user !='Overall':
        df=df[df['users']==selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline
def week_Activity_map(selected_user,df):
    if selected_user !='Overall':
        df=df[df['users']==selected_user]
    return df['day_name'].value_counts()
def month_activity_map(selected_user,df):
    if selected_user !='Overall':
        df=df[df['users']==selected_user]
    return df['month'].value_counts()
def activity_heatmap(selected_user,df):
    if selected_user !='Overall':
        df=df[df['users']==selected_user]
    activy_df=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return activy_df










