define(['require', 'jquery'], function(require, $) {

	var ipcRender = nodeRequire('electron').ipcRenderer;

    $('.file-reoutput-action').unbind('click').click(function () {
        $('.tools').addClass('hidden');

        var fileReoutputContainer = $('.file-reoutput').removeClass('hidden');

        // init the event

        // submit
            // check param
            // call node api
    });
});