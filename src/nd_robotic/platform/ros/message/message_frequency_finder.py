# message_frequency_finder_min.py
# Python 3.13 — robust 99% interval for sensor frequency using header.stamp only.
# Keep all comments in English only.

from __future__ import annotations

import gzip
import math
import re
from statistics import median
from typing import Dict, Iterable, List, Optional, TextIO, Tuple


class MessageFrequency99CI:
    def __init__(self, path: str, topics: List[str]):
        self._path = path
        self._topics = list(topics)
        self._topics_set = set(topics)

        # Accept both "topic:" and "# topic:" lines (with arbitrary spacing/quotes).
        self._topic_re = re.compile(r'^\s*(?:#\s*)?topic:\s*"?([^"\n]+)"?\s*$')

        # stamp fields inside header -> stamp.
        self._secs_re = re.compile(r'^\s*secs:\s*(-?\d+)\s*$')
        self._nsecs_re = re.compile(r'^\s*nsecs:\s*(-?\d+)\s*$')

    def _open_text(self) -> TextIO:
        if self._path.endswith(".gz"):
            return gzip.open(self._path, "rt", encoding="utf-8", errors="ignore")
        return open(self._path, "r", encoding="utf-8", errors="ignore")

    def _stream_header_stamps(self, fp: TextIO, targets: set[str]) -> Iterable[Tuple[str, float]]:
        """
        Stream parse: yield (topic, ts) using ONLY header.stamp (secs+nsecs) once per message.
        """
        current_topic: Optional[str] = None
        in_header = False
        in_stamp = False
        have_secs = False
        have_nsecs = False
        secs = 0
        nsecs = 0

        for raw in fp:
            line = raw.rstrip("\n")

            topic_match = self._topic_re.match(line)
            if topic_match is not None:
                detected_topic = topic_match.group(1).strip()
                if detected_topic in targets:
                    current_topic = detected_topic
                else:
                    current_topic = None

                # Reset state whenever a topic marker appears.
                in_header = False
                in_stamp = False
                have_secs = False
                have_nsecs = False
                secs = 0
                nsecs = 0
                continue

            if current_topic is None:
                continue

            stripped = line.strip()

            if stripped == "header:":
                in_header = True
                in_stamp = False
                have_secs = False
                have_nsecs = False
                secs = 0
                nsecs = 0
                continue

            if not in_header:
                continue

            if stripped == "stamp:":
                in_stamp = True
                have_secs = False
                have_nsecs = False
                secs = 0
                nsecs = 0
                continue

            if not in_stamp:
                continue

            secs_match = self._secs_re.match(stripped)
            if secs_match is not None:
                try:
                    secs = int(secs_match.group(1))
                    have_secs = True
                except ValueError:
                    have_secs = False

            nsecs_match = self._nsecs_re.match(stripped)
            if nsecs_match is not None:
                try:
                    nsecs = int(nsecs_match.group(1))
                    have_nsecs = True
                except ValueError:
                    have_nsecs = False

            if have_secs and have_nsecs:
                ts = float(secs) + float(nsecs) * 1e-9
                yield current_topic, ts
                # Emit only once per message.
                in_stamp = False

    @staticmethod
    def _percentile_sorted(values_sorted: List[float], p: float) -> float:
        if not values_sorted:
            return math.nan
        if p <= 0.0:
            return values_sorted[0]
        if p >= 1.0:
            return values_sorted[-1]
        k = (len(values_sorted) - 1) * p
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return values_sorted[int(k)]
        return values_sorted[f] + (values_sorted[c] - values_sorted[f]) * (k - f)

    def compute(self) -> List[Dict[str, object]]:
        stats: Dict[str, Dict[str, object]] = {}
        for topic in self._topics:
            stats[topic] = {
                "topic": topic,
                "count": 0,
                "bad_dt": 0,
                "t_min": None,
                "t_max": None,
                "prev": None,
                "freqs": [],
            }

        with self._open_text() as fp:
            for topic, ts in self._stream_header_stamps(fp, self._topics_set):
                s = stats[topic]
                s["count"] = int(s["count"]) + 1

                t_min = s["t_min"]
                t_max = s["t_max"]
                if t_min is None or ts < float(t_min):
                    s["t_min"] = ts
                if t_max is None or ts > float(t_max):
                    s["t_max"] = ts

                prev = s["prev"]
                if prev is not None:
                    dt = ts - float(prev)
                    if dt > 0.0:
                        freqs: List[float] = s["freqs"]  # type: ignore[assignment]
                        freqs.append(1.0 / dt)
                    else:
                        s["bad_dt"] = int(s["bad_dt"]) + 1

                s["prev"] = ts

        rows: List[Dict[str, object]] = []
        for topic in sorted(stats.keys()):
            s = stats[topic]
            freqs_sorted = sorted(s["freqs"])  # type: ignore[arg-type]
            f_med = median(freqs_sorted) if freqs_sorted else math.nan
            f_lo = self._percentile_sorted(freqs_sorted, 0.005) if freqs_sorted else math.nan
            f_hi = self._percentile_sorted(freqs_sorted, 0.995) if freqs_sorted else math.nan

            rows.append({
                "topic": topic,
                "count": int(s["count"]),
                "t_min": float(s["t_min"]) if s["t_min"] is not None else math.nan,
                "t_max": float(s["t_max"]) if s["t_max"] is not None else math.nan,
                "f_med": float(f_med),
                "ci99_lo": float(f_lo),
                "ci99_hi": float(f_hi),
                "bad_dt": int(s["bad_dt"]),
            })

        return rows

    def print_summary(self) -> None:
        rows = self.compute()
        header = (
            f"{'topic':45s} "
            f"{'count':>9s} "
            f"{'t_min':>12s} "
            f"{'t_max':>12s} "
            f"{'f_med(Hz)':>12s} "
            f"{'CI99_low':>12s} "
            f"{'CI99_high':>12s} "
            f"{'bad_dt':>7s}"
        )
        print(header)
        print("-" * len(header))
        for r in rows:
            print(
                f"{str(r['topic']):45s} "
                f"{int(r['count']):9d} "
                f"{float(r['t_min']):12.3f} "
                f"{float(r['t_max']):12.3f} "
                f"{float(r['f_med']):12.2f} "
                f"{float(r['ci99_lo']):12.2f} "
                f"{float(r['ci99_hi']):12.2f} "
                f"{int(r['bad_dt']):7d}"
            )


def main() -> None:
    # Hardcoded file path (inside the file, as requested).
    path = "/home/donkarlo/Dropbox/repo/nd_sociomind_project/data/experiment/composite/child/members/oldest/robotic_group/composite/children/composite/children/uav1/structure/kind/mind/memory/explicit/long_term/episodic/auto_biographical/event_specific_knowledge/normal/mixed_traces.yaml"

    # Hardcoded topic names (inside the file, as requested).
    # Important: these must match EXACTLY what appears in the YAML ("topic:" lines),
    # otherwise count stays 0 and frequencies will be NaN.
    topics = [
        "/uav1/odometry/odom_gps",
        "/uav1/rplidar/scan",
    ]

    mf = MessageFrequency99CI(path=path, topics=topics)
    mf.print_summary()


if __name__ == "__main__":
    main()