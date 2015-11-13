from flask import Flask, json, render_template, request

# User story:
# Start with a person standing at a stop. All they know is the stop #, and the
# text number for bt_text. From this, they should be able to text bt_text, and
# list of route codes that are for that stop #. If they reply with a combination
# of route code and stop #, they get the next 5 times the bust will be at that
# stop.
#
# Another feature would let someone request the next five times and routes that
# will be at that stop code regardless of route. 

#from pudb import set_trace; set_trace()


def create_app():

    this_app = Flask(__name__)
    this_app.app_name = "bt_text"

    with open(os.environ.get('BTT_CONFIG'), 'r') as f:
        this_app.json_config = json.load(f)

    return this_app

app = create_app()



@app.route('/')
def index():
    return 'Hello World!'



