define(['require', 'jquery'], function(require, $) {

    function init(){
		/**
		 * 初始化所有功能模块的交互事件
		 */
		require([ './render-tmx2txt',
				  './render-mergemd5',
				  './render-genmd5repo',
				  './render-filereoutput',
				  './render-txt2tmx'], function(){
			// 所有事件全部初始化完毕，默认显示第一个功能
			$('.tmx2txt-action').click();
			// $('.txt2tmx-action').click();
		});
    }

    return {
        init: init
    }

});