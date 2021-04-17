import pandas as pd
import datetime
import random
import csv
from tqdm import tqdm
from telegram import SyncTelegramClient 
from evaluation.ev_recollection_rate import RecollectionRate


"""
1. Read seed used when executing crawler.py
2. Read the collected_channels 
3. Remove the seed from the collected channels
4. Get 10 random samples of 1% or 2% of the collected channels
5. Perform evaluation on them
6. Save all the data in a csv file
"""

telethon_api = SyncTelegramClient()
evaluation_strat = RecollectionRate(telethon_api)

NUM_ITERATIONS = 1
PERCENTAGE = 2
NUM_SAMPLES = 10
BATCH_SIZE = 1000
SEED_FILE = 'seed.csv'
COLLECTED_CHANNELS_FILE = 'collected_channels.csv'
MODEL = 'Simple'

# Read the collected channels and the seed
with open(COLLECTED_CHANNELS_FILE) as f:
    reader = csv.reader(f)
    collected_channels = list(reader)
collected_channels = list(map(int, collected_channels[0]))

# with open(SEED_FILE) as f:
#     reader = csv.reader(f)
#     seed = list(reader)
# seed = list(map(int, seed[0]))
seed = pd.read_csv('groups.csv')
seed = seed.loc[(seed['consp'] == 1.0) & (seed['eng'] != 1.0)]
seed = seed.drop(columns = ['consp', 'eng'])
seed.reset_index(inplace=True)
seed = seed['ch_id'].tolist()[:20]

# Remove the seed from the collected channels
for ch in collected_channels:
    if ch in seed:
        collected_channels.remove(ch)

# Get 10 random samples of 1% or 2% of the collected channels
percentage = PERCENTAGE
num_total_groups = len(collected_channels)
k = len(collected_channels) * percentage // 100
print('Getting', NUM_SAMPLES, 'random samples of', percentage, 'percent of the population.', k, 'channels out of', num_total_groups)
samples = []
for i in range(NUM_SAMPLES):
    random_sample = [int(collected_channels[i]) for i in random.sample(range(len(collected_channels)), k)]
    samples.append(random_sample)
# Perform evaluation on every sample
result = []
for i, sample in enumerate(samples):
    print('Sample', i+1, 'out of', len(samples))
    percentage_recollected = evaluation_strat.evaluate(seed=seed, collected_channels=sample,num_iterations=NUM_ITERATIONS, batch_size=BATCH_SIZE)
    result.append(percentage_recollected)
    print(percentage_recollected)

print(result)
avg_score = None
if result:
    avg_score = sum(result)/len(result)
    print('Average score:', sum(result)/len(result))

# To be run only the first time, s.t. we create the file
# with open('rate_of_recollection.csv', mode='w') as f:
#     writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     writer.writerow(['Date', 'Model', 'Percentage', 'Average Score', 'Scores', 'Number of groups',
#     'Total number of groups', 'Number of samples', 'Number of iterations', 'Batch size'])

# Save the data in the csv file
with open('rate_of_recollection.csv', mode='a') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow([datetime.datetime.now(), MODEL, PERCENTAGE,  avg_score, result, k, 
    num_total_groups, NUM_SAMPLES, NUM_ITERATIONS, BATCH_SIZE])

