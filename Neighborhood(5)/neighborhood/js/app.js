var myPlaces = [{
        name: "Ludwig",
        latLng: {
            lat: 47.804094,
            lng: 13.046656
        }
    },
    {
        name: "Mozarts Geburtshaus",
        latLng: {
            lat: 47.800132,
            lng: 13.043555
        }
    },
    {
        name: "Cafe Bazar",
        latLng: {
            lat: 47.801772,
            lng: 13.043825
        }
    },
    {
        name: "220 Grad",
        latLng: {
            lat: 47.797853,
            lng: 13.049533
        }
    },
    {
        name: "Cafe Fingerlos",
        latLng: {
            lat: 47.807382,
            lng: 13.043642
        }
    },
    {
        name: "Schloss Mirabell",
        latLng: {
            lat: 47.807062,
            lng: 13.040699
        }
    }
];

var Place = function(data) {
    this.name = data.name;
    this.latLng = data.latLng;

    this.isSelected = ko.observable(0);
    this.isVisible = ko.observable(true);
    this.marker = null;
    this.infowindow = null;
};

var ViewModel = function(map) {
    var self = this;
    self.googleMap = map;
    this.places = ko.observableArray([]);
    this.filterValue = ko.observable("");
    this.selectedPlace = ko.observable(null);

    //place marker should bounce when the markers place is selected (via list or directly in map)
    this.toggleBounce = function(marker) {
        if (marker.getAnimation() !== null) {
            marker.setAnimation(null);
        } else {
            marker.setAnimation(google.maps.Animation.BOUNCE);
        }
    };

    this.selectPlace = function(clickedPlace) {
        //if user selects the already selected place, remove the selection from this place
        if (clickedPlace == self.selectedPlace()){
            self.selectedPlace().isSelected(0);
            self.toggleBounce(self.selectedPlace().marker);
            self.selectedPlace().infowindow.close();
            self.selectedPlace(null);
            return;
        }

        //unselect currently selected place if any, remove bouncing animation
        if (self.selectedPlace() !== null){
            self.selectedPlace().isSelected(0);
            self.toggleBounce(self.selectedPlace().marker);
            self.selectedPlace().infowindow.close();
        }
        //select new place, and add bouncing animation
        self.selectedPlace(clickedPlace);
        self.selectedPlace().isSelected(1);
        self.toggleBounce(clickedPlace.marker);

        //open up infowindow of selected marker
        self.selectedPlace().infowindow.open(
            self.googleMap, self.selectedPlace().marker);
    };

    //filter out all places that do not match the given filter by adjusting the isVisible field
    this.filterPlaces = function() {
        var filterValueLower = self.filterValue().toLowerCase();
        var placeFound = false;
        self.places().forEach(function(placeItem) {
            placeItem.isVisible(false);
            placeItem.marker.setVisible(false);
            // make all places visible with names that contain the filter string
            if (filterValueLower.length == 0 ||
                placeItem.name.toLowerCase().indexOf(filterValueLower) > -1) {
                placeItem.isVisible(true);
                placeItem.marker.setVisible(true);
                //select first visible place
                if (placeFound == false) {
                    self.selectPlace(placeItem);
                    placeFound = true;
                }
            }
        });
    }

    // this method populates the infowindows of the places with some of foresquares information about this place
    this.foursquare = function(place) {
        $.get("https://api.foursquare.com/v2/venues/search", {
                client_id: "KDQVOPOQ3HJ2422XD4PEZLHM2NVMTAY3MN21ZFGIJXWBQFIG",
                client_secret: "CMHIZYVP5RXEQOZYIFP0QPX3XKJMMCUBL0HNGNT4ZDFFLE14",
                v: "20170801",
                ll: "47.801772,13.043825",
                query: place.name,
                limit: 1
            },
            function(data) {
                //get web url, checkins count and formatted location
                var obj = data['response']['venues'][0];
                var infoWindowContent =
                    '<div id="content">' +
                    ' <h3>' + place.name + '</h3>' +
                    ' <strong>Address:</strong> ' + obj['location']['address'] + "," + obj['location']['city'] + '</br>' +
                    ' <strong>Url:</strong> <a href=' + obj['url'] + '>' + obj['url'] + '</a></br>' +
                    ' <strong>Check Ins:</strong> ' + obj['stats']['checkinsCount'] + '</br>' +
                    '</div>';
                place.infowindow = new google.maps.InfoWindow({
                    content: infoWindowContent
                });

        }).fail(function() {
            var infoWindowContent =
                '<div id="content">' +
                ' <h3>' + place.name + '</h3>' +
                    ' <p> Failed to retrieve information from Foursquare!</p>'+
                '</div>';
            place.infowindow = new google.maps.InfoWindow({
                content: infoWindowContent
            });
        });
    };

    //initialize every place with a marker, the information from the model and further information from fouresquare
    myPlaces.forEach(function(placeItem) {
        var cPlace = new Place(placeItem);
        var markerOptions = {
            map: self.googleMap,
            position: cPlace.latLng
        };
        cPlace.marker = new google.maps.Marker(markerOptions);

        self.foursquare(cPlace);

        //remove all animations from markers, to enable later bouncing animation
        cPlace.marker.setAnimation(null);
        //click on marker should have the same result as selecting the place from the list
        google.maps.event.addListener(cPlace.marker, 'click', function() {
            self.selectPlace(cPlace);
        });
        //in the beginning all places are visible
        cPlace.isVisible(true);
        self.places.push(cPlace);
    });



};

function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 47.801772,
            lng: 13.043825
        },
        zoom: 15
    });
    ko.applyBindings(new ViewModel(map));
    return map;
}

mapsError = function mapsError(){
    alert("failed to load google maps");
};

//for collapsing and expanding sidebar view
$(document).ready(function() {
    $('[data-toggle="offcanvas"]').click(function() {
        $('.row-offcanvas').toggleClass('active');
    });
});
