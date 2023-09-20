from multiprocessing.pool import ThreadPool
from typing import Callable

from api.url_generators.abc_url_generator import ABCUrlGenerator
from odoo_updaters.abs_odoo_updater import ABCOdooUpdater


class SWPuller:
    def __init__(
            self,
            url_generator: ABCUrlGenerator,
            db_updater: ABCOdooUpdater,
            thread_cnt: int,
            load_func: Callable,
    ):
        self.thread_cnt = thread_cnt
        self.url_generator = url_generator
        self.db_updater = db_updater
        self.load_func = load_func

    def pull_data(self):
        with ThreadPool(self.thread_cnt) as th_pool:
            # ThreadPool нужно обязательно закрывать для высвобождения ресурсов
            #Я использую потоки а не процессы для одного подключения к БД
            for data_piece in th_pool.imap_unordered(

                    self.load_func, self.url_generator.generate()
            ):
                self.db_updater.update(data_piece) #вызывается по мере поступления результатов из load_func
#В генераторе можно было бы указать, что он возвращает именно генератор строк -> Generator[str, None, None]: