import datetime as datetime, argparse, sqlite3, sys
from os import path
from modules import audioOutput, \
    backlight, \
    appFocus, \
    appActivity, \
    healthData, \
    pluggedIn, \
    appUsage, \
    routinedloc

if __name__ == '__main__':
    version ='1.0b0'
    parser = argparse.ArgumentParser(description=
                                     '''\n\nARGUS (Apple Reconnaissance Graphical Unification System)  
                                     Version: ''' + version + '''
                                    - Processes input from APOLLO (https://github.com/mac4n6/APOLLO) by Sarah Edwards 
                                    to create a timeline of forensic activity.\n\n\n
                                    The input file must be the output database of APOLLO with -o sql_json parameter.\n
                                    After the program finished, open argus_output.html in Firefox or Chrome.
                                    You can zoom by scrolling in the timeline and pan by clicking and dragging.
                                    Locations in the timeline can be clicked to set the map marker.
                                    
                                    \n\n\tAuthor: Philip Schütz, State Criminal Police Office North-Rhine Westphalia, Germany, 
                                    Digital Forensics Division''', prog='argus.py')

    parser.add_argument('--start',
                        help='Starting Timestamp (UTC) in format YYYY-MM-DD hh:mm:ss. '
                             'Any event starting after this time will be included in the timeline',
                        required=True)
    parser.add_argument('--end',
                        help='Ending Timestamp (UTC) in format YYYY-MM-DD hh:mm:ss. '
                             'Any event starting before this time will be included in the timeline',
                        required=True)
    parser.add_argument('--gmtoffset',
                        help='Assumed timezone (number of hours) to add to UTC/GMT timestamps',
                        required=True, type=int)
    parser.add_argument('-d', '--database', help='Path to the APOLLO database to be processed',
                        required=True)
    args = vars(parser.parse_args())

    try:
        gmtOffset = datetime.timedelta(hours=args['gmtoffset'])
    except ValueError:
        print("\nInvalid value for timezone. Value should be offset to UTC/GMT in hours")
        sys.exit(1)
    try:
        start = datetime.datetime.strptime(args['start'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        print("\nInvalid start timestamp! Use format YYYY-MM-DD hh:mm:ss")
        sys.exit(1)
    try:
        end = datetime.datetime.strptime(args['end'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        print("\nInvalid ending timestamp! Use format YYYY-MM-DD hh:mm:ss")
        sys.exit(1)
    try:
        if path.exists(args['database']):
            database = sqlite3.connect(args['database'])
            cur = database.cursor()
            cur.execute("SELECT * FROM APOLLO LIMIT 1")
        else:
            raise Exception
    except:
        print("\nNo valid database found at " + args['database'])
        sys.exit(1)

    if end < start:
        print("\nEnding timestamp can not be earlier than starting timestamp")
        sys.exit(1)
    if end - start > datetime.timedelta(hours=24):
        print("\nWARNING: Time period to visualise should not be longer than 24 hours. Continuing anyways...\n")

    print("\nARGUS (Apple Reconnaissance Graphical Unification System) Version: " + version +
          "\nProcesses input from APOLLO (https://github.com/mac4n6/APOLLO) by Sarah Edwards to create a timeline " +
          "of forensic activity.\n\n" +
          "The input file must be the output database of APOLLO with -o sql_json parameter.\n" +
          "After the program finished, open argus_output.html in Firefox or Chrome. You can zoom by scrolling in " +
          "the timeline and pan by clicking and dragging. Locations in the timeline can be clicked to set the "
          "map marker. Hovering over an element will reveal a tooltip with additional information.\n"
          "If you want to save or share the result, copy the output/ folder to somewhere else.\n\n" +
          "Author: Philip Schütz, State Criminal Police Office North-Rhine Westphalia, Germany, " +
          "Digital Forensics Division\n")

    print("Start Parsing: ...\n")
    backlight.create(start, end, database, 0)
    appFocus.create(start, end, database, 1)
    appUsage.create(start, end, database, 2)
    audioOutput.create(start, end, database, 3)
    pluggedIn.create(start, end, database, 4)
    routinedloc.create(start, end, gmtOffset, database, 5)

    appActivity.create(start, end, database, 6)
    healthData.create(start, end, gmtOffset, database)

    offsetstart = start + gmtOffset
    offsetend = end + gmtOffset
    globalsFile = open('output/globals.js', 'w')
    globalsFile.write('var start = "{0}"; \n'.format(offsetstart.strftime('%Y-%m-%d %H:%M:%S')))
    globalsFile.write('var end = "{0}";'.format(offsetend.strftime('%Y-%m-%d %H:%M:%S')))
