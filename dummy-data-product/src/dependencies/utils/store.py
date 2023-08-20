import json
from typing import Any, Dict, Iterator


class Store:
    """
    This is a naive implementation to store the data in a storage,
    ideally it should be a separate library which should be able to interact with S3, SFTP, Azure etc
    to write the data to a datastore.
    """

    def __init__(self, path: str):
        self.path = path

    def save(self, data: Dict[str, Any]) -> int:
        with open(f"{self.path}", "ab") as f:
            bytes_written = f.write(f"{json.dumps(data)}\n".encode("utf-8"))
        return bytes_written

    def read(self) -> Iterator[str]:
        with open(f"{self.path}", "rb") as f:
            for line in f:
                yield line.decode()
