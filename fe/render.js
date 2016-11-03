define(['require', 'jquery'], function(require, $) {

	// 与 main process 进程通信的模块 
	var ipcRender = nodeRequire('electron').ipcRenderer;

    function init(){
        /**
         * 功能选择： Tmx文件转存为Txt文件
         * 需要参数params：
         *  size: 每个文件存储条数，默认0.表示不分割文件
         *  srcPath: 表示源文件路劲
		 * 	tgtPath: 目标文件路劲，文件转存为txt后的存储路劲
		 * 	splitMark: txt每行中英分割符
         */
        $('.tmx2txt-action').unbind('click').click(function(){
			$('.tools').addClass('hidden');

			var tmx2TxtContainer = $('.tmx2txt').removeClass('hidden');

			
			// 选择tmx文件路劲
			tmx2TxtContainer.find('.choose-src-file').unbind('click').click(function(e){
				e.preventDefault();

				console.log('kkkkk');

				ipcRender.send('choose-file', ['tmx'], 'choose-tmx-file-back');
				ipcRender.once('choose-tmx-file-back', function(event, filenames){
					console.log('选择的文件: ' + filenames);
					tmx2TxtContainer.find('.src-file-name').val(filenames);
				});

				return false;

			});

			// 选择txt文件路劲
			tmx2TxtContainer.find('.choose-tgt-file').unbind('click').click(function(e){
				e.preventDefault();

				ipcRender.send('save-file', 'save-file-back');
				ipcRender.once('save-file-back', function(event, filenames){
					console.log('选择的文件: ' + filenames);
					tmx2TxtContainer.find('.tgt-file-name').val(filenames);
				});

				return false;
			});

			// 提交信息，开始处理数据
			tmx2TxtContainer.find('.confirm-btn').unbind('click').click(function(e){
				e.preventDefault();

				// check params
				// 1. srcPath
				// 2. tgtPath
				// 3: size
				// 4. 分割符
				var num = parseInt(tmx2TxtContainer.find('.file-tu-nums').val());
				num = isNaN(num) ? 4000 : (num > 0 ? num : 4000);
				var params = {
					srcPath: tmx2TxtContainer.find('.src-file-name').val(),
					tgtPath: tmx2TxtContainer.find('.tgt-file-name').val(),
					size: num,
					splitMark: tmx2TxtContainer.find('.radio input[name=optionsRadios]').val() == 1 ? '\t' : tmx2TxtContainer.find('#tabkey').val() 
				}
				if( params.srcPath.length < 1 || params.tgtPath.length < 1 ) {
					return ;
				}

				ipcRender.send('tmx2txt', params, 'tmx2txt-back');
				ipcRender.once('tmx2txt-back', function(event, rs){
					console.log(res);
				});
			});
        });
    }

   
    return {
        init: init
    }

});