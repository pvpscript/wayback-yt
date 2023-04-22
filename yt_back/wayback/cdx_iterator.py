from typing import List

class CDXIterator:
    def __init__(self, cdx_data: List[List[str]], *, delimiter: str = '|'):
        self._cdx_data = cdx_data
        self._delimiter = delimiter
        self._index = 0

    @property
    def delimiter(self):
        return self._delimiter

    def __iter__(self):
        self._index = 0

        return self

    def __next__(self) -> str:
        try:
            data = self._cdx_data[self._index]
            self._index += 1

            return self._delimiter.join(data)
        except IndexError:
            raise StopIteration
