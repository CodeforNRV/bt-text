from flask import Flask, json, request
import os
import bt_text.bt_request as bt_api
import pudb

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


@app.route('/')
def index():
    reply = "Welcome to the BT Text/Phone API"
    return reply


@app.route('/sms', methods=['GET', 'POST'])
def handle_text():

    data = request.form['Body']
    rt_code = int(data)
    times = bt_api.get_times_for_stop_code(stopCode=rt_code, requestShortNames=True)

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
                    <Say voice="woman">Thanks for calling Blacksburg transit. Please enter the bus stop code and then press star.</Say>
                </Gather>
                <Gather timeout="15" finishOnKey="*" action="/voice" method="POST">
                    <Say voice="woman">Please enter the bus stop code and then press star.</Say>
                </Gather>
                <Say voice="woman">We're sorry, we didn't receive any input. Goodbye!</Say>
            </Response>
            """
    return reply

@app.route('/voice', methods=['POST'])
def handle_voice_input():

    data = request.form['Body']
    rt_code = int(data)
    times = bt_api.get_times_for_stop_code(stopCode=rt_code, requestShortNames=False)

    message = "The next bus arrival times are: "
    for stop in times['times']:
        for time in stop[1]:
            dt = time.split()
            ft = dt[1][:-3]
            message += "{name} at {time}{apm};".format(name=stop[0],time=ft, apm=dt[2].lower())

    reply = """<?xml version="1.0" encoding="UTF-8" ?>
            <Response>
                <Say voice="woman">{content}. Thank you, goodbye!</Say>
            </Response>
            """.format(content=message)
    return reply
