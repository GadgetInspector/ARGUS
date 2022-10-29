import sqlite3, json, datetime
def create(fromTimestamp, toTimestamp, database, group):
    backlightFile = open('output/data/pluggedIn.js', 'w')
    backlightFile.write('var pluggedInData = [')

    cur = database.cursor()
    backlight = cur.execute("SELECT * \
                             FROM APOLLO \
                             WHERE Activity = 'Device Plugin Status' \
                             AND Key >= '{0}' AND Key <= '{1}' \
                             ORDER BY Key".format(fromTimestamp.strftime('%Y-%m-%d %H:%M:%S'),
                                                  toTimestamp.strftime('%Y-%m-%d %H:%M:%S')))

    output = ''
    # iterate over all returned rows
    print("Parsing plugged in state data... ")
    for event in backlight:
        eventData = json.loads(event[2])

        timezone = datetime.timedelta(hours=eventData["GMT OFFSET"])
        start = datetime.datetime.strptime(eventData["START"], '%Y-%m-%d %H:%M:%S') + timezone
        end = datetime.datetime.strptime(eventData["END"], '%Y-%m-%d %H:%M:%S') + timezone

        if eventData["IS PLUGGED IN"] == "PLUGGED IN":
            status = "Yes"
            color = "#9c4c46"
        else:
            status = "No"
            color = "#827a79"

        startString = start.strftime('%Y-%m-%d %H:%M:%S')
        endString = end.strftime('%Y-%m-%d %H:%M:%S')
        title = "<b>Plugged In State</b><br />{0}<br />{1} - {2}<br />".format(status, startString, endString)
        output += "{" + \
                  "start: '{0}', " \
                  "end: '{1}', " \
                  "group:{2}, " \
                  "content: '{3}', " \
                  "style: 'background-color:{4}', " \
                  "title: '{5}'" \
                      .format(startString, endString, group, status, color, title) \
                  + "},\n"

    backlightFile.write(output[:-2] + "]")
    backlightFile.close()
    return 0
