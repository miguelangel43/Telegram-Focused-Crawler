import math
import statistics
import numpy as np
import time
from tqdm import tqdm

""" With the objective of finding P(ch|q), we find P(ch) and P(t|ch), which is composed of P(t|post) and P(post|ch) """
class Balog1:

    def __init__(self, telethon_api):
        self.telethon_api = telethon_api

    # Function to find out the probability of a channel for balog1 and balog2
    """ get P(ch) """
    def get_p_ch(self, vers, channel):
        # Uniform probability where all channels are assumed to be equally relevant
        if vers == 1:
            return 1
        # Subscriber-based prior probability where channels with higher subscriber count are assumed to be more relevant
        elif vers == 2:
            channel_data = self.telethon_api.get_channel_info(channel)
            num_participants = self.telethon_api.get_channel_num_participants(channel_data)
            return math.log(10 + num_participants)
        # View count-based probability based on the mean of the view count the last 100 msgs 
        elif vers == 3:
            channel_data = self.telethon_api.get_channel_info(channel)
            messages = self.telethon_api.fetch_messages(
            channel=channel,
            size=100,
            max_id= None
            )
            view_count = []
            for m in messages:
                try:
                    view_count.append(int(m.views))
                except:
                    time.sleep(1)
                    pass
            print(view_count)
            return statistics.mean(view_count)
        else: 
            return print('incorrect version number')

    """ get P(t|ch) """ # TODO: Now it only works for a one word query, make it work for a multiple word query
    def get_p_t_ch(self, query, channel):
        channel_data = self.telethon_api.get_channel_info(channel)
        messages = self.telethon_api.fetch_messages(
        channel=channel,
        size=1000,
        max_id= None
        )
        query = query.lower()
        num_messages = len(messages)
        """ P(t|post) """
        p_t_post = [] 
        i = 0
        for m in messages:
            if isinstance(m.message, str):
                list_words = m.message.lower().split()
                num_query = list_words.count(query)
                p_t_post.append(float(num_query/(len(list_words)+1)))
        """ P(t|ch) """
        p_t_ch = 0
        """ P(post|ch) """
        p_post_ch = 1/num_messages
        for e in p_t_post:
            if e:
                p_t_ch += e * p_post_ch
        return p_t_ch

    def rank(self, channels, query):
        ranked_channels = []
        for channel in tqdm(channels):
            """ P(ch|q) """
            try:
                # Get P(q|ch) by multiplying all the P(t|ch) for every term t in the query. Eq 3.
                p_q_ch = []
                for q in query:
                    p_q_ch.append(self.get_p_t_ch(q, channel))
                    # print(channel, q, self.get_p_t_ch(q, channel))
                # p_q_ch = sum([self.get_p_t_ch(q, channel) for q in query])
                p_q_ch = sum(p_q_ch) # On the paper this is prod, but since I have not done smoothing, prod would smt result in 0
                ranked_channels.append([channel, p_q_ch * self.get_p_ch(2, channel)])
                #print(ranked_channels[-1])
            except:
                print(channel, ' was not found')
        ranked_channels.sort(reverse=True, key=lambda tup: tup[1])
        return ranked_channels
    
    def get_filtered_channels(self, channels):
        return [ch[0] for ch in channels if ch[1] > 0]

# True Positives: 74
# True Negatives: 55
# False Positives: 17
# False Negatives: 6

# ~85% accuracy