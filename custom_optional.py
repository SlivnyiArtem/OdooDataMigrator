from typing import Optional


class CustomOptional:
    def __init__(
        self,
        status: int,
        data: Optional,
        exc_msg: Optional[str],
        data_id: Optional[int],
    ):
        self.status = status
        self.exception = exc_msg
        self.data = data
        self.data_id = data_id
