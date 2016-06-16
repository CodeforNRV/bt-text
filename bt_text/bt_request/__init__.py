import xml.etree.ElementTree as ET
import requests
import pudb

def __req_get_arrival_and_departure_times_for_trip(tripID):
    exception = None
    try:
        req = requests.post("http://216.252.195.248/webservices/bt4u_webservice.asmx/GetArrivalAndDepartureTimesForTrip", data={'tripID': tripID})
    except requests.exceptions.RequestException as e:
        exception = e

    if exception == None:
        content = req.content
        code = req.status_code
        root = ET.fromstring(req.content)
    else:
        code = None
        root = None
        content = None

    return {"status_code": code, "content": content, "xml": root, "exception": exception}

def __req_get_current_bus_info():
    exception = None
    try:
        req = requests.post("http://216.252.195.248/webservices/bt4u_webservice.asmx/GetCurrentBusInfo")
    except requests.exceptions.RequestException as e:
        exception = e

    if exception == None:
        content = req.content
        code = req.status_code
        root = ET.fromstring(req.content)
    else:
        code = None
        root = None
        content = None

    return {"status_code": code, "content": content, "xml": root, "exception": exception}

def __req_get_current_routes(tripID):
    exception = None
    try:
        req = requests.post("http://216.252.195.248/webservices/bt4u_webservice.asmx/GetCurrentRoutes")
    except requests.exceptions.RequestException as e:
        exception = e

    if exception == None:
        content = req.content
        code = req.status_code
        root = ET.fromstring(req.content)
    else:
        code = None
        root = None
        content = None

    return {"status_code": code, "content": content, "xml": root, "exception": exception}

def __req_get_next_departures(routeShortName, stopCode):
    exception = None
    try:
        req = requests.post("http://216.252.195.248/webservices/bt4u_webservice.asmx/GetNextDepartures", data={'routeShortName': routeShortName, 'stopCode': stopCode})
    except requests.exceptions.RequestException as e:
        exception = e

    if exception == None:
        content = req.content
        code = req.status_code
        root = ET.fromstring(req.content)
    else:
        code = None
        root = None
        content = None

    return {"status_code": code, "content": content, "xml": root, "exception": exception}

def __req_get_scheduled_pattern_points(patternName):
    exception = None
    try:
        req = requests.post("http://216.252.195.248/webservices/bt4u_webservice.asmx/GetScheduledPatternPoints", data={'patternName': patternName})
    except requests.exceptions.RequestException as e:
        exception = e

    if exception == None:
        content = req.content
        code = req.status_code
        root = ET.fromstring(req.content)
    else:
        code = None
        root = None
        content = None

    return {"status_code": code, "content": content, "xml": root, "exception": exception}

def __req_get_scheduled_routes(stopCode):
    exception = None
    try:
        req = requests.post("http://216.252.195.248/webservices/bt4u_webservice.asmx/GetScheduledRoutes", data={'stopCode': stopCode})
    except requests.exceptions.RequestException as e:
        exception = e

    if exception == None:
        content = req.content
        code = req.status_code
        root = ET.fromstring(req.content)
    else:
        code = None
        root = None
        content = None

    return {"status_code": code, "content": content, "xml": root, "exception": exception}

def __req_get_scheduled_stop_codes(stopCode):
    exception = None
    try:
        req = requests.post("http://216.252.195.248/webservices/bt4u_webservice.asmx/GetScheduledStopCodes", data={'routeShortName': routeShortName})
    except requests.exceptions.RequestException as e:
        exception = e

    if exception == None:
        content = req.content
        code = req.status_code
        root = ET.fromstring(req.content)
    else:
        code = None
        root = None
        content = None

    return {"status_code": code, "content": content, "xml": root, "exception": exception}

def __req_get_scheduled_stop_names(stopCode):
    exception = None
    try:
        req = requests.post("http://216.252.195.248/webservices/bt4u_webservice.asmx/GetScheduledStopNames", data={'routeShortName': routeShortName})
    except requests.exceptions.RequestException as e:
        exception = e

    if exception == None:
        content = req.content
        code = req.status_code
        root = ET.fromstring(req.content)
    else:
        code = None
        root = None
        content = None

    return {"status_code": code, "content": content, "xml": root, "exception": exception}

def __req_get_summary(stopCode):
    exception = None
    try:
        req = requests.post("http://216.252.195.248/webservices/bt4u_webservice.asmx/GetSummary")
    except requests.exceptions.RequestException as e:
        exception = e

    if exception == None:
        content = req.content
        code = req.status_code
        root = ET.fromstring(req.content)
    else:
        code = None
        root = None
        content = None

    return {"status_code": code, "content": content, "xml": root, "exception": exception}

def get_next_departure_times_for_route_and_stop_code(routeShortName, stopCode, numTimesToReturn=3):
    results = []

    resp = __req_get_next_departures(routeShortName, stopCode)
    success = True
    if resp["status_code"] != None and resp["status_code"] == 200:
        for child in resp["xml"].iter('AdjustedDepartureTime'):
            results.append(child.text)
        sorted(results)
    else:
        success = False

    return { "success": success, "status_code": resp["status_code"], "times": results[:numTimesToReturn]}

def get_buses_for_stop_code(stopCode):
    resp = __req_get_scheduled_routes(stopCode)

    route_short_names = []
    route_names = []

    # pudb.set_trace()

    success = True
    if resp["status_code"] != None and resp["status_code"] == 200:
        for child in resp["xml"].iter('RouteShortName'):
            route_short_names.append(child.text)
        for child in resp["xml"].iter('RouteName'):
            route_names.append(child.text)
    else:
        success = False

    return { "success": success, "status_code": resp["status_code"], "route_short_names": route_short_names, "route_names": route_names }


def get_times_for_stop_code(stopCode, requestShortNames):
    buses_resp = get_buses_for_stop_code(stopCode)

    times = []
    success = buses_resp["success"]
    if buses_resp["status_code"] != None and buses_resp["status_code"] == 200 and success == True:
        if requestShortNames == True:
            buses = buses_resp["route_short_names"]
        else:
            buses = buses_resp[route_names]

        numTimesToReturn = 1

        if len(buses) <= 2:
            numTimesToReturn = 3

        for route in buses:
            next_deps = get_next_departure_times_for_route_and_stop_code(route, stopCode, numTimesToReturn)

            if next_deps["status_code"] != None and next_deps["status_code"] == 200:
                times.append( (route, next_deps["times"] ) )
            else:
                success = False
                break
    else:
        success = False

    return { "success": success, "times": times }
