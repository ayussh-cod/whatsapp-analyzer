import pandas as pd
import re
def preprocess(data):
    pattern = '\[\d{1,2}\/\d{1,2}\/\d{1,2}\,\s\d{1,2}\:\d{1,2}\:\d{1,2}\]\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    user_message = messages
    message_date = dates
    df = pd.Series(message_date)
    df1 = pd.Series(user_message)
    df1.to_frame()
    df.to_frame()
    df = pd.to_datetime(df, format='[%d/%m/%y, %H:%M:%S] ')
    df = pd.concat([df, df1], axis=1)
    df.rename(columns={0: 'date', 1: 'user_message'}, inplace=True)
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['message'] = messages
    df.drop('user_message', axis=1, inplace=True)
    df['month'] = df['date'].dt.month_name()
    df['month_num']=df['date'].dt.month
    df['only_date']=df['date'].dt.date
    df['day_name']=df['date'].dt.day_name()
    df['year'] = df['date'].dt.year
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    period = []
    for i in df[['day_name', 'hour']]['hour']:
        if i == 23:
            period.append(str(i) + "-" + str('00'))
        elif i == 0:
            period.append(str('00') + "-" + str(i + 1))
        else:
            period.append(str(i) + "-" + str(i + 1))
    df['period'] = period
    return df