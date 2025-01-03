from typing import NamedTuple, Any, Dict, Optional, Iterator, Set, List, Iterable
from collections import deque


class Pair(NamedTuple):
    key: Any
    value: Any


class HashTable:
    @classmethod
    def from_dict(cls, dictionary: Dict[Any, Any], capacity: Optional[int] = None) -> 'HashTable':
        hash_table = cls(capacity or len(dictionary))
        for key, value in dictionary.items():
            hash_table[key] = value
        return hash_table

    def __init__(self, capacity: int = 8, load_factor_threshold: float = 0.6) -> None:
        if capacity < 1:
            raise ValueError("Capacity must be a positive number")
        if not (0 < load_factor_threshold <= 1):
            raise ValueError("Load factor must be a number between (0, 1]")
        self._load_factor_threshold = load_factor_threshold
        self._buckets = [deque() for _ in range(capacity)]
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.load_factor >= self._load_factor_threshold:
            self._resize()

        bucket = self._buckets[self._index(key)]
        for index, pair in enumerate(bucket):
            if pair.key == key:
                bucket[index] = Pair(key, value)
                return
        bucket.append(Pair(key, value))
        self._size += 1

    def __getitem__(self, key: Any) -> Any:
        bucket = self._buckets[self._index(key)]
        for pair in bucket:
            if pair.key == key:
                return pair.value
        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        bucket = self._buckets[self._index(key)]
        for index, pair in enumerate(bucket):
            if pair.key == key:
                del bucket[index]
                self._size -= 1
                return
        raise KeyError(key)

    def __contains__(self, key: Any) -> bool:
        try:
            self[key]
        except KeyError:
            return False
        return True

    def __iter__(self) -> Iterator[Any]:
        yield from self.keys

    def __str__(self) -> str:
        res = []
        for key, value in self.pairs:
            res.append(f"{key!r}: {value!r}")
        return "{" + ", ".join(res) + "}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.from_dict({str(self)})"

    def __eq__(self, other: 'HashTable') -> bool:
        if not isinstance(other, HashTable):
            return False
        if self is other:
            return True
        return self.pairs == other.pairs

    def __or__(self, other: 'HashTable') -> 'HashTable':
        if not isinstance(other, HashTable):
            raise TypeError(f"unsupported operand type(s) for |: 'HashTable' and '{type(other).__name__}'")
        pairs = dict(self.pairs)
        pairs.update(other.pairs)

        return HashTable.from_dict(pairs)

    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        if key in self:
            return self[key]
        return default

    def copy(self) -> 'HashTable':
        return HashTable.from_dict(dict(self.pairs), self.capacity)

    def clear(self) -> None:
        self._buckets = [deque() for _ in range(self.capacity)]
        self._size = 0

    def update(self, iterable: Iterable[tuple[Any, Any]] = (), /, **kwargs: Any) -> None:
        for i, sequence in enumerate(iterable):
            if len(sequence) != 2:
                raise ValueError(
                    f"hashtable update sequence element #{i} has length {len(sequence)}; 2 is required"
                )
            self[sequence[0]] = sequence[1]

        for key, value in kwargs.items():
            self[key] = value

    @property
    def load_factor(self) -> float:
        return len(self) / self.capacity

    @property
    def capacity(self) -> int:
        return len(self._buckets)

    @property
    def pairs(self) -> Set[Pair]:
        return {pair for bucket in self._buckets for pair in bucket}

    @property
    def values(self) -> List[Any]:
        return [pair.value for bucket in self._buckets for pair in bucket]

    @property
    def keys(self) -> Set[Any]:
        return {pair.key for bucket in self._buckets for pair in bucket}

    def _index(self, key: Any) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        copy = HashTable(self.capacity * 2)
        for key, value in self.pairs:
            copy[key] = value
        self._buckets = copy._buckets
