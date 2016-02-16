angular.module('sortApp', [])

.controller('mainController', function($scope) {
  $scope.sortType     = 'Price'; // set the default sort type
  $scope.sortReverse  = false;  // set the default sort order
  $scope.searchCars   = '';     // set the default search/filter term
  
  // create the list of sushi rolls 
  $scope.cars = [{"Interior": "IPMB", "Roof": "RFBC", "Price": 51000.0, "Status": "Active", 
                  "Created_at": "2016-01-29 20:21:59.467239", "Mileage": 23036.0, "Year": "2013", 
                  "Pic": "https://my.teslamotors.com/configurator/compositor/?model=ms&view=STUD_3QTR&size=120&bkba_opt=2&file_type=jpg&options=MS01,RENA,AD02,AU00,BT60,CH00,COL3-PPMR,DRLH,HP00,IDLW,IPMB,PA00,PF00,PS01,RFBC,SC01,SU00,TM00,TP01,TR00,WT19,X001,X003,X007,X009,X011,X014,X020,X025,X027,X031,YF00", "Location": "Seattle", "Paint": "COL3-PPMR", "Last_Update": "None", "Model": "BT60", "Id": "P13590", "Wheel": "WT19"}, 
                  {"Interior": "QPMT", "Roof": "RFPO", "Price": 50800.0, "Status": "Active", "Created_at": "2016-01-29 20:22:00.675578", 
                  "Mileage": 24184.0, "Year": "2013", "Pic": "https://my.teslamotors.com/configurator/compositor/?model=ms&view=STUD_3QTR&size=120&bkba_opt=2&file_type=jpg&options=MS01,RENA,AD02,AU00,BS00,BT60,CH00,COL2-PMSG,CW00,DRLH,DV2W,FG02,HP00,IDPB,IX00,LP00,PA00,PF00,PK00,PS01,PX00,QPMT,RFPO,SC01,SP00,SU00,TM00,TP01,TR00,UTMF,WT19,WTX0,X001,X003,X007,X009,X011,X014,X021,X025,X027,X028,X031,X040,YF00", 
                  "Location": "New York", "Paint": "COL2-PMSG", "Last_Update": "None", "Model": "BT60", "Id": "P26502", "Wheel": "WT19"}, {"Interior": "IPMT", "Roof": "RFPO", "Price": 50700.0, "Status": "Active", "Created_at": "2016-01-29 20:22:00.327272", "Mileage": 27311.0, "Year": "2013", "Pic": "https://my.teslamotors.com/configurator/compositor/?model=ms&view=STUD_3QTR&size=120&bkba_opt=2&file_type=jpg&options=MS01,RENA,AD02,AU00,BS00,BT60,CH00,COL3-PPMR,CW00,DRLH,HP00,IDOM,IDPB,IPMT,LP00,PA00,PF00,PK00,PS01,RFPO,SC01,SP00,SU00,TM00,TP01,TR00,WT19,X001,X003,X007,X009,X011,X014,X020,X025,X027,X031,YF00", 
                  "Location": "New York", "Paint": "COL3-PPMR", "Last_Update": "None", "Model": "BT60", "Id": "P16389", "Wheel": "WT19"}];
  
});