import math
import numpy as np
import time
from tqdm import tqdm
from telethon.tl.types import InputPeerChannel
from telethon.errors.rpcerrorlist import ChannelPrivateError

class BalogViews:

    def __init__(self, telethon_api):
        self.telethon_api = telethon_api

    def rank(self, channels, query):
        ranked_channels = []
        for channel in tqdm(channels):
            try:
                num_messages = self.telethon_api.get_num_messages(channel)
                num_subs = self.telethon_api.get_channel_num_participants(channel)
                prob_query_posts = 0 # P(q|post)
                for term in query:
                    messages_object = self.telethon_api.search_query(channel, term)
                    # Get all the messages where the term of the query appears
                    messages = messages_object.messages
                    for m in messages:
                        # Transform the message string in a list of words
                        m_as_list = m.message.split()
                        num_t_post = 0
                        num_all_terms_post = len(m_as_list)
                        if num_all_terms_post == 0:
                            break
                        for word in m_as_list:
                            if term in word.lower():
                                num_t_post += 1
                        prob_query_posts += num_t_post/num_all_terms_post
                # Calculate probabilities
                prob_query_channel = prob_query_posts/num_messages
                prob_channel = self.telethon_api.get_avg_view_count(channel)/num_subs
                prob_channel_query = prob_query_channel * prob_channel
                # Add channel with score
                ranked_channels.append([channel, prob_query_channel])
            except ChannelPrivateError:
                pass
            except ZeroDivisionError:
                pass
        # Sort so that highest ranking channels are on top
        ranked_channels.sort(reverse=True, key=lambda tup: tup[1])
        # Calculate the average score
        num_channels = len(ranked_channels) if len(ranked_channels) else 1 # If there are no channels make it 1 to avoid division by zero
        avg_score = sum([ch[1] for ch in ranked_channels])/num_channels
        return ranked_channels, avg_score
                        
    def get_filtered_channels(self, channels, threshold):
        filtered_channels = [ch[0] for ch in channels if ch[1] > threshold]
        return filtered_channels