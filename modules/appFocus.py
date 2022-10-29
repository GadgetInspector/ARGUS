import sqlite3, json, datetime


def create(fromTimestamp, toTimestamp, database, group):
    # Prepare output file
    appfocusFile = open('output/data/appinFocus.js', 'w', encoding="utf-8")
    appfocusFile.write('var appfocusData = [')

    # Read bundle id to app name translation file
    bundlefile = open('bundlenames.json', 'r').read()
    bundletranslation = json.loads(bundlefile)

    cur = database.cursor()
    appFocus = cur.execute("SELECT * \
                             FROM APOLLO \
                             WHERE Activity = 'Application In Focus' \
                             AND Key >= '{0}' AND Key <= '{1}' \
                             ORDER BY Key".format(fromTimestamp.strftime('%Y-%m-%d %H:%M:%S'),
                                                  toTimestamp.strftime('%Y-%m-%d %H:%M:%S')))

    # Initialise array for coloring occurances of an app in the same color
    colors = ['#f94144', '#f3722c', '#f8961e', '#f9844a', '#f9c74f',
              '#90be6d', '#43aa8b', '#4d908e', '#577590', '#277da1']

    # Initialize variables for iterating
    output = ''
    counter = 0
    bundleDict = {}
    print("Parsing app focus data... ")
    for event in appFocus:
        eventData = json.loads(event[2])  # Load data about the event
        bundle = eventData["BUNDLE ID"]
        if bundle not in bundleDict.keys():
            bundleDict[bundle] = colors[counter % len(colors) - 1] # Assign color to an app the first time it occurs
            counter += 1
        color = bundleDict[bundle]

        if bundle in bundletranslation.keys():  # Search bundle id in translation file to show app name
            appname = bundletranslation[bundle]
        else:
            appname = bundle

        # Ignore WebKit.GPU as it holds almost no info but crowds the visualisation
        if bundle == 'com.apple.WebKit.GPU':
            continue

        timezone = datetime.timedelta(hours=eventData["GMT OFFSET"])
        start = datetime.datetime.strptime(eventData["START"], '%Y-%m-%d %H:%M:%S') + timezone
        end = datetime.datetime.strptime(eventData["END"], '%Y-%m-%d %H:%M:%S') + timezone

        startString = start.strftime('%Y-%m-%d %H:%M:%S')
        endString = end.strftime('%Y-%m-%d %H:%M:%S')

        if startString == endString:
            displaytype = 'point'
            appname = ''
        else:
            displaytype = 'range'# If no time range is given, switch type to point

        title = "<b>App Focus</b><br />{0}<br />{1} - {2}<br />".format(bundle, startString, endString)
        title += "LAUNCH REASON: {0}".format(eventData["LAUNCH REASON"])

        output += "{" + \
                  "start: '{0}', " \
                  "end: '{1}', " \
                  "type:'{2}', " \
                  "group:{3}, " \
                  "content: '{4}', " \
                  "style: 'background-color:{5}', " \
                  "title: '{6}'" \
                  .format(startString, endString, displaytype, group, appname, color, title) \
                  + "},\n"

    appfocusFile.write(output[:-2] + "]")
    appfocusFile.close()
    return 0
