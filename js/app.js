angular.module('sortApp', [])

.controller('mainController', function($scope, $http) {
  $scope.sortType     = 'Price'; // set the default sort type
  $scope.sortReverse  = false;  // set the default sort order
  $scope.searchCars   = '';     // set the default search/filter term
  $scope.master = {
          'Model' : 'Any',
          'Location' : 'Any',
          'Year' : 'Any',
          'Wheel' : 'Any',
          'Roof' : 'Any',
          'Mileage' : 30000,
          'Price' : 80000
  };

  
  $scope.reset = function() {
    //console.log("Reset accessed");
    $scope.filter = angular.copy($scope.master);
    //console.log("Reset accessed 2");
  };

  $scope.reset();
  
  $scope.getCars = function() {
      var config = {
        params : $scope.filter
      };
  

     $http.get('/api', config).success(function(response){
          //console.log(config)
          //console.log("My data: "+ response);
          
          $scope.cars = response;
          $scope.numcars = $scope.cars.length
      });



  }
  $scope.getCars(); 

  
});