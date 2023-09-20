import logging
import xmlrpc.client
import argparse
from functools import partial

from api.data_loaders.sw_data_loader import SWDataLoader
from api.loader_funcs import load_sw_data
from api.url_generators.SW_chr_url_gen import SWChrUrlGen
from settings.environ_handler import env
from odoo_connectors.basic_odoo_connector import BasicOdooConnector
from odoo_updaters.sw_odoo_updater import SWOdooUpdater
from puller import SWPuller

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="pulling swapi data and " "posting to odoo"
    )   #стандартный парсер аргументов
    parser.add_argument("conf_file", type=str, help="path to conf file")
        #Добавляем именованный аргумент в словарь
    args = parser.parse_args() #Парсируем аргументы
    env.read_env(args.conf_file)
    db_url = env("DB_URL")
    db_name = env("DB_NAME")
    username = env("USER_NAME")
    password = env("PASSWORD")

    '''
    xmlrpc-метод использующий xml для передачи запросов через https,
    реализация этой библиотеки для python
     способна анализировать и транслировать ответы, приходящие
     в объекты и прочие структуры данных внутри python 
     
     https://www.odoo.com/documentation/14.0/developer/reference/external_api.html
     
     1. common-endpoint предоставляет вызоовы, 
     не требующие аутентификации
     (аутентификация - удостоверение личности, авториация - проверка прав)
    2. процесс аутентификации
    3. получение доступа к моделям odoo для вызовов к ним, 
    через execute_kw функцию удаленного вызова базы данных
    
          
     
     
    '''
    common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(db_url))
    uid = common.authenticate(db_name, username, password, {})
    models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(db_url))

    pull_logger = logging.getLogger("**SW_Logger**") #Получение объекта
                                                     # встроенного логировщика
                                                    # из стандартной библиотеки

    pull_logger.setLevel(logging.INFO) # минимальный уровень(debug игнорируется)
    handler = logging.FileHandler(env("LOGGER_FILE"))
    pull_logger.addHandler(handler)

    connector = BasicOdooConnector(
        db_url, db_name, username, password, uid, common, models
    )
    # просто хранилище данных о соединении

    partial_load_func = partial(load_sw_data, loader=SWDataLoader)
    #нам нужно будет использовать эту функцию так,
    # чтобы один из её аргументов был итератором, а другой был постоянный
    # на каждом вызове. partial(как я понял) применяет часть аргументов к
    # функции, упрощая запись аргументов, оставшиеся аргументы пердаются с начала,
    # аргументы вызова partial добавляются с конца, или именованными

    url_gen = SWChrUrlGen()
    threads_cnt = int(env("THREADS_PULL_CNT"))
    db_upd = SWOdooUpdater(connector, pull_logger)
                #конструируем объект апдейтера базы данных

    puller = SWPuller(url_gen, db_upd, threads_cnt, partial_load_func)
    #простая оболочка - это было не очень удачное решение
    puller.pull_data()
    pull_logger.info("Скачивание завершено")
