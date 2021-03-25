import json
from telethon.errors import ChatAdminRequiredError
from telethon.sync import TelegramClient
from telethon.tl import functions
from tqdm import tqdm
import time
import math

# Telegram API keys
api_id = 1812168
api_hash = '57d99f51542be90739730033e553b7e8'

class SyncTelegramClient:
    def __init__(self):
        self._client = TelegramClient("session", api_id, api_hash)

    def fetch_messages(self, channel, size=100, max_id=None, min_id=None):
        """Method to fetch messages from a specific channel / group"""

        params = [channel, size]
        kwargs = {}

        # The telethon module has issues if a keyword passed is None, so we will add the keyword
        # only if it is not None
        for key in ['max_id', 'min_id']:
            if locals()[key] is not None:
                kwargs[key] = locals()[key]

        with self._client as client:
            data = client.get_messages(*params, **kwargs)

        return data

    def get_channel_info(self, channel):
        with self._client as client:
            data = client(functions.channels.GetFullChannelRequest(channel=channel)).to_json()
        return json.loads(data)

    def get_channel_users(self, channel, limit=1000):
        """method to get participants from channel (we might not have privileges to get this data)
        getting some errors about permissions"""
        with self._client as client:
            try:
                participants = client.get_participants(channel, limit)
            except ChatAdminRequiredError as e:
                # TODO: ???
                raise e

        return participants

    # Returns the channel name given the id as input
    def get_channel_name(self, channel_data):
        # channel_id = 1242023007
        channel_name = channel_data["chats"][0]["username"]
        return channel_name

    def get_channel_id(self, channel_name):
        # channel_name = 'ATTILA HILDMANN OFFICIAL ⚫️⚪️🔴⚔️'
        return self.get_channel_info(str(channel_name))["full_chat"]["id"]

    def get_channel_num_participants(self, channel_data):
        return channel_data["full_chat"]["participants_count"]

    # Tries to join th channels/groups in the list that it takes as input
    def join_channels(self, new_groups):
        for group in new_groups:
            print("joining ", self.get_channel_info(group)["chats"][0]["username"])
            try:
                self._client.invoke(JoinChannelRequest(group))
            except:
                print("failed")

    """ This function does not work in Ipython """
    def find_groups_fwd(self, visited_channels, old_groups, batch_size=500):
        """Finds forwarded messages in old_groups and returns the channels those messages were sent from along with the edges.
        Args:
            visited_channels: all channels visited so far, to avoid visiting them again.
            old_groups: channels that are going to be searched for forwards. They are either the seed (in the first iteration)
                or the collected channels from the previous iteration.
        Returns:
            new_groups: the channels whose messages were forwarded to old_groups.
            new_edges: a list of lists [[ch_destination ,ch_origin]]. This means that a message was forwarded from
                ch_origin to ch_destination.
        """
        new_groups = []
        new_edges = []
        for group in tqdm(old_groups):
            # Fetch the last BATCH_SIZE messages
            try:
                channel_data = self.get_channel_info(group)
                messages = self.fetch_messages(
                channel=group,
                size=batch_size,
                max_id= None
                )
                for m in messages:
                    # If a msg was forwarded from another channel, append it to the list
                    if m.fwd_from:
                        if hasattr(m.fwd_from ,'from_id'):
                            if hasattr(m.fwd_from.from_id, 'channel_id'):
                                new_edges.append([group, m.fwd_from.from_id.channel_id])
                                if m.fwd_from.from_id.channel_id not in new_groups:
                                    if m.fwd_from.from_id.channel_id not in visited_channels:
                                        new_groups.append(m.fwd_from.from_id.channel_id)
            # The channel contains less messages than BATCH_SIZE
            except BufferError:
                print('The channel contains less messages than BATCH_SIZE')
            # except:
            #     print(group, ' error')
            #     time.sleep(1) 
            #     pass              
        return new_groups, new_edges