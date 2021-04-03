import math
import statistics
import numpy as np
import time
from tqdm import tqdm
from telethon.tl.types import InputPeerChannel

class Balog2:

    def __init__(self, telethon_api):
        self.telethon_api = telethon_api

    def rank(self, channels, query):
        for channel in tqdm(channels):
            for term in query:
                # Get all the messages where the term of the query appears
                messages = self.telethon_api.search_query(channel, term).messages
                prob_term_posts = [] # P(t|post)
                for m in messages:
                    if isinstance(m.message, str):
                        #TODO: Check how many times the query occurs in the message 
                        # (character-wise. e.g. if query is 'covid-19', 'covid-19-impfung' also counts)
                        
                 
    def get_filtered_channels(self, channels):
        #TODO
        return [ch[0] for ch in channels if ch[1] > 0.0001]