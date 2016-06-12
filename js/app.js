angular.module('sortApp', [])

.controller('mainController', function($scope, $http) {
  $scope.sortType     = 'Price'; // set the default sort type
  $scope.sortReverse  = false;  // set the default sort order
  $scope.searchCars   = '';     // set the default search/filter term
  $scope.master = {
          'Model' : 'Any',
          'Location' : 'Any',
          'Year' : 'Any',
          'Color' : 'Any',
          'Wheel' : 'Any',
          'Roof' : 'Any',
          'Mileage' : 30000,
          'Price' : 80000
  };

  
  $scope.reset = function() {
    $scope.filter = angular.copy($scope.master);
  };

  $scope.reset();
  
  $scope.getCars = function() {
      var config = {
        params : $scope.filter
      };
  

     $http.get('/api', config).success(function(response){
          $scope.cars = response;
          $scope.numcars = $scope.cars.length
      });



  }
  $scope.getCars(); 

  
});