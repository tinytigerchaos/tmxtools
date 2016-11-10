const {ipcMain} = require('electron');
const _http = require('./http.js');
let port = 8888;

/**
 * 负责接收前台页面发出处理文件的请求，并将相关参数转发到后台服务（tarnado）
 */

// Tmx转存为Txt
ipcMain.on('tmx2txt', function (event, params, callbackName) {
	var originEvent = event;

	var options = {
		path: 'tmxtotxt',
		params: params,
		port: port
	}

	_http.post(options, function(res){
		originEvent.sender.send(callbackName, res);
	});
});

// Txt转存为Tmx
ipcMain.on('txt2tmx', function (event, params, callbackName) {
	var originEvent = event;

	var options = {
		path: 'txttotmx',
		params: params,
		port: port
	}

	_http.post(options, function(res){
		originEvent.sender.send(callbackName, res);
	});
});

module.exports = function setPort(currentPort){
	port = currentPort;
}