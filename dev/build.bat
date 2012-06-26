@echo off
type styles\*.css > ..\ui\css\geostore-ui.css
type ..\ui\js\jquery-1.6.1.min.js ..\ui\js\jquery.tmpl.min.js ..\ui\js\jquery.cookie.js ..\ui\js\json2.js ..\ui\js\jquery.expander.js ..\..\services\snowblozm\js\Snowblozm.class.js ..\..\services\firespark\jquery\dev\jquery-firespark.js init.js geostore\*.js > ..\ui\js\geostore-ui.js
pause
