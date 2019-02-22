(function() {
    'use strict';


    angular
    .module('iaHackathon')
    .controller('PredictionResultController', PredictionResultController);
    
    PredictionResultController.$inject = ['dataSheetService', "$state"];

    function PredictionResultController(dataSheetService, $state) {
        var vm = this;
        vm.dataPrediction = null;
        vm.dataShow = {};
        vm.back = back;

        init();

        function init() {
            vm.dataPrediction = dataSheetService.getPrediction();
            if (vm.dataPrediction !== undefined && vm.dataPrediction !== null) {
                if (vm.dataPrediction.Prediction.predictedLabel === "M") {
                    vm.dataShow.color="#e60000";
                    vm.dataShow.text ="Malignant tumor";
                    vm.dataShow.percent = vm.dataPrediction.Prediction.predictedScores.M;
                } else {
                    vm.dataShow.color="#29a329";
                    vm.dataShow.text ="Benign tumor";
                    vm.dataShow.percent = vm.dataPrediction.Prediction.predictedScores.B;
                }
            } else {
                vm.dataShow.color="#FFFF";
                vm.dataShow.text ="No prediction result";
                vm.dataShow.percent = 0;
            }


        }

        
        function back() {
            $state.go("init");
        }
    }
    

})();