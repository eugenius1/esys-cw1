from bottle import route, run, template, static_file
import paho.mqtt.client as mqtt
import json

# broker_ip = '127.0.0.1'
broker_ip = '192.168.0.10'
mqtt_topic = "esys/GreenRhino/geiger"

data_keys = ['count_per_minute', 'random_number']

@route('/hello/<name>')
def hello(name='World'):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static')

@route('/')
def geiger_view():
    recent = {}
    for k in data_keys:
        if k in data_agg:
            recent[k] = data_agg[k][-1]

    print(recent)

    if len(recent) != len(data_keys):
        recent = dict.fromkeys(data_keys)

    print(recent)
    recent['random_password'] = 'pUR3!y?r4nd0M-noT@1MPL3meNt3d_yEt'

    return template('''
<!DOCTYPE html>
<html lang="en">
<head>
<title>Green Rhino</title>
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
        <span class="col-sm-4"><strong>Radioactivity</strong>: </span>
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
            labels: ["", "", "", "", "", "", ""],
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
                data: [25, 19, 20, 31, 16, 15, 12],
                spanGaps: false,
            }]
        },
    });
}
</script>
</body>
</html>
        ''', **recent, do_chart='true')


global message_list
message_list = []
data_agg = {}

def process_new_message(message):
    if not isinstance(message, dict):
        print('got {} instead of dict'.format(type(message)))
    try:
        for key in data_keys:
            value = message['Geiger'][key]
            if key not in data_agg:
                data_agg[key] = [value]
            else:
                data_agg[key].append(value)
    except KeyError as e:
        print('derp! missing some key')
        print(e)

def on_message(client, userdata, message):
    global msg
    msg = json.loads(message.payload.decode("utf-8"))
    print('Received <{raw}>, storing as {typ}'.format(typ=type(msg), raw=message.payload))
    message_list.append(msg)
    print('Stored messages count:', len(message_list))
    process_new_message(msg)

def on_connect(client, userdata, flags, rc):
    print('Connected!')

def on_log(client, userdata, level, buf):
    print("log: ",buf)

mclient = mqtt.Client()
mclient.on_connect = on_connect
mclient.on_message = on_message
mclient.on_log = on_log

mclient.connect(broker_ip)

mclient.loop_start()    #start the loop
mclient.subscribe(mqtt_topic)
# time.sleep(5)
# mclient.loop_stop()

run(host='localhost', port=8080, reloader=True)

mclient.loop_stop()
# mclient.loop_forever()
