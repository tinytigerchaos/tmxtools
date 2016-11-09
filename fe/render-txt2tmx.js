define(['require', 'jquery'], function(require, $) {

    /**
     * 功能选择： Tmx文件转存为Txt文件
     * 需要参数params：
     *  size: 每个文件存储条数，默认0.表示不分割文件
     *  srcPath: 表示源文件路劲
     * 	tgtPath: 目标文件路劲，文件转存为txt后的存储路劲
     * 	splitMark: txt每行中英分割符
     */

    // 与 main process 进程通信的模块 
	var ipcRender = nodeRequire('electron').ipcRenderer;

    $('.txt2tmx-action').unbind('click').click(function () {
        $('.tools').addClass('hidden');

        var txt2TmxContainer = $('.txt2tmx').removeClass('hidden');
        // 选择tmx文件路劲
        txt2TmxContainer.find('.choose-src-file').unbind('click').click(function (e) {
            e.preventDefault();

            ipcRender.send('choose-file', {
                title: '选择Txt文件',
                filters: [
                    {name: 'Txt文件', extensions: ['txt']},
                    {name: '所有文件', extensions: ['*']}
                ]
            }, 'choose-txt-file-back');
            ipcRender.once('choose-txt-file-back', function (event, filenames) {
                console.log('选择的文件: ' + filenames);
                txt2TmxContainer.find('.src-file-name').val(filenames);
            });

            return false;
        });

        // 选择txt文件路劲
        txt2TmxContainer.find('.choose-tgt-file').unbind('click').click(function (e) {
            e.preventDefault();

            ipcRender.send('save-file', 'save-file-back');
            ipcRender.once('save-file-back', function (event, filenames) {
                console.log('选择的文件: ' + filenames);
                txt2TmxContainer.find('.tgt-file-name').val(filenames);
            });

            return false;
        });

        // 提交信息，开始处理数据
        txt2TmxContainer.find('.confirm-btn').unbind('click').click(function (e) {
            e.preventDefault();

            // check params
            // 1. srcPath
            // 2. tgtPath
            // 3: size
            // 4. 分割符
            var num = parseInt(txt2TmxContainer.find('.file-tu-nums').val());
            num = isNaN(num) ? 4000 : (num > 0 ? num : 4000);
            var params = {
                srcPath: txt2TmxContainer.find('.src-file-name').val(),
                tgtPath: txt2TmxContainer.find('.tgt-file-name').val(),
                size: num,
                splitMark: txt2TmxContainer.find('.radio input[name=optionsRadios]').val() == 1 ? '\t' : txt2TmxContainer.find('#tabkey').val()
            }
            if (params.srcPath.length < 1 || params.tgtPath.length < 1) {
                return;
            }

            ipcRender.send('txt2tmx', params, 'txt2tmx-back');
            ipcRender.once('txt2tmx-back', function (event, res) {
                console.log(res);
            });
        });
    });
});