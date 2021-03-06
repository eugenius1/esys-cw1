import string
import os
import json

import paho.mqtt.client as mqtt
from bottle import route, run, template, static_file

debug = True

if debug:
    broker_ip = '127.0.0.1'
else:
    broker_ip = '192.168.0.10'

mqtt_topic = "esys/GreenRhino/geiger"

# keys of Geiger JSON object with data
data_keys = ['count_per_minute', 'random_number']

password_length = 20
# number of possible password characters is 64, a power of 2
password_chars = string.ascii_letters + string.digits + '!@'
password_chars_count = len(password_chars)

global message_list
message_list = []

data_agg = {}
# Data aggregator - a dictionary of lists
# the key is the name from data_keys
# newer data is appended to the end of the list

global random_password
random_password = ''

def random_password_character(choice):
    choice = int(choice)
    print('choosing char #', choice)
    return password_chars[choice % password_chars_count]

# path for static files like images
@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static')

@route('/')
def geiger_view():
    recent = {}
    for k in data_keys:
        if k in data_agg:
            recent[k] = data_agg[k][-1]

    if len(recent) != len(data_keys):
        recent = dict.fromkeys(data_keys)

    recent['random_password'] = random_password
    print(recent)

    # graph_data = [25, 19, 20, 31, 16, 15, 12]
    graph_data = data_agg.get('count_per_minute', [])
    graph_data_str = json.dumps(graph_data)
    graph_labels_str ='[' + (', ' * (len(graph_data)-1)) + ']'


    return template('''
<!DOCTYPE html>
<html lang="en">
<head>
<title>CrptoKey | Green Rhino</title>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
</head>
<body>
<br>
<div class="container col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
<div class="jumbotron">
<div class="container" style="font-size:21px">
    <div class="row"><img class="img-responsive" src="/static/crypto-key.png"></div>
    <p class="row">
        <span class="col-sm-4"><strong>Random number</strong>: </span>
        <span class="col-sm-8">{{random_number}}</span>
    </p>
    <p class="row">
        <span class="col-sm-4"><strong>Random password</strong>: </span>
        <span class="col-sm-8"><code>{{random_password}}</code></span>
    </p>
    <p class="row">
        <span class="col-sm-4"><strong>Current radioactivity</strong>: </span>
        <span class="col-sm-8">{{count_per_minute}} CPM <small>(counts per minute)</small></span>
    </p>
    <div class="row"><canvas id="radioactivity-chart" width="400" height="400"></canvas></div>
</div>
</div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js"></script>
<script>
if({{do_chart}}){
    var ctx = document.getElementById("radioactivity-chart");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: {{graph_labels}},
            datasets: [{
                label: 'Radioactivity over time',
                fill: false,
                lineTension: 0.1,
                backgroundColor: "rgba(75,192,192,0.4)",
                borderColor: "rgba(75,192,192,1)",
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: "rgba(75,192,192,1)",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgba(75,192,192,1)",
                pointHoverBorderColor: "rgba(220,220,220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: {{graph_data}},
                spanGaps: false,
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
}
</script>
</body>
</html>
        ''', **recent, do_chart='true', 
        graph_labels=graph_labels_str,
        graph_data = graph_data_str)


# callbacks for MQTT actions
def on_connect(client, userdata, flags, rc):
    print('Connected!')

def on_log(client, userdata, level, buf):
    print("log: ",buf)

def on_message(client, userdata, message):
    global msg

    # message comes as a byte string, 
    # convert to Python string, and then to a dictionary
    msg = json.loads(message.payload.decode("utf-8"))
    print('Received <{raw}>, storing as {typ}'.format(typ=type(msg), raw=message.payload))
    message_list.append(msg)
    print('Stored messages count:', len(message_list))
    
    process_new_message(msg)

def process_new_message(message):
    if not isinstance(message, dict):
        print('got {} instead of dict'.format(type(message)))
    try:
        # aggregate data from this message into data_agg,
        # which is a dictionary of lists
        for key in data_keys:
            value = message['Geiger'][key]
            if key not in data_agg:
                data_agg[key] = [value]
            else:
                data_agg[key].append(value)

        random_num = data_agg['random_number'][-1]
        global random_password
        random_password = random_password_character(random_num) + random_password
        if len(random_password) >= password_length:
            random_password = random_password[:password_length]

    except KeyError as e:
        print('derp! missing some key')
        print(e)


mclient = mqtt.Client()

# Attach callback functions
mclient.on_connect = on_connect
mclient.on_message = on_message
mclient.on_log = on_log

# Connect to broker
mclient.connect(broker_ip)

# start the MQQT subscribe loop
mclient.loop_start()
mclient.subscribe(mqtt_topic)

run(host='localhost', port=8080, reloader=True)
# blocking function call above, so the loop_stop below never runs

mclient.loop_stop()
