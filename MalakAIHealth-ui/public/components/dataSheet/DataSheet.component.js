(function() {
    'use strict';

    angular
    .module('iaHackathon')
    .controller('DataSheetController', DataSheetController);
    
    DataSheetController.$inject = ['dataSheetService', "$state"];

    function DataSheetController(dataSheetService, $state) {
        var vm = this;

        vm.dataSheet = {
            radius_mean: 0,
            texture_mean: 0,
            perimeter_mean: 0,
            area_mean: 0,
            smoothness_mean: 0,
            compactness_mean: 0,
            concavity_mean: 0,
            concave_points_mean: 0,
            symmetry_mean: 0,
            fractal_dimension_mean: 0,

            radius_se: 0,
            texture_se: 0,
            perimeter_se: 0,
            area_se: 0,
            smoothness_se: 0,
            compactness_se: 0,
            concavity_se: 0,
            concave_points_se: 0,
            symmetry_se: 0,
            fractal_dimension_se: 0,

            radius_worst: 0,
            texture_worst: 0,
            perimeter_worst: 0,
            area_worst: 0,
            smoothness_worst: 0,
            compactness_worst: 0,
            concavity_worst: 0,
            concave_points_worst: 0,
            symmetry_worst: 0,
            fractal_dimension_worst: 0
        };
        vm.selectedIndex = 0;

        vm.next = next;
        vm.back = back;
        vm.send = send;

        init();

        function init() {
            vm.selectedIndex = 0;
        }

        function next() {
            if (vm.selectedIndex<2) {
                vm.selectedIndex += 1; 
            }
            
        }

        function back() {
            if (vm.selectedIndex>0) {
                vm.selectedIndex -= 1;
            }
        }

        function send() {
            dataSheetService.obtainPrediction(vm.dataSheet).then(function (data) {
                console.log("ok");
                console.log(data);
                dataSheetService.setPrediction(data);
                $state.go("result");

            }, function (dataError) {
                console.log("Ko");
                console.log(dataError);
                dataSheetService.setPrediction(dataError);
                $state.go("error");

            });
        }

    }

  
})();