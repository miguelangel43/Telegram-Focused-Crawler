import random
import csv
from tqdm import tqdm
from telegram import SyncTelegramClient 
from evaluation.ev_recollection_rate import RecollectionRate

# TODO:
"""
1. Read seed used when executing crawler.py
2. Read the collected_channels 
3. Remove the seed from the collected channels
4. Get 10 random samples of 1% or 2% of the collected channels
5. Perform evaluation on them
6. Plot how the rate of seed recollection changes with the size of the sample
"""

telethon_api = SyncTelegramClient()
evaluation_strat = RecollectionRate(telethon_api)

NUM_ITERATIONS = 1

# Read the collected channels and the seed
with open('collected_channels_simple.csv') as f:
    reader = csv.reader(f)
    collected_channels = list(reader)
collected_channels = list(map(int, collected_channels[0]))
with open('seed_simple.csv') as f:
    reader = csv.reader(f)
    seed = list(reader)
seed = list(map(int, seed[0]))
# Remove the seed from the collected channels
for ch in collected_channels:
    if ch in seed:
        collected_channels.remove(ch)

# Get 10 random samples of 1% or 2% of the collected channels
percentage = 1
k = len(collected_channels) * percentage // 100
print('Getting 10 random samples of', percentage, 'percent of the population.', k, 'channels out of', len(collected_channels))
samples = []
for i in range(10):
    random_sample = [int(collected_channels[i]) for i in random.sample(range(len(collected_channels)), k)]
    samples.append(random_sample)
# Perform evaluation on every sample
result = []
for i, sample in enumerate(samples):
    print('Sample', i+1, 'out of', len(samples))
    percentage_recollected = evaluation_strat.evaluate(seed=seed, collected_channels=sample,num_iterations=NUM_ITERATIONS)
    result.append(percentage_recollected)
    print(percentage_recollected)

print(result)
with open('simple_evaluation_2.csv', 'w') as f:
    w = csv.writer(f)
    w.writerow(result)