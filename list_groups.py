import csv
from telegram import SyncTelegramClient

telethon_api = SyncTelegramClient()
# The groups querdenken341, 36, 351, 366, 515, 6051  don't exist

# Admins in some groups need to accept me in the group in order for me to 
# write messages. I still have access to all the messages and media posted. 
# 441

channel_ids = [1242023007, 1483513669, 1493488074, 1401905477, 1491403279, 1450867165, 1360165831, 1305215986, 1292782129, 1199810152, 1267231752, 1177709684, 1487349751, 1246299608, 1492522272, 1434237539, 1165697042, 1325676349, 1170658711, 1121191471, 1493241558, 1403417647, 1258368994, 1161395503, 1088907893, 1495035777, 1494607443, 1387264853, 1259128287, 1154006990, 1183691613, 1459389378, 1286953722, 1219958281, 1473564705, 1408963731, 1317024626, 1470503570, 1172331372, 1258613756, 1332226443, 1304926302, 1288304737, 1448890226, 1458097215, 1206773549, 1270967153, 1347607127, 1453973886, 1228499058, 1466519068, 1111678723, 1464169151, 1234280957, 1437293191, 1313237034, 1486928183, 1392105989, 1310120179, 1321465958, 1325060422]

channels = [
'querdenken203',
'querdenken231',
'querdenken221',
'querdenken251',
'querdenken215',
'querdenken284',
'querdenken212',
'querdenken228',
'querdenken238',
'querdenken241',
'querdenken242',
'querdenken234',
'querdenken211',
'querdenken30',
'querdenken391',
'querdenken34',
'querdenken33',
'querdenken37',
'querdenken_39MeckUm',
#'querdenken_39MD',
'querdenken35',
'querdenken38',
'querdenken399',
'querdenken361',
'querdenken40',
'querdenken441',
'querdenken482',
'querdenken413',
'querdenken571',
'querdenken521',
'querdenken561',
'querdenken591',
'querdenken53',
'querdenken615',
'querdenken621',
'querdenken631',
'querdenken6201',
'querdenken69',
'querdenken611',
'querdenken731',
'querdenken793',
'querdenken7071',
'querdenken713',
'querdenken795',
'querdenken7141',
'querdenken7261',
'querdenken761',
'querdenken751',
'querdenken7192',
#'querdenken775',
'querdenken753',
'querdenken773',
'querdenken718',
'querdenken7551',
'querdenken721',
'querdenken871',
#'querdenken874',
#'querdenken89',
'querdenken8041',
'querdenken861',
'querdenken841',
#'querdenken865',
'querdenken8341',
'querdenken9371',
'querdenken911',
'BewegungLeipzig'
]

group_ids = [telethon_api.get_channel_info(channel)["full_chat"]["id"] for channel in channels]

cw_groups = csv.writer(open("old_groups.csv",'w'))
cw_groups.writerow(group_ids)

