function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition);
    } else { 
      alert("Geolocation is not supported by this browser.");
    }
}

var map, infoWindow;
var marker = false; ////Has the user plotted their location marker? 
function initMap() {
    //The center location of our map.
    var centerOfMap = new google.maps.LatLng(20.0094409, 64.4213648);
    map = new google.maps.Map(document.getElementById('map'), {
        center: centerOfMap,
        zoom: 8,
        mapTypeControl: true,
    });
    infoWindow = new google.maps.InfoWindow;

  // Try HTML5 geolocation.
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
            };

            infoWindow.setPosition(pos);
            infoWindow.setContent('You are here');
            infoWindow.open(map);
            map.setCenter(pos);
            map.setZoom(15);
        }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
    // Browser doesn't support Geolocation
    handleLocationError(false, infoWindow, map.getCenter());
    }

    //Listen for any clicks on the map.
    google.maps.event.addListener(map, 'click', function(event) {                
        //Get the location that the user clicked.
        var clickedLocation = event.latLng;
        //If the marker hasn't been added.
        if(marker === false){
            //Create the marker.
            marker = new google.maps.Marker({
                position: clickedLocation,
                map: map,
                draggable: true //make it draggable
            });
            //Listen for drag events!
            google.maps.event.addListener(marker, 'dragend', function(event){
                markerLocation();
            });
        } else{
            //Marker has already been added, so just change its location.
            marker.setPosition(clickedLocation);
        }
        //Get the marker's location.
        markerLocation();
    });

}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
  infoWindow.open(map);
}

//This function will get the marker's current location and then add the lat/long
//values to our textfields so that we can save the location.
function markerLocation(){
    //Get location.
    var currentLocation = marker.getPosition();
    //Add lat and lng values to a field that we can save.
    // document.getElementById('lat').value = currentLocation.lat(); //latitude
    // document.getElementById('lng').value = currentLocation.lng(); //longitude
    console.log(currentLocation.lat());
    console.log(currentLocation.lng());
}
        

//Load the map when the page has finished loading.
google.maps.event.addDomListener(window, 'load', initMap);