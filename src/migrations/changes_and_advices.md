# Изменения в versions(определённых миграциях)
## ПРИ СОЗДАНИИ СВОИХ ТИПОВ данных, напр, Enum:
## следует явно прописывать в downgrade удаление типов при откатах
## напр: op.execute("DROP TYPE")  
- alembic init ./<path>/<имя_папки_с_миграциями>
- alemibc revision --autogenerate -m "name_migr" # создать миграцию
### миграцию можно удалить безболезненно, пока она не была прогнана 
### Функция для отката: downgrade(base: до начального состояния | ver: до определённой версии),
- alembic downgrade base | ver
### Функция для повышения версии: upgrade(head: до последней версии | ver: до опред верс) 
- alembic upgrade head | ver
### Можно прописать свой код в миграциях
#### создать пустую миграцию:
- alembic revision

# Изменения в alembic.ini

### script_location = migrations 
- расположение папки с миграциями
### prepend_sys_path = .
- обозначить путь до папки для безошибочных импортов
### смена формата написания миграций
- раскомментировать следующие строчки и pip install black
    - hooks = black
    - black.type = console_scripts
    - black.entrypoint = black
    - black.options = -l 79 REVISION_SCRIPT_FILENAME


# Изменения в versions/env.py
- from config import settings
#### обязательно импортировать все файлы с моделями
#### иначе метаданные будут пустые
- from auth.models import Model # noqa
- from something_else.models Model_2 # noqa | чтобы не удалилось из кода при проверке
- from database import Base
#### смена url db
- config.set_main_option("sqlalchemy.url", settings.DATABASE_URL_psycopg)
                                            # если юзать асинх: ... + "?async_fallback=True"
#### c_s_d позволяет улавливать изменения, например, в параметрах аргументов
- with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            # c_s_d позволяет улавливать изменения, например, в параметрах аргументов
            compare_server_default=True
        )