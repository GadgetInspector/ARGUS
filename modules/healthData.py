import sqlite3, json, datetime


def create(fromTimestamp, toTimestamp, gmtOffset, database):
    # Prepare output file
    healthsdFile = open('output/data/health_stepsdistance.js', 'w')
    healthsdFile.write('var stepsdistance = [')

    cur = database.cursor()
    healthsd = cur.execute("SELECT * \
                             FROM APOLLO \
                             WHERE (Activity = 'Health Steps' OR \
                                   Activity = 'Health Distance') \
                             AND (Key >= '{0}' AND Key <= '{1}') \
                             ORDER BY Key".format(fromTimestamp.strftime('%Y-%m-%d %H:%M:%S'),
                                                  toTimestamp.strftime('%Y-%m-%d %H:%M:%S')))

    output = ""
    print("Parsing health data... ")
    for event in healthsd:
        eventData = json.loads(event[2])

        start = datetime.datetime.strptime(eventData["START DATE"], '%Y-%m-%d %H:%M:%S') + gmtOffset
        end = datetime.datetime.strptime(eventData["END DATE"], '%Y-%m-%d %H:%M:%S') + gmtOffset
        delta = end - start

        # Colour short intervals differently, as they are more precise but hold smaller values to make them stand out
        group = 1 if delta.seconds > 60 else 0

        startString = start.strftime('%Y-%m-%d %H:%M:%S')
        endString = end.strftime('%Y-%m-%d %H:%M:%S')
        if event[1] == "Health Steps":
            title = "{content:\"" + "{0} - {1} <br /> {2} Steps".format(startString, endString, eventData["STEPS"]) + "\"}"
            output += "{" + \
                      "x: '{0}', " \
                      "end: '{1}', " \
                      "y: {2}, " \
                      "group:{3}, " \
                      "label: {4}" \
                      .format(startString, endString, eventData["STEPS"], group, title) \
                      + "},\n"
    healthsdFile.write(output[:-2] + "]")
    healthsdFile.close()
    return 0
