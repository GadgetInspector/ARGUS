# ARGUS (Apple Reconnaissance Graphical Unification System):

Processes input from [APOLLO](https://github.com/mac4n6/APOLLO) by Sarah Edwards to create a timeline of forensic activity of iOS devices (up to iOS 15)

The input file must be the output database of APOLLO with -o sql_json parameter used in APOLLO.

After the program finished, open argus_output.html in Firefox or Chrome. You can zoom by scrolling in the timeline and pan by clicking and dragging. Locations in the timeline can be clicked to set the map marker. Hovering over an element will reveal a tooltip with additional information.

If you want to save or share the result, copy the output/ folder to somewhere else.

Currently processed data types: 
- App in Focus
- App Usage
- App Activity/Intent
- Audio Output
- Display Backlight Status
- Plugged In State
- Steps Taken

## Misc
Feel free to contact me with things you need, want to see improved, hate,... I'm new to this github stuff so I might need some time to get adjusted. 

## Usage

argus.py [-h] --start START --end END --gmtoffset GMTOFFSET -d DATABASE

## Example

`argus.py --start "2022-10-25 18:00:00" --end "2022-10-25 19:00:00" --gmtoffset 2 -d apollo.db`

Shows forensics activity data from 18:00 to 19:00 on October 25, 2022. Open argus_output.html in the output directory to see the results. 


## TO DO
- Include more data types 
- Include more health data
- Include more location types (Cloud-V2.sqlite etc)
- Options to show/hide data types
- Show more metadata from App Activities/Intents
- Decode some plist data to get even more meta data
- Metadata all the things
- Make this iOS 16 proof (i. e. add iOS16 support to APOLLO)


