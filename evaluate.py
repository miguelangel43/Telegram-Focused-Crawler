import random
import csv
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

# Read the collected channels and the seed
with open('collected_channels.csv') as f:
    reader = csv.reader(f)
    collected_channels = list(reader)
collected_channels = list(map(int, collected_channels[0]))
with open('seed.csv') as f:
    reader = csv.reader(f)
    seed = list(reader)
seed = list(map(int, seed[0]))
# Remove the seed from the collected channels
for ch in collected_channels:
    if ch in seed:
        collected_channels.remove(ch)

# Get 10 random samples of 1% or 2% of the collected channels
percentage = 3
k = len(collected_channels) * percentage // 100
samples = []
for i in range(10):
    samples.append([int(collected_channels[i]) for i in random.sample(range(len(collected_channels)), k)])

# Perform evaluation on every sample
result = []
for sample in samples:
    percentage_recollected = evaluation_strat.evaluate(seed, sample,num_iterations=2)
    result.append(percentage_recollected)
    print(percentage_recollected)

print(result)