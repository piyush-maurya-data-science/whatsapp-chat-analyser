import re
import pandas as pd

def preprocess(data):
    pattern = r"\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2} ?(?:am|pm)\s-\s"
    cleaned_data = data.replace("\u202f", " ")
    messages = re.split(pattern, cleaned_data)[1:]
    dates = re.findall(pattern, cleaned_data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert 'message_date' to datetime

    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)


    ##
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['timeline_date'] = df['date'].dt.date #DAILY TIMELINE
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month #MONTHLY TIMELINE
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name() #ACTIVITY MAP
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute


    # HEATMAP
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period


    return df