import sqlite3, json, datetime


def create(fromTimestamp, toTimestamp, gmtOffset, database, group, locid):
    routinedvisitFile = open('output/data/routinedvisit.js', 'w')
    routinedvisitFile.write('var routinedvisitData = [')

    cur = database.cursor()
    routinedvisit = cur.execute("SELECT * \
                             FROM APOLLO \
                             WHERE Activity = 'Routined Location - Visit Entry' \
                             AND Key >= '{0}' AND Key <= '{1}' \
                             ORDER BY Key".format(fromTimestamp.strftime('%Y-%m-%d %H:%M:%S'),
                                                  toTimestamp.strftime('%Y-%m-%d %H:%M:%S')))

    # Prepare variables for iterating
    ident = locid
    output = ''
    # iterate over all returned rows
    print("Parsing routined visit data... ")
    for event in routinedvisit:

        ident += 1
        eventData = json.loads(event[2])

        start = datetime.datetime.strptime(eventData["VISIT ENTRY"], '%Y-%m-%d %H:%M:%S') + gmtOffset
        end   = datetime.datetime.strptime(eventData["VISIT EXIT"], '%Y-%m-%d %H:%M:%S') + gmtOffset

        startString = start.strftime('%Y-%m-%d %H:%M:%S')
        endString   = end.strftime('%Y-%m-%d %H:%M:%S')
        # Get coordinates
        lat = str(eventData["LATITUDE"])
        lon = str(eventData["LONGITUDE"])

        # Get metadata if present in event
        if eventData["DATA POINT COUNT"]:
            datapoints = eventData["DATA POINT COUNT"]
        if eventData["PLACE ID"]:
            placeid = eventData["PLACE ID"]
        if eventData["UNCERTAINTY"]:
            uncertainty = eventData["UNCERTAINTY"]
            if uncertainty < 25:
                color = "#4F674A"
            if uncertainty < 50 and uncertainty >= 25:
                color = "#7CA577"
            if uncertainty < 100 and uncertainty >= 50:
                color = "#E9DF40"
            if uncertainty < 250 and uncertainty >= 100:
                color = "#EFD75D"
            if uncertainty < 500 and uncertainty >= 250:
                color = "#EAA125"
            if uncertainty < 1000 and uncertainty >= 500:
                color = "#F3A742"
            if uncertainty < 1500 and uncertainty >= 1000:
                color = "#F36442"
            if uncertainty >= 1500:
                color = "F6876C"
        if eventData["DEVICE CLASS"]:
            deviceclass = eventData["DEVICE CLASS"]
        if eventData["DEVICE MODEL"]:
            devicemodel = eventData["DEVICE MODEL"]

        content= ""
        title = "<b>Routined Visit Location</b>" \
                "<br />{0}, {1}<br />{2} - {3}<br />" \
                "Uncertainty: {4}<br /> Device Class:{5}, Device Model: {6} <br />" \
                "Place ID: {7}" \
                .format(lat, lon, startString, endString, uncertainty, deviceclass, devicemodel, placeid)

        output += "{" +\
                  "id: {0}, " \
                  "start: '{1}', " \
                  "end: '{2}', " \
                  "group: {3}, " \
                  "content: '{4}', " \
                  "type: 'range', " \
                  "title: '{5}' ," \
                  "lat: {6}, " \
                  "lon: {7}, " \
                  .format(ident, startString, endString, group, content, title, lat, lon) \
                  + "},\n"

    routinedvisitFile.write(output[:-2] + "]")
    routinedvisitFile.close()
    return 0
