"use strict";

var packager = require('electron-packager');

var platform = 'win32';
var arch = 'ia32,x64';

var options = {
	arch: arch,
	dir: __dirname,
	platform: platform,
	asar: true,
	name: 'Tmx Tools',
	out: __dirname+ '/releases',
	overwrite: true,
	version: '1.2.2',
	ignore: [ 'build-elec.js',
			  'README.md',
			  'releases',
              'PyInstaller-3.2',
              'main.exe',
              'port.txt',
              '',
			  '.DS_Store',
			  'tmx11.dtd',
			  'tmx14.dtd']
};

packager(options, function done_callback (err, appPaths) {
	if(err) {
		console.log(err);
	} else {
		console.log('package success: ' + appPaths);
	}
})
