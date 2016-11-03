const http = require('http');
const querystring = require('querystring');
const util = require('util');

const defaultOptions = {
    hostname: 'localhost',
    port: 8888,
    path: '',
    method: 'POST',
    params: {}
} 

module.exports = function(options, callback){
    console.log(options)
    options = util._extend(defaultOptions, options);
    console.log(options);


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
        })
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

