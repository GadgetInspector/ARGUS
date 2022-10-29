function locationClick(properties) { //Eventlistener for click on location data to update map
    if(properties.item){
         const item = items.get(properties.item);
         if(item.lon) {
             markers.clearMarkers();
             var lonLat = new OpenLayers.LonLat(item.lon , item.lat)
                .transform(
                     new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
                     map.getProjectionObject() // to Spherical Mercator Projection
             );
             markers.addMarker(new OpenLayers.Marker(lonLat));
             zoom=15;
             map.setCenter (lonLat, zoom);

         }
         document.getElementById('details').innerHTML = item.title;
    }
}

document.getElementById("start").innerHTML = start;
document.getElementById("end").innerHTML = end;


var container = document.getElementById('timeline');
var healthContainer = document.getElementById('health')
var map = new OpenLayers.Map("map");

// Create a Timeline
var groups = new vis.DataSet();
var subgroups = new vis.DataSet();
groups.add({id: 0, content: 'Display'});
groups.add({id: 1, content: 'App in Focus'});
groups.add({id: 2, content: 'App Usage'});
groups.add({id: 3, content: 'Audio Output'});
groups.add({id: 4, content: 'Plugged In'});
groups.add({id: 5, content: 'Routined Locations'});
groups.add({id: 6, content: 'App Activity'});
var items = new vis.DataSet();
items.add(appfocusData);
items.add(backlightData);
items.add(audiooutputData);
items.add(appactivityData);
items.add(pluggedInData);
items.add(appUsageData);
items.add(routinedlocData);
var healthItems = new vis.DataSet(stepsdistance)

// Configuration for the Timeline
var options = {
    align: 'center',
    groupOrder: 'id',
    groupHeightMode: 'auto',
    stack: false,
    start: start,
    end: end,
    min: start,
    max: end,
    margin: { axis: 5 },// minimal margin between items and the axis
    tooltip: {
      followMouse: true,
      overflowMethod: 'cap',
      delay: 100,
    },
    orientation: { axis: 'both'}
};


var timeline = new vis.Timeline(container, items, options);
timeline.setGroups(groups);

//Create map
map.addLayer(new OpenLayers.Layer.OSM());
var markers = new OpenLayers.Layer.Markers( "Markers" );
map.addLayer(markers);

timeline.on("click", locationClick); //Set eventlistener if an element in the timeline is clicked

var healthOptions = {
  style:'bar',
  drawPoints: false,
  dataAxis: {icons:true},
  orientation:'bottom',
  start: start,
  min:start,
  end: end,
  max: end,
};

var health_steps = new vis.Graph2d(health, healthItems, healthOptions);
var healthGroups = new vis.DataSet();
healthGroups.add({id: 0, content: 'Steps Long intervals'});
healthGroups.add({id: 1, content: 'Steps Short intervals'});

