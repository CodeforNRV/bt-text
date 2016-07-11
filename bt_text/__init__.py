from flask import Flask, json, request
import os
import bt_text.bt_request as bt_api
import pudb
import re

# User story:
# Sends stop code, gets next times for the stop. If there are fewer than 3
# routes, return each with the next 3 stop times. If there 3 ore more, send
# just the next stop time for each route time.

# First query API for a list of current routes (short names)
# Next, build a dictionary with the short names as the keys, lists of stop
# codes s the values.
# Then figure out which routes, match our user provided stop code.
# If there are 3 or more routes that match, return the next stop time for each
# if there are 1 or 2 routes that match, return the next 3 stop times for each


# Sends stop code and route code, returns next 5 arrival times


def create_app():

    this_app = Flask(__name__)
    this_app.app_name = "bt_text"

    return this_app

app = create_app()

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    #response = jsonify(error.to_dict())
    #response.status_code = error.status_code
    #return response
    reply = """<?xml version="1.0" encoding="UTF-8" ?>
            <Response>
            {content}
            </Response>""".format(content=error.message)
    return reply

@app.route('/')
def index():
    reply = "Welcome to the BT Text/Phone API"
    return reply


def parse_rt_stop(data):
    args = re.findall(r"[\w']+", data)
    print args
    if len(args) == 1:
        rt_code = None
        stop_code = int(args[0])
    if len(args) == 2:
        try:
            stop_code = int(args[0])
            rt_code = args[1]
        except:
            stop_code = int(args[1])
            rt_code = args[0]

    return rt_code, stop_code


@app.route('/sms', methods=['POST'])
def handle_text():
    try:
        data = request.form['Body']
        print "parsing:", data
        rt_code, stop_code = parse_rt_stop(data)
    except:
        raise InvalidUsage('<Message>Invalid stop number, please try again.</Message>')

    if rt_code:
        times = bt_api.get_next_departure_times_for_route_and_stop_code(routeShortName=rt_code, stopCode=stop_code)

        #times for route and stop code version doesn't have rt code embeded in it, so modify
        times['times'] = [(rt_code.upper(), [t]) for t in times['times']]
    else:
        times = bt_api.get_times_for_stop_code(stopCode=stop_code, requestShortNames=True)
    
    if times['success'] == False:
        raise InvalidUsage("""
            <Message>We're sorry, there was a problem retrieving stop times, please try again later.</Message>
        """)
    elif times['success'] == "Invalid":
        raise InvalidUsage("""
            <Message>That appears to be an invalid stop number, please try again.</Message>
        """)
    if times['times'] is None:
        raise InvalidUsage("""
            <Message>There are no current bus times for that stop number.</Message>
        """)

    message = ""
    
    for stop in times['times']:

        for time in stop[1]:
            dt = time.split()
            ft = dt[1][:-3]
            message += "{name} @ {time}{apm};\n".format(name=stop[0],time=ft, apm=dt[2].lower())

    reply = """<?xml version="1.0" encoding="UTF-8" ?>
            <Response>
            <Message>{content}</Message>
            </Response>""".format(content=message)
    return reply

@app.route('/voice', methods=['GET'])
def handle_voice_call():

    reply = """<?xml version="1.0" encoding="UTF-8" ?>
            <Response>
                <Gather timeout="15" finishOnKey="*" action="/voice" method="POST">
                    <Say>Thanks for calling Blacksburg transit. Please enter the bus stop code and then press star.</Say>
                </Gather>
                <Gather timeout="15" finishOnKey="*" action="/voice" method="POST">
                    <Say>Please enter the bus stop code and then press star.</Say>
                </Gather>
                <Say>We're sorry, we didn't receive any input. Goodbye!</Say>
            </Response>
            """
    return reply

@app.route('/voice', methods=['POST'])
def handle_voice_input():
    try:
        data = request.form['Digits']
        rt_code = int(data)
    except:
        raise InvalidUsage("""
            <Gather timeout="15" finishOnKey="*" action="/voice" method="POST">
                <Say>Not a valid stop number, please try again.</Say>
            </Gather>
            <Gather timeout="15" finishOnKey="*" action="/voice" method="POST">
                <Say>Please enter the bus stop code and then press star.</Say>
            </Gather>
            <Say>We're sorry, we didn't receive any input. Goodbye!</Say>
            """)
    times = bt_api.get_times_for_stop_code(stopCode=rt_code, requestShortNames=False)
    
    if times['success'] is False:
        raise InvalidUsage("""
            <Say>We're sorry, there was a problem retrieving stop times, please try again later.</Say>
        """)
    elif times['success'] == "Invalid":
        raise InvalidUsage("""
            <Gather timeout="15" finishOnKey="*" action="/voice" method="POST">
                <Say>That appears to be an invalid stop number, please enter the stop number followed by the star key.</Say>
            </Gather>
            <Say>We're sorry, we didn't receive any input. Goodbye!</Say>
        """)
    if times['times'] is None:
        raise InvalidUsage("""
            <Say>There are no current bus times for that stop number. Goodbye!</Say>
        """)

    message = "The next bus arrival times are: "
    for stop in times['times']:
        for time in stop[1]:
            dt = time.split()
            ft = dt[1][:-3]
            message += "{name} at {time}{apm};".format(name=stop[0],time=ft, apm=dt[2].lower())

    reply = """<?xml version="1.0" encoding="UTF-8" ?>
            <Response>
                <Say>{content}. Thank you, goodbye!</Say>
            </Response>
            """.format(content=message)
    return reply
