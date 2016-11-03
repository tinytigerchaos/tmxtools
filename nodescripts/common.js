const electron = require('electron');
const ipcMain = electron.ipcMain;
const dialog = electron.dialog;

/**
 * 监听页面选择文件事件，打开文件选择框，发送文件名路劲
 */
ipcMain.on('choose-file', function (event, options, callbackName) {
    console.log(callbackName);
    options = options || {};

    dialog.showOpenDialog({
		title: options.title || '选择文件',
		defaultPath: '',
		filters: options.filters || [
			{ name: '所有文件', extensions: ['*'] }
        ],
		properties: options.properties || ['openFile']
    }, function (filenames) {
		event.sender.send(callbackName, filenames);
    });
});

/**
 * 监听前台文件选择，用户选择保存一个文件，需输入文件名
 */
ipcMain.on('save-file', function (event, callbackName) {
    console.log(callbackName);

    dialog.showSaveDialog({
		title: '选择文件',
		defaultPath: ''
    }, function (filenames) {
		event.sender.send(callbackName, filenames);
    });
});