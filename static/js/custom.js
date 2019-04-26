function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition);
    } else { 
      alert("Geolocation is not supported by this browser.");
    }
}

var lats, lngs;

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
            getAdd(pos.lat, pos.lng);
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
            lats = clickedLocation.lat();
            lngs = clickedLocation.lng();
            document.getElementById("lat").value = lats;
            document.getElementById("lng").value = lngs;
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
    lats = currentLocation.lat();
    lngs = currentLocation.lng();
    document.getElementById("lat").value = lats;
    document.getElementById("lng").value = lngs;
    changeAdd();
}
        

//Load the map when the page has finished loading.
google.maps.event.addDomListener(window, 'load', initMap);

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})


function changeAdd() {
    var latt = document.getElementById("lat").value;
    var lngg = document.getElementById("lng").value;
    getAdd(latt, lngg);
}

function getAdd(latt, lngg) {
    var xmlhttp = new XMLHttpRequest();
    var url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+ latt + "," + lngg +"&key=AIzaSyBsWOCuRTvT2j9QSPMwuY_9DpC-Ei6sYvc";
    console.log(url);
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var myArr = JSON.parse(this.responseText);
            mFunction(myArr);
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
    
    function mFunction(arr) {
        // console.log(arr['results']);
        document.getElementById("address").value = arr['results'][0]['formatted_address'];
    }            
}

function productDetails(barcode) {
    var xmlhttp = new XMLHttpRequest();
    var url = "/lookup/"+ barcode;
    console.log(url);
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // console.log(this.responseText);
            var text = this.responseText.split(",")[1].split(":")[1].split("'")[1];
            var image_url = this.responseText.split(",")[3].split(":")[1].split("'")[1];
            var splited = this.responseText.split(":")
            var pk = splited[splited.length-1].split("}")[0]
            // var myArr = JSON.parse(text);
            mfunction(text, image_url, pk);
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
    
    function mfunction(text, image_url, pk) {
        document.getElementById("pid").value = pk;
        document.getElementById("product_title").value = text;
        document.getElementById("image_u").value = image_url;
    }            
}