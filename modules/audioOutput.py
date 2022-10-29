import datetime
import json


def create(fromTimestamp, toTimestamp, database, group):
    audioOutputFile = open('output/data/audioOutput.js', 'w', encoding="utf-8")
    audioOutputFile.write('var audiooutputData = [')

    cur = database.cursor()
    audioOutput = cur.execute("SELECT * \
                             FROM APOLLO \
                             WHERE Activity = 'Audio Output' \
                             AND Key >= '{0}' AND Key <= '{1}' \
                             ORDER BY Key".format(fromTimestamp.strftime('%Y-%m-%d %H:%M:%S'),
                                                  toTimestamp.strftime('%Y-%m-%d %H:%M:%S')))

    # Initialise array for coloring occurances of an output device in the same color
    colors = ["#004e64", "#00a5cf", "#9fffcb", "#25a18e", "#7ae582"]

    # Initialize variables for iterating
    portDict = {}
    output = ''
    counter = 0
    print("Parsing audio output data... ")
    for event in audioOutput:
        eventData = json.loads(event[2])

        portName = eventData["AUDIO PORT NAME"]

        if portName not in portDict.keys():
            portDict[portName] = colors[counter % len(colors) - 1]
            counter += 1
        color = portDict[portName]

        timezone = datetime.timedelta(hours=eventData["GMT OFFSET"])
        start = datetime.datetime.strptime(eventData["START"], '%Y-%m-%d %H:%M:%S') + timezone
        end = datetime.datetime.strptime(eventData["END"], '%Y-%m-%d %H:%M:%S') + timezone

        startString = start.strftime('%Y-%m-%d %H:%M:%S')
        endString = end.strftime('%Y-%m-%d %H:%M:%S')

        title = "<b>Audio Output</b><br />{0} - {1} <br />{2} <br />".format(startString, endString, portName)
        if eventData["AUDIO IDENTIFIER"]:
            title += "Audio Identifier: " + str(eventData["AUDIO IDENTIFIER"]) + "<br>"
        if eventData["AUDIO PORT TYPE"]:
            title += "Audio Port Type: " + str(eventData["AUDIO PORT TYPE"]) + "<br>"
        if eventData["ROUTE CHANGE REASON"]:
            title += "Route Change Reason: " + str(eventData["ROUTE CHANGE REASON"]) + "<br>"

        output += "{" + \
                    "start: '{0}', " \
                    "end: '{1}', " \
                    "group:{2}, " \
                    "content: '{3}', " \
                    "style: 'background-color:{4}', " \
                    "title: '{5}'" \
                  .format(startString, endString, group, portName, color, title) \
              + "},\n"

    audioOutputFile.write(output[:-2] + "]")
    audioOutputFile.close()
    return 0
