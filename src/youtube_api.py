
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pickle
from google.auth.transport.requests import Request
import pandas as pd
from datetime import date

def read_cred():
    #reading from a .txt file that contains scopes and client secret from google for developers
    info_file = open('youtube_data.txt', 'r')
    scope = info_file.readline().rstrip()
    cs = info_file.readline().rstrip()
    info_file.close()
    return scope,cs

def get_youtube_service(scopes,client_secret,cred_files):
    credentials = None
    if os.path.exists(cred_files):
        with open(cred_files, 'rb') as token:
            credentials = pickle.load(token)


    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret, scopes)
            credentials = flow.run_local_server(port=0)

        with open(cred_files, 'wb') as token:
            pickle.dump(credentials, token)
    service = build("youtube", "v3", credentials=credentials)
    return service

def get_subscriptions(service):
    request = service.subscriptions().list(
        part='snippet,contentDetails',
        mine=True,
        maxResults=50
    )
    response = request.execute()
    sub_dict = {'title': [], 'id': [], 'view_count': [], 'sub_count': [], 'video_count': [], 'topics': []}


    for item in response.get('items', []):
        snippet = item.get('snippet', {})
        resource_id = snippet.get('resourceId', {})

        sub_dict['title'].append(snippet.get('title'))
        sub_dict['id'].append(resource_id.get('channelId'))

    return sub_dict
def get_stats(sub_dict, youtube):
    sub_list = sub_dict['id']
    for i in sub_list:  # for every channelId
        requests = youtube.channels().list(
            part="statistics,topicDetails",
            id=i,
            maxResults=20
        )
        response = requests.execute()
        items = response.get('items', [])
        if items:
            stats = items[0].get('statistics', {})
            topics = items[0].get('topicDetails', {})
            topic_urls = topics.get('topicCategories', [])
            topic_names = []
            for url in topic_urls:
                topic_name = url.split('/')[-1]
                topic_names.append(topic_name)

            sub_dict['topics'].append(topic_names)
            sub_dict['view_count'].append(stats.get('viewCount'))
            sub_dict['sub_count'].append(stats.get('subscriberCount'))
            sub_dict['video_count'].append(stats.get('videoCount'))


    df_subs = pd.DataFrame(sub_dict)
    df_subs['date'] = date.today()

    return df_subs
def calculate_new_subscribers(df_subs,csv_file):
    # If previous data exists, calculate the new subscribers
    if os.path.exists(csv_file):
        prev_df = pd.read_csv(csv_file)
        merged_df = pd.merge(df_subs, prev_df[['id', 'sub_count']], on='id', how='left', suffixes=('', '_prev'))
        merged_df['new_subscribers'] = merged_df['sub_count'].astype(float) - merged_df['sub_count_prev'].fillna(0).astype(float)
        merged_df.loc[merged_df['sub_count_prev'].isnull(),'new_subscribers']=0
    else:
        merged_df = df_subs.copy()
        merged_df['new_subscribers'] = 0

    return merged_df

def new_views(df_subs,csv_file):
    # If previous data exists, calculate the new views
    if os.path.exists(csv_file):
        prev_df = pd.read_csv(csv_file)
        df = pd.merge(df_subs, prev_df[['id', 'view_count']], on='id', how='left', suffixes=('', '_prev'))
        df['new_views'] = df['view_count'].astype(float) - df['view_count_prev'].fillna(0).astype(float)
        df.loc[df['view_count_prev'].isnull(),'new_views']=0
    else:
        df = df_subs.copy()
        df['new_views'] = 0

    return df



def main():
    scopes,client_secret=read_cred()
    cred_files = "youtube_credentials.pickle"
    csv_file = 'youtube_api.csv'
    youtube = get_youtube_service(scopes,client_secret,cred_files)
    sub_dict = get_subscriptions(youtube)
    df_subs = get_stats(sub_dict, youtube)
    df_merged=calculate_new_subscribers(df_subs,csv_file)
    final_df=new_views(df_merged,csv_file)
    final_df=final_df.drop_duplicates(subset=['title','date'])


    if os.path.exists(csv_file):
        final_df.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        final_df.to_csv(csv_file, index=False)



main()