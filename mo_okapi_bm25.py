from rank_bm25 import BM25Okapi
from tqdm import tqdm

# df = pd.read_csv('groups.csv')
# df = df.loc[(df['consp'] == 1.0) & (df['eng'] != 1.0)]
# df = df.drop(columns = ['consp', 'eng'])
# df.reset_index(inplace=True)

class OkapiBM25:
# Returns the Okapi BM25 score of a channel given a query
    def __init__(self, telethon_api):
        self.telethon_api = telethon_api

    def get_bm25_score(self, query, channel):
        channel_data = self.telethon_api.get_channel_info(channel)
        messages = self.telethon_api.fetch_messages(
        channel=channel,
        size= 5000,
        max_id= None
        )
        corpus = []
        for m in messages:
            try:
                corpus.append(m.message.lower().split())
            except:
                pass
        bm25 = BM25Okapi(corpus)
        msg_scores = bm25.get_scores(query)
        return sum(msg_scores)

    def rank(self, channels, query):
        ranked_channels = []
        for channel in tqdm(channels):
            try:
                ranked_channels.append([channel, self.get_bm25_score(query, channel)])
            except:
                print(channel, 'was not found')
                pass
        return ranked_channels

    def get_filtered_channels(self, channels):
        return [ch[0] for ch in channels if ch[1] > 0.05]