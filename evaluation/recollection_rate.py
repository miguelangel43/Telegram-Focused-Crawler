
class RecollectionRate:

    def __init__(self, telethon_api):
        self.telethon_api = telethon_api

    def evaluate(self, seed, collected_channels, num_iterations, batch_size):
        num_recollected = 0
        iteration_channels = list(collected_channels)
        # Crawl 
        for i in range(num_iterations):
            print('Iteration:', i+1, 'of', num_iterations)
            iteration_channels, x = self.telethon_api.find_groups_fwd(collected_channels, iteration_channels, batch_size=batch_size)
            collected_channels += iteration_channels
        # Calculate the num of recollected channels in all iterations except the last one
        for ch in collected_channels:
            if ch in seed:
                num_recollected += 1

        return num_recollected/len(seed)