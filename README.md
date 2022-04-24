# Imagier Vagabond project setup

## Local Homebrew setup

Install Python and virtualenv with asdf (with i386 binaries):

```sh
asdf plugin-add python
asdf install python 2.7.18
pip install virtualenv --user
```

```sh
brew install mariadb@10.5
brew services start mariadb@10.5
```

## Install Python dependencies

```sh
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Create MySQL user and database

```
$ mysql
$ # or mysql -p --user=root

mysql> create database imagier;
  create user 'vagabond';
  grant all privileges on imagier.* to vagabond@localhost identified by '******';
```

Import database:

```sh
mysql -p --user=vagabond imagier < backup/imagiervagabond_fr_prod.sql
```

Copy and edit database settings:

```sh
cp imagier/env.py.example imagier/env.py
```

Then edit `env.py` with the correct database connection settings. Once you're done, you should be able to connect to a MySQL prompt with:

```
$ ./manage.py dbshell
mysql> show tables;
```

## Copy static files

Static files must be copied with:

```sh
python manage.py collectstatic
```

This will copy files from the Django admin, other modules, and from `imagier/static` into `public/static`.

The `public` folder contains files that should be served directly by Apache or a file server (rather than through Django).

You can run a simple server:

```sh
cd public
python -m http.server 8001
```

and then configure `imagier/env.py` to:

```
MEDIA_URL = "http://localhost:8001/media/"
STATIC_URL = "/static/"
```

Note: in development, we use the staticfiles app to serve static files from the same origin as the main site.

In a prod environment with uWSGI, it's possible to [serve static files](https://uwsgi-docs.readthedocs.io/en/latest/StaticFiles.html) from the same domain, with the `static-map` parameter:

```
--static-map /static=/path/to/imagiervagabond/public/static
--static-map /media=/path/to/imagiervagabond/public/media
```

## Run the Python application

In the Docker environment, the development server can be started with:

```sh
python ./manage.py runserver localhost:8000
```

In a production environment, you can use any WSGI-compatible web server (Apache, nginx, etc.). They must be configured to launch `imagier/wsgi.py`.

Don't forget to edit `imagier/env.py` to set `DEBUG = False`.

## Remove the thumbnail cache

```
python manage.py thumbnail clear
rm -rf public/media/cache
```

## Admin: make changes to the CKEditor build

We're using CKEditor 5 for the admin rich-text editor, with:

- a custom build defined in `client/ckeditor`;
- output in `static/dist/ckeditor.js`.

This follows the “Advanced setup” guide at https://ckeditor.com/docs/ckeditor5/latest/builds/guides/integration/advanced-setup.html

To rebuild the `ckeditor.js` bundle, you will need Node.js to run those commands:

```sh
npm install
npm run build:ckeditor
```
