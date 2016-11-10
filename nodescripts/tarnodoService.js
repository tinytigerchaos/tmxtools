const childProcess = require('child_process');
const fs = require('fs');
const _http = require('./http.js');
const path = require('path');

function start( callback ){
    /**
     * 开始python webContents服务
     * 1. windows 平台
     */

    // 删除port文件
    try {
        fs.unlinkSync('./port.txt');
    } catch (error) {
        console.log('port文件不存在');
    }

    let checkTimer; // 检查服务是否已启动

    // 开始服务，执行main.exe文件
    let startProcess = childProcess.spawn(path.dirname(__dirname) + '/main.exe', ['']);
    startProcess.stdout.on('data', function(data){
        console.log('data: ' + data.toString());
    });
    startProcess.stdout.on('end', function(){
        console.log('start process ended.');
        clearInterval(checkTimer);
    });
    startProcess.stderr.on('data', function(data){
        console.log('err data info: ' + data.toString());
        clearInterval(checkTimer);
    });
    startProcess.on('exit', function(code){
        console.log('startProcess exit with code: ' + code);
        clearInterval(checkTimer);
    });

    // 轮训检查port文件是否已经创建成功
    checkTimer = setInterval(function(){
        try {
            var port = parseInt(fs.readFileSync('./port.txt').toString());
            if(!isNaN(port) && port > 0) {
                // 说明检测到端口已启动成功
                clearInterval(checkTimer);
                console.log('启动成功, 端口号： ' + port);
                if(callback) {
                    callback(port);
                }
            }   
        } catch (error) {
            // console.log(error);
            console.log('文件不存在');
        }
    }, 3000);
}

function stop(port){
    _http.get('http://localhost:' + port + '/quit', function(result){
        console.log(result)
    });
}

module.exports = {
    start: start,
    stop: stop
}