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

`argus.py [-h] --start START --end END --gmtoffset GMTOFFSET -d DATABASE`

Shows forensics activity data from 18:00 to 19:00 on October 25, 2022. Open argus_output.html in the output directory to see the results. 
`start` and `end` are to be specified in UTC time. The parameter `gmtoffset` reflects the time difference from UTC including correction for daylight savings time. When the timezone is UTC+1 (Amsterdam, Paris, Berlin) in June, `gmtoffset` should be set to `2`, in December to `1`. This is currently relevant for location and health data, as other activity data has timezone information associated to them in the source database. 

## Example

`argus.py --start "2022-10-25 18:00:00" --end "2022-10-25 19:00:00" --gmtoffset 2 -d apollo.db`




## TO DO
- Include more data types 
- Include more health data
- Include more location types (Cloud-V2.sqlite etc)
- Include timestamps and files of .ktx files to show display content in timeline
- Options to show/hide data types
- Show more metadata from App Activities/Intents
- Decode some plist data to get even more meta data
- Metadata all the things
- Make this iOS 16 proof (i. e. add iOS16 support to APOLLO)


