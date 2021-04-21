import statistics
import numpy as np
import time
from tqdm import tqdm
from telethon.tl.types import InputPeerChannel

class SimpleSubs:

    def __init__(self, telethon_api):
        self.telethon_api = telethon_api

    def rank(self, channels, query):
        ranked_channels = []
        for channel in tqdm(channels):
            num_messages = self.telethon_api.get_num_messages(channel)
            num_subs = self.telethon_api.get_channel_num_participants(channel)
            count_all_terms = 0
            for term in query:
                messages_object = self.telethon_api.search_query(channel, term)
                count_term =  messages_object.count
                count_all_terms += count_term
            # Calculate probabilities
            prob_query_channel = count_all_terms/num_messages
            prob_channel = np.log(10+num_subs)
            prob_channel_query = prob_query_channel * prob_channel
            # Add channel and score
            ranked_channels.append([channel, prob_channel_query])
        # Sort so that highest ranking channels are on top
        ranked_channels.sort(reverse=True, key=lambda tup: tup[1])
        # Calculate the average score
        num_channels = len(ranked_channels) if len(ranked_channels) else 1 # If there are no channels make it 1 to avoid division by zero
        avg_score = sum([ch[1] for ch in ranked_channels])/num_channels
        return ranked_channels, avg_score
                        
    def get_filtered_channels(self, channels, threshold):
        filtered_channels = [ch[0] for ch in channels if ch[1] > threshold]
        return filtered_channels