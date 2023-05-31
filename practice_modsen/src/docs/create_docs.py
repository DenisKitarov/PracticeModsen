from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from src.docs.schemas import *
import json
from src.config.cfg_parser import get_config

config = get_config('config.ini')
docs_config = config['docs']


def load_docstrings(spec, app):
    """ Загружаем описание API.

    :param spec: объект APISpec, куда загружаем описание функций
    :param app: экземпляр Flask приложения, откуда берем описание функций
    """
    with app.app_context():
        for fn_name in app.view_functions:
            if fn_name == 'static':
                continue
            print(f'Загружаем описание для функции: {fn_name}')
            view_fn = app.view_functions[fn_name]
            spec.path(view=view_fn)


def create_tags(spec):
    """ Создаем теги.

    :param spec: объект APISpec для сохранения тегов
    """
    tags = [{'name': 'frontend', 'description': 'frontend webpage'},
            {'name': 'API', 'description': 'api endpoint'}]

    for tag in tags:
        print(f"Добавляем тег: {tag['name']}")
        spec.tag(tag)


def get_apispec(app):
    """ Формируем объект APISpec.

    :param app: объект Flask приложения
    """
    spec = APISpec(
        title="Simple Search Engine",
        version="1.0.0",
        openapi_version="3.0.3",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    spec.components.schema("SearchPageSchema", schema=SearchPageSchema)
    spec.components.schema("SearchParametersSchema",
                           schema=SearchParametersSchema)
    spec.components.schema("SearchResponseSchema", schema=SearchResponseSchema)
    spec.components.schema("DeleteParametersSchema",
                           schema=DeleteParametersSchema)
    spec.components.schema("DeleteSuccessSchema", schema=DeleteSuccessSchema)
    spec.components.schema("DeleteErrorSchema", schema=DeleteErrorSchema)

    spec.path

    create_tags(spec)

    load_docstrings(spec, app)

    write_json_file(spec)

    return spec


def write_json_file(spec: APISpec):
    """ Экспортируем объект APISpec в Json файл.
    :param spec: объект APISpec
    """
    with open(docs_config['docs_path'], 'w') as file:
        json.dump(spec.to_dict(), file, indent=4, ensure_ascii=True,)
    print(f"Документация сохранена по пути {docs_config['docs_path']}")
