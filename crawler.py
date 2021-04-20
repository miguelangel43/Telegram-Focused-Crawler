from tqdm import tqdm
import csv
import time
import pandas as pd
import datetime

from telegram import SyncTelegramClient 

# Import the crawling and the evaluation strategies
from models.balog import Balog
from models.simple import Simple
from models.simple_subs import SimpleSubs
from models.simple_views import SimpleViews
from models.balog_subs import BalogSubs
from models.balog_views import BalogViews

# Instanciate the crawling and the evaluation strategies
telethon_api = SyncTelegramClient()

model_name = 'Simple_subs' # For the log
model = BalogSubs(telethon_api)

""" 
    Visited channels: all channels that have already analyzed. It's importat to keep track of them so that we don't analyze them again.
    Seed: we begin iteration 0 with them. We also use them as an evaluation metric in the rate of original seed recollection.
    Collected channels: seed + all the new channels that we deem to have CT content.
    Iteration channels: channels found in the iteration. The ones that we deem to have CT content will be added to the seed.

"""

BATCH_SIZE = 1000 # Number of messages that will be collected to search for mentions
NUM_ITERATIONS = 2
QUERY = ['corona', 'covid', 'qanon', 'querdenk', 'giftspritz', 'impf'] # With this query words like 'coronavirus' or 'covid-19' will also count
THRESHOLD_IN_PERCENTAGE = 0.75

# Reading the seed groups
seed_input = pd.read_csv('groups.csv')
seed_input = seed_input.loc[(seed_input['consp'] == 1.0) & (seed_input['eng'] != 1.0)]
seed_input = seed_input.drop(columns = ['consp', 'eng'])
seed_input.reset_index(inplace=True)
seed_input = seed_input['ch_id'].tolist()[:20]

# Initializing variables
seed = list(seed_input)
visited_channels = list(seed_input)
collected_channels = list(seed_input)
iteration_channels = list(seed_input) # The output channels in iteration i will be the input channels of iteration i+1

# Initializing csv file. To be run only the first time, s.t. the csv file is created with the proper column names
# with open('crawls.csv', mode='w') as f:
#     writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     writer.writerow(['Date', 'Crawler', 'Retrieved messages per group', 'Iteration', 'Total Iterations', 'Seed size', 'Query', 'Threshold',
#     'Threshold percentage', 'Average Score', 'Seed', 'Collected channels', 'Ranked channels', 'Iteration channels'])

print('Ranking seed channels..')
ranked_seed, seed_score = model.rank(seed, QUERY)
threshold = THRESHOLD_IN_PERCENTAGE * seed_score
print('Seed scores:', seed_score)
print(threshold, 'will be used as threshold')

for i in range(NUM_ITERATIONS):
    print('Iteration:', i)
    # Find groups given original seed or new channels
    print('Finding new channels..')
    found_channels = telethon_api.find_groups_fwd(visited_channels=visited_channels, old_groups = iteration_channels, batch_size=BATCH_SIZE)
    visited_channels.extend(found_channels) 
    # Rank the groups based on a QUERY
    print('Ranking channels..')
    ranked_channels, avg_score = model.rank(found_channels, QUERY)
    # Add the highest ranked channels to the seed.
    print('Adding highest ranked channels to seed...') 
    iteration_channels = model.get_filtered_channels(ranked_channels, threshold)
    if len(found_channels):
        print(len(iteration_channels), 'new channels added,', int(len(iteration_channels)/len(found_channels)*100), '%', 'of channels')
    else:
        print('No new channels added')
    print('Average score:', avg_score)
    collected_channels.extend(iteration_channels)
    # Save the data in the csv file
    with open('crawls.csv', mode='a') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([datetime.datetime.now(), model_name, BATCH_SIZE, i+1, NUM_ITERATIONS, len(seed), QUERY, threshold, 
        THRESHOLD_IN_PERCENTAGE, avg_score, seed, collected_channels, ranked_channels, iteration_channels])

# # Save the collected channels and the seed in a csv file
with open('collected_channels.csv', 'w') as f:
    w = csv.writer(f)
    w.writerow(collected_channels)
with open('seed.csv', 'w') as f:
    w = csv.writer(f)
    w.writerow(seed)