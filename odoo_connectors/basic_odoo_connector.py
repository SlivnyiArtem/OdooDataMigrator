from xmlrpc.client import ServerProxy


class BasicOdooConnector:
    def __init__(
        self,
        db_url: str,
        db_name: str,
        db_username: str,
        db_password: str,
        db_uid,
        db_common: ServerProxy,
        db_models: ServerProxy,
    ):
        self.db_url = db_url
        self.db_name = db_name
        self.db_username = db_username
        self.db_password = db_password
        self.db_uid = db_uid
        self.db_common = db_common
        self.db_models = db_models
