import sqlite3, json, datetime


def create(fromTimestamp, toTimestamp, database, group=0):
    # Prepare output file
    appActivityFile = open('output/data/appActivity.js', 'w', encoding="utf-8")
    appActivityFile.write('var appactivityData = [')
    # Read bundle id to app name translation file
    bundlefile = open('bundlenames.json', 'r').read()
    bundletranslation = json.loads(bundlefile)

    cur = database.cursor()
    appActivities = cur.execute("SELECT * \
         FROM APOLLO \
         WHERE (Activity = 'Application Activity' OR \
               Activity = 'Application Intents') \
         AND Key >= '{0}' AND Key <= '{1}' \
         ORDER BY Key".format(fromTimestamp.strftime('%Y-%m-%d %H:%M:%S'),
                              toTimestamp.strftime('%Y-%m-%d %H:%M:%S')))


    # Initialise array for coloring occurances of an app in the same color
    colors = ['#f94144', '#f3722c', '#f8961e', '#f9844a', '#f9c74f',
              '#90be6d', '#43aa8b', '#4d908e', '#577590', '#277da1']
    output = ''

    # Initialize variables for iterating
    counter = 0
    subgroupoffset = 0
    laststarttime = fromTimestamp
    bundleDict = {}
    print("Parsing app activity data... ")
    for event in appActivities:
        eventData = json.loads(event[2])  # Load data about the event
        bundle = eventData["BUNDLE ID"]
        if bundle not in bundleDict.keys():
            bundleDict[bundle] = colors[counter % len(colors) - 1]  # Assign color to an app the first time it occurs
            counter += 1
        color = bundleDict[bundle]  # If app already occurred, look up the assigned color

        timezone = datetime.timedelta(hours=eventData["GMT OFFSET"])
        start = datetime.datetime.strptime(eventData["START"], '%Y-%m-%d %H:%M:%S') + timezone
        end = datetime.datetime.strptime(eventData["END"], '%Y-%m-%d %H:%M:%S') + timezone

        startString = start.strftime('%Y-%m-%d %H:%M:%S')
        endString = end.strftime('%Y-%m-%d %H:%M:%S')

        # Place activities in different height in visualisation if too close together to avoid overlap
        if (start - laststarttime).seconds < 5:
            subgroupoffset += 1
        else:
            subgroupoffset = 0
        laststarttime = start

        displaytype = 'box' if startString == endString else 'range'  # If no time range is given, switch type to box

        if bundle in bundletranslation.keys():  # Search bundle id in translation file to show app name
            appname = bundletranslation[bundle]
        else:
            appname = bundle

        # Collect detailed info and write to tooltip
        title = "<b>App Activity</b><br>{0}<br />{1} - {2}<br />".format(bundle, startString, endString)
        if event[1] == "Application Intents":
            if "DERIVED INTENT ID" in eventData.keys() and eventData["DERIVED INTENT ID"]:
                title += "Intent ID: " + str(eventData["DERIVED INTENT ID"]) + "<br>"
            if "INTENT CLASS" in eventData.keys() and eventData["INTENT CLASS"]:
                title += "Intent Class: " + eventData["INTENT CLASS"] + "<br>"
            if "INTENT VERB" in eventData.keys() and eventData["INTENT VERB"]:
                title += "Intent Verb: " + eventData["INTENT VERB"] + "<br>"
            if "DIRECTION" in eventData.keys() and eventData["DIRECTION"]:
                title += "Direction: " + str(eventData["DIRECTION"])
        else:
            if "ACTIVITY TYPE" in eventData.keys() and eventData["ACTIVITY TYPE"]:
                title += "Activity Type: " + eventData["ACTIVITY TYPE"] + "<br>"
            if "CONTENT DESCRIPTION" in eventData.keys() and eventData["CONTENT DESCRIPTION"]:
                title += "Content Description: " + eventData["CONTENT DESCRIPTION"].replace("<br>", "") + "<br>"
            if "CONTENT URL" in eventData.keys() and eventData["CONTENT URL"]:
                title += "Content URL: " + eventData["CONTENT URL"] + "<br>"
            if "USER ACTIVITY REQUIRED STRING" in eventData.keys() and eventData["USER ACTIVITY REQUIRED STRING"]:
                title += "User Activity String: " + eventData["USER ACTIVITY REQUIRED STRING"]

        title = title.replace('\n', '<br />')  # Replace Line breaks with HTML line breaks
        # Create output for file
        output += "{" + \
                  "start: '{0}', " \
                  "end: '{1}', " \
                  "type:'{2}', " \
                  "group:{3}, " \
                  "subgroup: {4}, " \
                  "content: '{5}', " \
                  "style: 'background-color:{6}', " \
                  "title: \" {7}\"" \
                  .format(startString, endString, displaytype, group, subgroupoffset % 5, appname, color, title) \
                  + "},\n"

    appActivityFile.write(output[:-2] + "]")
    appActivityFile.close()
    return 0
