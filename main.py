# Standard imports
from os.path import dirname, realpath, join

# Project imports
from models import Record
from settings import DB_CONNECTION
from views import raw_response_handle, html_response_handle, \
    database_response_handle, service_response_handle

# Third-party imports
from aiohttp.web import Application, run_app
from aiohttp_jinja2 import setup as jinja2_setup
from jinja2 import FileSystemLoader


# TODO: TYPO: "Error, trying to run delete coroutinewith wrong query class"


def main():
    template_root = join(dirname(realpath(__file__)), 'templates')

    DB_CONNECTION.connect()

    DB_CONNECTION.create_tables((Record,), safe=True)

    Record.delete().execute()
    Record.insert_many(({} for _ in range(500))).execute()

    DB_CONNECTION.close()

    DB_CONNECTION.set_allow_sync(False)

    try:
        application = Application()
        jinja2_setup(application, loader=FileSystemLoader(template_root))

        application.router.add_get('/', raw_response_handle)
        application.router.add_get('/template', html_response_handle)
        application.router.add_get('/database', database_response_handle)
        application.router.add_get('/service', service_response_handle)

        run_app(application)
    except Exception as exception:
        # TODO: error notification logic
        raise exception
    finally:
        DB_CONNECTION.close()


if __name__ == '__main__':
    main()
