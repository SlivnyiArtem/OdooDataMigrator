from api.service_funcs import load_people_cnt
from api.url_generators.abc_url_generator import ABCUrlGenerator
from settings.environ_handler import env


class SWChrUrlGen(ABCUrlGenerator):
    def __init__(self):
        super(SWChrUrlGen, self).__init__()

    def generate(self):
        cnt = load_people_cnt(env("PEOPLE_URL")) + 1
        for i in range(1, cnt):
            yield str(i)
