(function() {
    'use strict';

angular
    .module('iaHackathon')
    .factory('dataSheetService', dataSheetService);

dataSheetService.$inject = ['$http', '$q'];

function dataSheetService($http, $q) { 
    var predictionData = null;

    var service = {
        obtainPrediction: obtainPrediction,
        getPrediction: getPrediction,
        setPrediction: setPrediction
    };

    return service;

    function obtainPrediction(data) {
        var defer = $q.defer();

        // $http.get('/predictionJson/prediction.json', JSON.stringify(data)).then(function (response) {
        $http.post('/prediction', JSON.stringify(data)).then(function (response) {

            defer.resolve(response.data);
            
        }, function (response) {
            
            defer.reject(response);
            
        });

        return defer.promise;
    }

    function setPrediction(data) {
        predictionData = data;
    }

    function getPrediction() {
        return predictionData;
    }
}

})();