import xml.etree.ElementTree as ET
import requests


def REQ_GetArrivalAndDepartureTimesForTrip(tripID):
    xml = requests.post("http://216.252.195.248/webservices/bt4u_webservice.asmx/GetArrivalAndDepartureTimesForTrip", data={'tripID': tripID}).content
    root = ET.fromstring(xml)
    return root

def REQ_GetCurrentBusInfo():
    xml = requests.post("http://216.252.195.248/webservices/bt4u_webservice.asmx/GetCurrentBusInfo").content
    root = ET.fromstring(xml)
    return root

def REQ_GetCurrentRoutes(tripID):
    xml = requests.post("http://216.252.195.248/webservices/bt4u_webservice.asmx/GetCurrentRoutes").content
    root = ET.fromstring(xml)
    return root

def REQ_GetNextDepartures(routeShortName, stopCode):
    xml = requests.post("http://216.252.195.248/webservices/bt4u_webservice.asmx/GetNextDepartures", data={'routeShortName': routeShortName, 'stopCode': stopCode}).content
    root = ET.fromstring(xml)
    return root

def REQ_GetScheduledPatternPoints(patternName):
    xml = requests.post("http://216.252.195.248/webservices/bt4u_webservice.asmx/GetScheduledPatternPoints", data={'patternName': patternName}).content
    root = ET.fromstring(xml)
    return root

def REQ_GetScheduledRoutes(stopCode):
    xml = requests.post("http://216.252.195.248/webservices/bt4u_webservice.asmx/GetScheduledRoutes", data={'stopCode': stopCode}).content
    root = ET.fromstring(xml)
    return root

def REQ_GetScheduledStopCodes(stopCode):
    xml = requests.post("http://216.252.195.248/webservices/bt4u_webservice.asmx/GetScheduledStopCodes", data={'routeShortName': routeShortName}).content
    root = ET.fromstring(xml)
    return root

def REQ_GetScheduledStopNames(stopCode):
    xml = requests.post("http://216.252.195.248/webservices/bt4u_webservice.asmx/GetScheduledStopNames", data={'routeShortName': routeShortName}).content
    root = ET.fromstring(xml)
    return root

def REQ_GetSummary(stopCode):
    xml = requests.post("http://216.252.195.248/webservices/bt4u_webservice.asmx/GetSummary").content
    root = ET.fromstring(xml)
    return root

def GetNextDepartureTimesForRouteAndStopCode(routeShortName, stopCode, numTimesToReturn=3):
    results = []

    root = REQ_GetNextDepartures(routeShortName, stopCode)
    for child in root.iter('AdjustedDepartureTime'):
        results.append(child.text)

    sorted(results)

    return results[:numTimesToReturn]


def get_busses_for_stop_code(stopCode):
    root = REQ_GetScheduledRoutes(stopCode)

    results = []

    for child in root.iter('RouteShortName'):
        results.append(child.text)

    return results


def GetTimesForStopCode(stopCode):
    routes = get_busses_for_stop_code(stopCode)

    numTimesToReturn = 1

    if len(routes) <= 2:
        numTimesToReturn = 3

    times = []
    for route in routes:
        times.append( (route, GetNextDepartureTimesForRouteAndStopCode(route, stopCode, numTimesToReturn) ) )

    return times
