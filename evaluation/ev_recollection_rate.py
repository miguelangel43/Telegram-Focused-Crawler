
class RecollectionRate:

    def __init__(self, telethon_api):
        self.telethon_api = telethon_api

    def evaluate(self, seed, collected_channels, num_iterations):
        num_recollected = 0
        # Remove the seed from the collected channels
        for ch in collected_channels:
            if ch in seed:
                collected_channels.remove(ch)
        iteration_channels = collected_channels

        # Crawl 
        for i in range(num_iterations):
            print('Iteration:', i+1, 'of', num_iterations)
            groups_and_edges = self.telethon_api.find_groups_fwd(collected_channels, iteration_channels)
            iteration_channels = groups_and_edges[0]
            collected_channels += iteration_channels
        
        # Calculate the num of recollected channels in all iterations except the last one
        for ch in collected_channels:
            if ch in seed:
                num_recollected += 1

        return num_recollected/len(seed)