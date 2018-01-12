# Third-party imports
from aiohttp import ClientSession
from aiohttp.web import Response
from aiohttp_jinja2 import template
from async_timeout import timeout
from peewee import fn
from peewee_async import Manager

# Project imports
from settings import DB_CONNECTION
from models import Record


def database_requests_enabled(function):
    def _wrapped(*args, **kwargs):
        return function(
            *args, **kwargs, db_manager=Manager(DB_CONNECTION)
        )
    return _wrapped


async def raw_response_handle(request):
    return Response(
        text='Hello, {}'.format(request.query.get('name', 'Anonymous'))
    )


@template('index.html')
async def html_response_handle(request):
    return {'name': request.query.get('name', 'Anonymous')}


@database_requests_enabled
async def database_response_handle(_, db_manager):
    return Response(
        text='Random record date: {}\nRecords overall: {}'.format(
            (
                await db_manager.get(Record.select().order_by(fn.Random()))
            ).created_date,
            (
                await db_manager.count(Record.select())
            )
        )
    )


async def service_response_handle(request):
    async with ClientSession() as session:
        async with timeout(10):
            async with session.get(
                'https://httpbin.org/get?text={}'.format(
                    request.query.get('search', 'test')
                )
            ) as response:
                return Response(
                    text=(
                        'Response from httpbin.org: {}'.format(
                            await response.text()
                        )
                    )
                )
