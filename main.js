const {app, BrowserWindow} = require('electron')
const electron = require('electron')
const path = require('path');
const http = require('http');
const dialog = electron.dialog;

var childProcess = require('child_process');
// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let win

function createWindow () {
  // Create the browser window.
  win = new BrowserWindow({width: 1200, height: 600})

  // and load the index.html of the app.
  win.loadURL(`file://${__dirname}/index.html`)

  // Open the DevTools.
  win.webContents.openDevTools()

 // TODO: 注册全局快捷键

 // 开始python webContents服务

//  childProcess.exec('./python/pyth')

  // Emitted when the window is closed.
  win.on('closed', () => {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    win = null
  })
}

// function getPath() {
//   var sourcefilepath = dialog.showOpenDialog({properties: ['openFile', 'openDirectory', 'multiSelections']})
//   console.log(sourcefilepath)
//
// }

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (win === null) {
    createWindow()
  }
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

var ipcMain = require('electron').ipcMain;

/**
 * 监听页面选择文件事件，打开文件选择框，发送文件名路劲
 */
ipcMain.on('choose-file', function(event, types, callbackName){
    console.log(types);
    console.log(callbackName);

    dialog.showOpenDialog({
      title: '选择Tmx文件',
      defaultPath: '',
      filters: [
          { name: 'Tmx文件', extensions: ['tmx'] },
          { name: '所有文件', extensions: ['*'] }
        ],
      properties:['openFile']
    }, function(filenames){
      event.sender.send(callbackName, filenames);
    });
})

/**
 * 监听前台文件选择，用户选择保存一个文件，需输入文件名
 */
ipcMain.on('save-file', function(event, callbackName){
    console.log(callbackName);

    dialog.showSaveDialog({
      title: '选择Tmx文件',
      defaultPath: ''
    }, function(filenames){
      event.sender.send(callbackName, filenames);
    });
})


ipcMain.on('tmx2txt', function(event, params, callbackName){
  var res = '';
  // todo: 调用Python接口

  // http.post('http://localhost:8888/tmxtotxt', options, function(res){

  // })


  event.sender.send(callbackName, res);
})