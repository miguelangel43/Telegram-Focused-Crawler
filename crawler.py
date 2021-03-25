from tqdm import tqdm
import csv
import time
import pandas as pd

from telegram import SyncTelegramClient 

# Import the crawling and the evaluation strategies
from models.mo_balog1 import Balog1
from evaluation.ev_recollection_rate import RecollectionRate

# Instanciate the crawling and the evaluation strategies
telethon_api = SyncTelegramClient()
model = Balog1(telethon_api)
evaluation = RecollectionRate(telethon_api)

""" 
    Visited channels: all channels that have already analyzed. It's importat to keep track of them so that we don't analyze them again.
    Seed: we begin iteration 0 with them. We also use them as an evaluation metric in the rate of original seed recollection.
    Collected channels: seed + all the new channels that we deem to have CT content.
    Iteration channels: channels found in the iteration. The ones that we deem to have CT content will be added to the seed.

"""

BATCH_SIZE = 100 # Number of messages that will be collected to search for mentions
NUM_ITERATIONS = 5
QUERY = ['covid-19', 'corona']

# Reading the seed groups
seed = pd.read_csv('groups.csv')
seed = seed.loc[(seed['consp'] == 1.0) & (seed['eng'] != 1.0)]
seed = seed.drop(columns = ['consp', 'eng'])
seed.reset_index(inplace=True)
seed = seed['ch_name'].tolist()

#original_seed = ['1444228991']

seed = seed
visited_channels = seed
collected_channels = seed
iteration_channels = seed # The output channels in iteration i will be the input channels of iteration i+1

for i in range(NUM_ITERATIONS):
    print('Iteration:', i)
    # Find groups given original seed or new channels
    print('Finding new channels..')
    groups_and_edges = telethon_api.find_groups_fwd(visited_channels=visited_channels, old_groups = iteration_channels, batch_size=BATCH_SIZE)
    visited_channels += groups_and_edges[0]
    print('FOUND CHANNELS:', groups_and_edges[0])
    # Rank the groups based on a QUERY
    print('Ranking channels..')
    ranked_channels = model.rank(groups_and_edges[0], QUERY)
    print('RANKED CHANNELS:', ranked_channels)
    # Add the highest ranked channels (to 10%, 20%, 30%? or the channels with a rank coefficient higher than a threshold) to the seed.
    print('Adding highest ranked channels to seed...')
    iteration_channels = groups_and_edges[0]
    new_channels = model.get_filtered_channels(ranked_channels)
    print('NEW CHANNELS:', new_channels)
    print(len(iteration_channels), 'new channels added')
    collected_channels += new_channels

# Evaluation
print('Evaluating..')
print('Rate of seed recollection:', evaluation.evaluate(seed, iteration_channels, num_iterations=2)*100, '%')
# 0% using all the groups as orginal seed for 2 iterations.