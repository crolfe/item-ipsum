import uuid


class NotFoundError(KeyError):
    ...


class BaseDB:
    def insert(self, data, pk=None):
        raise NotImplementedError  # pragma: no cover

    def get(self, pk):
        raise NotImplementedError  # pragma: no cover

    def delete(self, pk):
        raise NotImplementedError  # pragma: no cover

    def list(self, start=None, amount=None):
        raise NotImplementedError  # pragma: no cover

    def count(self) -> int:
        raise NotImplementedError  # pragma: no cover


class InMemoryDB(BaseDB):
    def __init__(self):
        self._items = {}

    def insert(self, data, pk=None) -> str:
        if not pk:
            pk = uuid.uuid4().hex

        self._items[pk] = data

        return pk

    def count(self) -> int:
        return len(self._items)

    def get(self, pk):
        try:
            return self._items[pk]
        except KeyError:
            raise NotFoundError

    def list(self):
        items = []
        for key, item in self._items.items():
            items.append(dict(pk=key, **item))

        return items

    def delete(self, pk):
        self._items.pop(pk, None)
        return True
