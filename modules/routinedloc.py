import sqlite3, json, datetime

def create(fromTimestamp, toTimestamp, gmtOffset, database, group):
    routinedlocFile = open('output/data/routinedloc.js', 'w')
    routinedlocFile.write('var routinedlocData = [')

    cur = database.cursor()
    rountinedloc = cur.execute("SELECT * \
                             FROM APOLLO \
                             WHERE Activity = 'Routined Location' \
                             AND Key >= '{0}' AND Key <= '{1}' \
                             ORDER BY Key".format(fromTimestamp.strftime('%Y-%m-%d %H:%M:%S'),
                                                  toTimestamp.strftime('%Y-%m-%d %H:%M:%S')))

    # Prepare variables for iterating
    ident = 0
    output = ''
    # iterate over all returned rows
    print("Parsing routined location data... ")
    for event in rountinedloc:

        ident += 1
        eventData = json.loads(event[2])

        start = datetime.datetime.strptime(eventData["TIMESTAMP"], '%Y-%m-%d %H:%M:%S') + gmtOffset
        startString = start.strftime('%Y-%m-%d %H:%M:%S')

        # Get coordinates
        lat = str(eventData["LATITUDE"])
        lon = str(eventData["LONGITUDE"])

        # Get metadata if present in event
        horizontalacc, speed, course, color = '', '', '', '#000000'
        if "HORIZONTAL ACCURACY" in eventData.keys():
            horizontalacc = eventData["HORIZONTAL ACCURACY"]
            if horizontalacc < 25:
                color = "#4F674A"
            if horizontalacc < 50 and horizontalacc >= 25:
                color = "#7CA577"
            if horizontalacc < 100 and horizontalacc >= 50:
                color = "#E9DF40"
            if horizontalacc < 250 and horizontalacc >= 100:
                color = "#EFD75D"
            if horizontalacc < 500 and horizontalacc >= 250:
                color = "#EAA125"
            if horizontalacc < 1000 and horizontalacc >= 500:
                color = "#F3A742"
            if horizontalacc < 1500 and horizontalacc >= 1000:
                color = "#F36442"
            if horizontalacc >= 1500:
                color = "F6876C"
        if "SPEED (KMPH)" in eventData.keys():
            if eventData["SPEED (KMPH)"] != "-3.6":
                speed = eventData["SPEED (KMPH)"]
        if "COURSE" in eventData.keys():
            if eventData["COURSE"] != "-1.0":
                course = eventData["COURSE"]

        content= ""
        title = "<b>Routined Cache Location</b><br />{0}, {1}<br />{2}<br />" \
                "<span style=\"color:{3}\">Horizontal Accuracy: {4}</span><br />" \
                "Speed (km/h): {5}<br />" \
                "Course: {6}<br />"\
                .format(lat, lon, startString, color, horizontalacc, speed, course)

        output += "{" +\
                  "id: {0}, " \
                  "start: '{1}', " \
                  "group:{2}, " \
                  "content: '{3}', " \
                  "type: 'point', " \
                  "title: '{4}' ," \
                  "lat: {5}, " \
                  "lon: {6}, " \
                  "style: \"color:{7}\"" \
                  .format(ident, startString, group, content, title, lat, lon, color) \
                  + "},\n"

    routinedlocFile.write(output[:-2] + "]")
    routinedlocFile.close()
    return ident
