from telegram import SyncTelegramClient
from list_groups import channels
import psycopg2

telethon_api = SyncTelegramClient()


# Connect to the db
con = psycopg2.connect(
	host = "localhost",
	database = "dbcollection",
	user = "postgres",
	password = "thesis2021",
	port = "5432"
	)

# Cursor
cur = con.cursor()


cur.execute(
	"SELECT * FROM message"
	)

out = cur.fetchall()

for x in out:
	print(x[2]['message'])
	
# print(out[0][2]['message'])

# Close the connection
con.close()