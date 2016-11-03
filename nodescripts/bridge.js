const {ipcMain} = require('electron');
const httpPost = require('./httppost.js');

/**
 * 负责接收前台页面发出处理文件的请求，并将相关参数转发到后台服务（tarnado）
 */

// Tmx转存为Txt
ipcMain.on('tmx2txt', function (event, params, callbackName) {
	var originEvent = event;

	var options = {
		path: 'tmxtotxt',
		params: params
	}

	httpPost(options, function(res){
		originEvent.sender.send(callbackName, res);
	});
});

// Txt转存为Tmx
ipcMain.on('txt2tmx', function (event, params, callbackName) {
	var originEvent = event;

	var options = {
		hostname: 'localhost',
		port: 8888,
		path: 'txttotmx',
		method: 'POST',
		params: params
	}

	httpPost(options, function(res){
		originEvent.sender.send(callbackName, res);
	});
})