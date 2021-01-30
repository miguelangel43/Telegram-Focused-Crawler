import time
import csv 
import json
from tqdm import tqdm
import numpy as np

from telegram import SyncTelegramClient
from list_groups import channels
from model import Message, Channel

telethon_api = SyncTelegramClient()


def ingest_channel(channel_name: str, channel_id: int, stop_point: int = None):

    BATCH_SIZE = 100
    current_message_id = None

    # Fetch messages
    messages = telethon_api.fetch_messages(
        channel=channel_name,
        size=BATCH_SIZE,
        max_id=current_message_id,
    )

    # Store messages
    for m in messages:
        message_channel_id = m.to_id.channel_id
        message_id = m.id
        # If a msg was forwarded from another channel, add it to the list
        if m.fwd_from:
            if hasattr(m.fwd_from.from_id ,'channel_id'):
                #print(telethon_api.get_channel_info(m.fwd_from.from_id.channel_id)["chats"][0]["username"])
                new_groups.add(int(m.fwd_from.from_id.channel_id))
                new_edges.add((int(channel_id),int(m.fwd_from.from_id.channel_id)))

        msg = Message(
            record_id=(message_channel_id << 32) + message_id,
            message_id=message_id,
            channel_id=m.to_id.channel_id,
            retrieved_utc=int(time.time()),
            updated_utc=int(time.time()),
            data=m.to_json()
            )

        with open('messages.csv', 'a') as f:
            w = csv.writer(f)
            w.writerow((msg.record_id, msg.channel_id, msg.message_id, msg.data))

# Adds the input channel info to table Channel
def add_channel(channel_name: str, channel_id: int, channel_data):
    ch_data = json.dumps(channel_data) 
    with open('channel.csv', 'a') as f:
        w = csv.writer(f)
        w.writerow((channel_id, ch_data))


if __name__ == "__main__":
    # messages.csv header
    with open('messages.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(('record_id', 'channel_id', 'message_id', 'data'))   

    # channel.csv header
    with open('channel.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(('channel_id', 'ch_data'))

    new_groups = set()
    new_edges = set()

    for channel in tqdm(channels):

        channel_data = telethon_api.get_channel_info(channel)
        channel_id = channel_data["full_chat"]["id"]
        channel_name = channel_data["chats"][0]["username"]
        # print(channel_name)

        add_channel(channel, channel_id, channel_data)
        ingest_channel(channel, channel_id)


    print("Number of groups: ", len(new_groups))
    print("Number of edges: ", len(new_edges))

    cw_groups = csv.writer(open("new_groups.csv",'w'))
    cw_groups.writerow(list(new_groups))
    cw_edges = csv.writer(open("new_edges.csv", "w"))
    cw_edges.writerow(list(new_edges))

    # with open('new_groups.txt', 'w') as f:
    #     for item in new_groups:
    #         f.write("%s\n" % item)

    # with open('new_edges.txt', 'w') as f:
    #     for item in new_edges:
    #         f.write("%s\n" % item)