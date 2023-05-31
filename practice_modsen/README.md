
# Simple Search Engine

Очень простой поисковик по текстам документов. Данные хранятся в БД Postgres, поисковый индекс в Elasticsearch.

## Предварительный шаг

Перед установкой поисковика необходимо установить:

```diff
    python 3.9
    Postgres 14
    Elasticsearch 8.7.0
```

Скрипты инициализации БД находятся в папке [\database\postgres](https://github.com/mmm-PC/simple-search-engine/tree/master/database/postgres)

Для Elasticsearch необходимо отключить HTTPS для текущей версии поисковика
## Установка

____Для установки необходимо:____

- Клонировать репозиторий

```bash
  git clone https://github.com/mmm-PC/simple-search-engine
```

- Go to the project directory

```bash
  cd my-project
```

- Установить необходимые зависимости с помощью команд

```bash
  py -3.9 -m venv .venv
  .\.venv\Scripts\activate.bat
  pip install -r requirements.txt
```
или с помощью файла `setup_enviroment.bat`

- Указать в файле `config.ini` необходимые параметры подключения к БД Postgres:
```ini
[postgres]
host = localhost                                //адрес сервера БД
database =  simple_search_engine_db             //название БД
user = simple_search_engine_owner               //имя пользователя
password = Very!Strong1Password0                //пароль
```
параметры подключения к индексу Elasticsearch:
```ini
[elasticsearch]
host = localhost                                //адрес сервера БД
port = 9200                                     //порт         
scheme = http                                   //схема подключения (http/https)
```
а также параметры индекса:
```ini
[index]
name-1 = simple_search_engine_v1
name-2 = simple_search_engine_v2
alias = simple_search_engine
```
## Запуск

Запуск осуществляется с помощью команд
```bash
  .\.venv\Scripts\activate.bat
  python .\main.py
```
или с помощью файла `run.bat`

Предварительно должен быть запущен сервер БД Postgres и Elasticsearch

В файле `main.py` при необходимости раскоментировать функции `populate_db(api, путь_к_файлу_с_данными.csv)` и `make_index(api)`
```python
if __name__ == "__main__":
    api = init()                
    # populate_db(api, "database\\data\\posts.csv")           # Заполнение БД
    # make_index(api)                                         # Создание индекса Elasticsearch

    main(api)
```

## Документация

После запуска API, документация в формате OpenAPI доступна по адресу [http://127.0.0.1:12800/docs](http://127.0.0.1:12800/docs)


## API Reference

#### Поиск записей

```http
  GET /api/search?q=${q}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `q` | `string` | **Required**. Поисковый запрос |

#### Удаление записи

```http
  DELETE /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `integer` | **Required**. Индекс документа |


## Демо

Демонстрационная страница после запуска API находится по адресу [http://127.0.0.1:12800/search](http://127.0.0.1:12800/search)
