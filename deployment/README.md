# Deployment notes

* First make sure all required Python packages are installed
* Install Apache2 (some [notes](http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/) for flask)
* Install [wsgi](https://stackoverflow.com/questions/19344252/how-to-install-configure-mod-wsgi-for-py) for Python3
* [Generate cert and set up HTTPS](https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-apache-in-ubuntu-16-04)
* Set `GARAGE_SYSTEM_CONFIG` env variable to your app config file (or use default)
* When [SSLOpenSSLConfCmd](https://serverfault.com/questions/698093/invalid-command-sslopensslconfcmd-perhaps-misspelled-or-defined-by-a-module-n) is not working, concat `dhparams.pem` at the end of the cert
* Strong HTTPS [config](https://raymii.org/s/tutorials/Strong_SSL_Security_On_Apache2.html)
* db access -- [set app directory](https://stackoverflow.com/questions/27753308/how-to-set-permissions-for-apache2-to-let-user-create-or-edit-files-in-var-www) (eg. `/var/www/my-app/`) owner to `www-data` and set appropriate read/write access with `chmod`
* Add user that runs the web app (usually `www-data`) to `gammu` group so they can inject new messages to Gammu-smsd
* Gammu-smsd config in `/etc/gammu-smsdrc`

## Setting access to application files

Allow access to `/var/www` directory, where application is placed:

```
$ sudo chown -R www-data:www-data /var/www
```

Allow read/write access to `user_config.ini` and `app.db` (database file):

```
# set user group
$ sudo chown root:www-data /path/to/user_config.ini
$ sudo chown root:www-data /path/to/app.db
# allow read/write/exec
$ sudo chmod 660 /path/to/user_config.ini
$ sudo chmod 660 /path/to/app.db
```

Also copy `garage_system.wsgi` to the the root of the application and set it's execute bit.

Addd `www-data` user to `gammu` group so application can add messages to `gammu-smsd` with `gammu-smsd-inject`:

```
sudo usermod -a -G gammu www-data
```

## Install WSGI module for Python 3

```
$ sudo apt-get install libapache2-mod-wsgi-py3
```

## Enable Apache2 modules

For some reason Apache2 installed on Raspberry Pi 3 didn't have modules `mod_ssl` and `headers` enabled by default. These should come with default Apache2 package, so all is needed is to enable them:

```
$ sudo a2enmod ssl
$ sudo a2enmod headers
```

## Generate self-signed certificate

```
$ sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt
```

## Apache SSL config

Copy `ssl-params.conf` to `/etc/apache2/conf-available`, then create symbolic link (`ln -s`) for it in `/etc/apache2/conf-enabled`.

## Apache site configs

Simply copy `000-default.conf` a `default-ssl.conf` into `/etc/apache2/sites-available` and create symbolic links (if they aren't created already) in `/etc/apache2/sites-enabled`.

In `default-ssl.conf` make sure it's pointing to the right directory, WSGI script (you may want to move `garage_system.wsgi` to the root of the application), and certificates. Also make sure `garage_system.wsgi` sets the right directory.

## Gammu SMSD config

Default config lives in `/etc/gammu-smsdrc`. You can use config in this repo to replace it.