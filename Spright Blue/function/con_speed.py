# ================================================================
# IMPORT [json files]
import json

# IMPORT [speedtest -> Internet]
import speedtest #pip3 install speedtest-cli

# IMPORT [datetime -> calendar]
from datetime import datetime


logfile = "arq/ping.json"
isp = speedtest.Speedtest()
srv = isp.get_best_server()
latency = "{0:,.0f}".format(float(srv['latency']))
update = datetime.strftime(datetime.now(),'20%y-%m-%d %I:%M')

# ================================================================
dic_ping = {
    "LATENCY": int(latency),
    "UPDATE": update
}

json_object = json.dumps(dic_ping, indent=2)

DATA_JSON = ""
with open(logfile, 'w+') as file_json:
    file_json.write(json_object)

with open(logfile, 'r') as file_json:
    data = json.loads(file_json.read())
    DATA_JSON = data['LATENCY']
# ================================================================