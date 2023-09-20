from abc import abstractmethod


class ABCUrlGenerator:
    @abstractmethod
    def generate(self):
        pass
