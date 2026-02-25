import re
import pandas as pd


def processor(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s*[ap]m\s-\s'
    message = re.split(pattern, data)
    messages = message[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({
        'user_message': messages,
        'message_date': dates
    })

    df['message_date'] = pd.to_datetime(
        df['message_date'],
        format='%d/%m/%Y, %I:%M %p - '
    )
    users = []
    messages_clean = []

    for msg in df['user_message']:
        entry_mess = re.split(r'([^:]+):\s', msg)

        if len(entry_mess) > 1:
            users.append(entry_mess[1])
            messages_clean.append(entry_mess[2])
        else:
            users.append('group_notification')
            messages_clean.append(entry_mess[0])

    df['user'] = users
    df['message'] = messages_clean

    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['month_num'] = df['message_date'].dt.month
    df['only_date'] = df['message_date'].dt.date
    df['day_name'] = df['message_date'].dt.day_name()
    df['dates'] = df['message_date'].dt.day
    df['hours'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute


    period = []
    for hour in df[['day_name' , 'hours']]['hours']:
        if hour == 23 :
            period.append(str(hour) + str("-00"))
        elif hour == 0:
            period.append(f"00-{hour+1}") 
        else:
             period.append(f"{hour}-{hour+1}")
    df['period'] = period
        

    return df