(function() {
    'use strict';


    angular
    .module('iaHackathon')
    .controller('ErrorController', ErrorController);
    
    ErrorController.$inject = ['dataSheetService', "$state"];

    function ErrorController(dataSheetService, $state) {
        var vm = this;

        vm.back = back;

        init();

        function init() {
            vm.dataPrediction = dataSheetService.getPrediction();

        }

        function back() {
            $state.go("init");
        }
    }
    

})();