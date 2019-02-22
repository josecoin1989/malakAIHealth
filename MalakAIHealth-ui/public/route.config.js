(function() {
    'use strict';

    angular.module('iaHackathon')
        .config(function($stateProvider, $urlServiceProvider, $mdThemingProvider) {


        $urlServiceProvider.rules.otherwise({ state: 'init' });

        var initState = {
            name: 'init',
            url: '/init',
            templateUrl: './components/dataSheet/dataSheet.template.html',
            controller: 'DataSheetController as vmDataSheetController'
        }
    
        var resultState = {
            name: 'result',
            url: '/result',
            templateUrl: './components/predictionResult/predictionResult.template.html',
            controller: 'PredictionResultController as vmPredictionResultController'
        }

        var errorState = {
            name: 'error',
            url: '/error',
            templateUrl: './components/error/error.template.html',
            controller: 'ErrorController as vmErrorController'
        }
  
    $stateProvider.state(initState);
    $stateProvider.state(resultState);
    $stateProvider.state(errorState);

    $mdThemingProvider.theme('docs-dark', 'default')
        .primaryPalette('yellow')
        .dark();
  });

  
})();