
class RecollectionRate:

    def __init__(self, telethon_api):
        self.telethon_api = telethon_api

    def evaluate(self, seed, collected_channels, num_iterations):
        num_recollected = 0
        print(len(collected_channels))
        for ch in collected_channels:
            if ch in seed:
                collected_channels.remove(ch)
        print(len(collected_channels))
        print('seed', seed)
        print('collected_channels', collected_channels)
        iteration_channels = collected_channels
        for i in range(num_iterations):
            print('Iteration:', i+1, 'of', num_iterations)
            groups_and_edges = self.telethon_api.find_groups_fwd(collected_channels, iteration_channels)
            iteration_channels = groups_and_edges[0]
            collected_channels += iteration_channels
        
        for ch in collected_channels:
            if ch in seed:
                num_recollected += 1
        return num_recollected/len(seed)