const http = require('http');
const querystring = require('querystring');
const util = require('util');

const defaultOptions = {
    hostname: 'localhost',
    port: '8888',
    path: '',
    method: 'POST',
    params: {}
} 

function httpPost(options, callback){
    options = util._extend(defaultOptions, options);

    var req = http.request(options, function (res) {
        var chunks = [];
        res.on('data', function (chunk) {
            chunks.push(chunk);
        });
        res.on('end', function () {
            if(callback) callback({
                status: 'success',
                content: chunks.concat().toString()
            });
        });
    });

    req.on('error', function (e) {
        console.log(e.message);
        if (callback ) callback({
            status: 'failed',
            msg: e.message
        });
    });

    req.write(querystring.stringify(options.params));
    req.end;
}

function httpGet(options, callback){
    options = util._extend(defaultOptions, options);
    options.method = 'GET';
    var url = 'http://' + options.hostname + options.port + '/' + options.path + '?' + querystring.stringify(options.params);
    http.get(url, function(res){
        if(callback) {
            callback({
                status: 'success',
                content: res.resume()
            });
        }
    }).on('err', function(e){
        console.log('request error [get]: ' + url);
        console.log(e);
         if (callback ) callback({
            status: 'failed',
            msg: e.message
        });
    });
}

module.exports = {
    post: httpPost,
    get: httpGet
}
