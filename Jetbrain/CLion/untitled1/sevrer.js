var multiparty = require('multiparty'),
    http = require('http'),
    util = require('util'),
    path = require('path'),
    fs = require('fs'),
    PORT = 12345;

http.createServer(function(req, res) {

    if (req.url == './upload' && req.method.toLowerCase() == 'post') {
        var form = new formidable.IncomingForm();
        form.parse(req, function(err, fields, files) {
            res.writeHead(200, {'content-type': 'text/plain'});
            res.write('received upload:\n\n');
            res.end(sys.inspect({fields: fields, files: files}));
        });
    }

    var filePath = '.' + req.url;
    if (filePath == './')
        filePath = './index.html';

    var extname = path.extname(filePath);
    var consentType = 'text/html';
    switch (extname) {
        case '.js':
            consentType = 'text/javascript';
            break;
        case '.css':
            consentType = 'text/css';
            break;
    }

    fs.exists(filePath, function (exists) {

        if (exists) {
            fs.readFile(filePath, function (error, content) {
                if (error) {
                    res.writeHead(500);
                    res.end();
                }
                else {
                    res.writeHead(200, {'Content-Type': consentType});
                    res.end(content, 'utf-8');
                }
            });
        }
        else {
            res.writeHead(404);
            res.end();
        }
    });

});