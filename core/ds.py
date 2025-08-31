"""
- MinHeap: smallest item first (wraps heapq)
- Queue: FIFO using list
"""
import heapq
from typing import Any, List, Optional

class MinHeap:
    def __init__(self) -> None:
        self._heap: List[Any] = []

    def push(self, item: Any) -> None:
        heapq.heappush(self._heap, item)

    def pop(self) -> Optional[Any]:
        if self.is_empty():
            return None
        return heapq.heappop(self._heap)

    def peek(self) -> Optional[Any]:
        if self.is_empty():
            return None
        return self._heap[0]

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def to_list_ordered(self) -> List[Any]:
        tmp = list(self._heap)
        heapq.heapify(tmp)
        out: List[Any] = []
        while tmp:
            out.append(heapq.heappop(tmp))
        return out

class Queue:
    def __init__(self) -> None:
        self._items: List[Any] = []

    def enqueue(self, item: Any) -> None:
        self._items.append(item)

    def dequeue(self) -> Optional[Any]:
        if self.is_empty():
            return None
        return self._items.pop(0)

    def peek(self) -> Optional[Any]:
        if self.is_empty():
            return None
        return self._items[0]

    def is_empty(self) -> bool:
        return len(self._items) == 0