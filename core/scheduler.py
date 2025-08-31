from datetime import timedelta, date
from typing import List, Tuple, Optional
from core.data_manager import load_settings
from core.ds import MinHeap, Queue
from core.utils import status_label

class Scheduler:
    def __init__(self):
        settings = load_settings()
        self.weather_delay_days: int = int(settings.get("weather_delay_days", 0))
        self._heap = MinHeap()          # (effective_date, seq, crop)
        self._fifo = Queue()            # FIFO for NORMAL items
        self._crops: List[object] = []  # keep for rebuilds
        self._seq: int = 0              # tiebreaker

    def _effective_date(self, crop) -> date:
        base = getattr(crop, "harvest_date")  # datetime
        return (base.date() + timedelta(days=self.weather_delay_days))

    def _next_seq(self) -> int:
        self._seq += 1
        return self._seq

    def set_weather_delay(self, days: int) -> None:
        self.weather_delay_days = int(days or 0)
        self._heap = MinHeap()
        self._fifo = Queue()
        seq = 0
        for c in self._crops:
            eff = self._effective_date(c)
            seq += 1
            self._heap.push((eff, seq, c))
            if status_label(eff) == "NORMAL":
                self._fifo.enqueue((eff, seq, c))
        self._seq = seq

    def add_crop(self, crop) -> None:
        self._crops.append(crop)
        eff = self._effective_date(crop)
        self._heap.push((eff, self._next_seq(), crop))
        if status_label(eff) == "NORMAL":
            self._fifo.enqueue((eff, self._seq, crop))

    def remove_crop(self, crop_name: str) -> None:
        self._crops = [c for c in self._crops if c.name != crop_name]
        self.set_weather_delay(self.weather_delay_days)

    def next_to_harvest(self) -> Optional[object]:
        item = self._heap.peek()
        if item:
            _, _, crop = item
            return crop
        return None

    def get_schedule(self) -> List[Tuple[date, object]]:
        triples = self._heap.to_list_ordered()
        return [(d, c) for (d, _seq, c) in triples]

    def get_normal_fifo(self) -> List[Tuple[date, object]]:
        return [(d, c) for (d, _seq, c) in list(self._fifo._items)]