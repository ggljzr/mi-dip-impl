# Deployment notes

* Install Apache2 (some [notes](http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/) for flask)
* Install [wsgi](https://stackoverflow.com/questions/19344252/how-to-install-configure-mod-wsgi-for-py) for Python3
* [Generate cert and set up HTTPS](https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-apache-in-ubuntu-16-04)
* Don't forget to set `secret_key` for flask app in `.wsgi` file
* Set GARAGE_SYSTEM_CONFIG env variable to your app config file (or use default)
* When [SSLOpenSSLConfCmd](https://serverfault.com/questions/698093/invalid-command-sslopensslconfcmd-perhaps-misspelled-or-defined-by-a-module-n) is not working, concat `dhparams.pem` at the end of the cert

More detailed how-to coming soon.
