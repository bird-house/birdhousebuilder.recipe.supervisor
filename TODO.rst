Todo list
*********

Bugs
====

* supervisor hostname config does not always work:
Starting supervisord:
Error: Could not determine IP address for hostname humbold, please try setting an explicit IP address in the "port" setting of your [inet_http_server] section.  For example, instead of "port = 9001", try "port = 127.0.0.1:9001."
For help, use /home/pingu/anaconda/bin/supervisord -h

Features
========

* maybe load supervisor from pypi instead of conda
* run supervisor on startup
http://supervisord.org/running.html#running-supervisord-automatically-on-startup
* run supervisor monitor behing nginx proxy
http://serverfault.com/questions/591811/nginx-proxy-pass-mangled-relative-links-upstream
http://serverfault.com/questions/568317/supervisord-inet-http-server-behind-nginx#568908


