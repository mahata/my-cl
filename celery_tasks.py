from celery import Celery

from wand.image import Image
from wand.display import display

import os


celery_backend = os.environ.get('CELERY_BACKEND', 'redis://localhost')
celery_broker = os.environ.get('CELERY_BROKER', 'redis://localhost')

app = Celery('celery_tasks',
             backend=celery_backend,
             broker=celery_broker)


@app.task
def resize(url, output_file):
    # FixMe: It's better to split the phase into 2 parts:
    #   1. Fetch the image
    #   2. Resize the image
    # FixMe: What if the web server doesn't return 2xx status code?
    # FixMe: It doesn't need to fetch the same URL multiple times
    # FixMe: `url` passed to the method may not be the URL of an image

    with Image(filename=url) as img:
        with img.clone() as i:
            i.resize(100, 100)  # ToDo: Parameterize
            i.save(filename=output_file)

    return True
