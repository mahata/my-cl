# cl-example

## What is this?

It's a toy service which resizes the image of a given URL. As it's just a toy, it should *not* be deployed to production.

Here's [the very brief architecture](http://www.plantuml.com/plantuml/uml/HOnD2i8m64JtESLSm0ja8TL5GH4jbU8wj1yKcYRw_TnVKmdTpflt6j70QcjqWn3ZS4GRWomUf-w2dZv6ecwR2ZjpNeWzkY02dGb3VuDcl3cF9B8VIyp_V3LEk3uVT_TN2tjbtY8jwJWZfAdgjUWQIfEjyGi0):

```
     ┌────┐          ┌─────┐                 ┌──────┐                   ┌──────┐
     │User│          │Flask│                 │Broker│                   │Worker│
     └─┬──┘          └──┬──┘                 └──┬───┘                   └──┬───┘
       │  API Request   │                       │                          │    
       │ ──────────────>│                       │                          │    
       │                │                       │                          │    
       │                │Pass the URL to process│                          │    
       │                │───────────────────────>                          │    
       │                │                       │                          │    
       │  Return JSON   │                       │                          │    
       │ <──────────────│                       │                          │    
       │                │                       │                          │    
       │                │                       │ Fetch and process the URL│    
       │                │                       │ ─────────────────────────>    
     ┌─┴──┐          ┌──┴──┐                 ┌──┴───┐                   ┌──┴───┐
     │User│          │Flask│                 │Broker│                   │Worker│
     └────┘          └─────┘                 └──────┘                   └──────┘
```

## How to run this app?

If you have `docker-compose` installed locally, `docker-compose up` will boot-up everything needed for the service.

API endpoints for this app are:

* `/ping` (GET: for the availability check)
* `/api/v1/resize` (POST: for generating a resized image)

For example, `/api/v1/resize` works like following with `curl`:

```
$ curl -X POST http://localhost:5000/api/v1/resize -d 'url=https%3A%2F%2Fmahata.gitlab.io%2Fimg%2Ffavicon.png'
{
  "data": [
    {
      "output": "http://localhost:5000/img/_NEFIkFTi"
    }
  ],
  "status": "OK"
}
```

`/api/v1/resize` takes the `url` parameter, which is a url-encoded string (URL) of the image to resize. This endpoint returns JSON that contains a URL that provides the resized image.

## How to test this app?

Assuming your app is running with `docker-compose`, you can run unittests for this app by:

```
$ docker exec -ti $(docker ps | grep flask | cut -d ' ' -f 1) python web_test.py
```

## Some things to be considered

* `Dockerfile` runs `apt-updage` and `apt-get`, which means the Dockerfile can't create a Docker image that is idempotent.
* `Celery Broker` is `Redis`, but there are other options as well:
  * `Amazon SQS` is a promising choice, as we don't need to manage the queue (but we'll be locked into AWS).
  * `RabbitMQ` is also an alternative.
    * `RabbitMQ` is very reliable when it comes to delivering messages. On the other hand, `Redis` works fast, but it cuts slow clients. Although this is a bit old, this article explains the characteristics of various [Message Queues](https://bravenewgeek.com/dissecting-message-queues/).
* This app doesn't care about the `state` of the resizing process.
  * There exists a timing when the resizing task is submitted to Celery, but the actual resized image isn't ready.
* This app doesn't care about the `rate limit` of the resizing process.
  * This app can crash when there are tons of resizing requests.
* This app is vulnerable regarding the way we use ImageMagick.
  * By default, ImageMagick doesn't allow fetching images via HTTP/HTTPS because there are malicious images in WWW.
* This app serves images from Flask, but it should be served by the webserver (or CDN is even better).
* This app doesn't distinguish the image types. As a result, it can't tell which image type the server is returning (e.g., `.jpg`, `.png`, `.gif`, etc.)
* This app returns a randomized file name for the resized image, but we don't care about the collision of the file names.

## How to develop this app locally?

Some prerequisites are:

* Imagemagick
* Redis

This app is expected to be developed in `pyenv`. If you don't have `pyenv` and `pyenv-virtualenv`:

```
$ brew install pyenv pyenv-virtualenv
$ vim ~/.zshrc

# Add following lines
export PYENV_ROOT="$HOME/.pyenv"
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Run following commands to install the Python interpreter and the packages needed for the app:

```
$ pyenv install 3.8.1
$ pyenv virtualenv 3.8.1 cl-example
$ pyenv local cl-example
$ pip install -r requirements.txt
```

Once they are installed, you can do followings:

```
# (To run Celery)
$ celery -A celery_tasks worker --loglevel=info

# (To run Flask)
$ python web.py
```
