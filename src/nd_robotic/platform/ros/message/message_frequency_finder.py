# message_frequency_finder_min.py
# Python 3.13 — robust 99% interval for sensor frequency using header.stamp only.
# Keep all comments in English only.

import sys, gzip, re, math
from statistics import median
from typing import List, TextIO


class MessageFrequency99CI:
    def __init__(self, path: str, topics: List[str]):
        self._path = path
        self._topics = set(topics)
        self._topic_re = re.compile(r'^\s*(?:#\s*)?topic:\s*"?([^"\n]+)"?\s*$')

    def _open_text(self) -> TextIO:
        p = self._path
        if p.endswith(".gz"):
            return gzip.open(p, "rt", encoding="utf-8", errors="ignore")
        return open(p, "r", encoding="utf-8", errors="ignore")

    def _parse_header_stamps(self, fp, targets: set[str]):
        # Stream parse: yield (topic, ts) using ONLY header.stamp (secs+nsecs) once per episodic.
        curr = None
        in_header = in_stamp = False
        have_secs = have_nsecs = False
        secs = nsecs = 0

        for raw in fp:
            line = raw.rstrip("\n")

            m = self._topic_re.match(line)
            if m:
                topic = m.group(1).strip()
                curr = topic if topic in targets else None
                in_header = in_stamp = False
                have_secs = have_nsecs = False
                continue

            if curr is None:
                continue

            ls = line.strip()

            if ls == "header:":
                in_header = True
                in_stamp = False
                have_secs = have_nsecs = False
                secs = nsecs = 0
                continue

            if in_header:
                if ls == "stamp:":
                    in_stamp = True
                    have_secs = have_nsecs = False
                    secs = nsecs = 0
                    continue

                if in_stamp:
                    if ls.startswith("secs:"):
                        try:
                            secs = int(ls.split(":", 1)[1])
                            have_secs = True
                        except ValueError:
                            pass
                    elif ls.startswith("nsecs:"):
                        try:
                            nsecs = int(ls.split(":", 1)[1])
                            have_nsecs = True
                        except ValueError:
                            pass

                    if have_secs and have_nsecs:
                        ts = float(secs) + float(nsecs) * 1e-9
                        yield curr, ts
                        in_stamp = False  # emit once per episodic

    @staticmethod
    def _percentile_sorted(arr: List[float], p: float) -> float:
        # p in [0,1]; arr must be sorted ascending.
        if not arr:
            return math.nan
        k = (len(arr) - 1) * p
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return arr[int(k)]
        return arr[f] + (arr[c] - arr[f]) * (k - f)

    def compute(self):
        stats = {t: {"count": 0, "bad_dt": 0, "t_min": None, "t_max": None, "prev": None, "freqs": []}
                 for t in self._topics}

        with self._open_text() as fp:
            for topic, ts in self._parse_header_stamps(fp, self._topics):
                s = stats[topic]
                s["count"] += 1
                s["t_min"] = ts if s["t_min"] is None or ts < s["t_min"] else s["t_min"]
                s["t_max"] = ts if s["t_max"] is None or ts > s["t_max"] else s["t_max"]
                if s["prev"] is not None:
                    dt = ts - s["prev"]
                    if dt > 0.0:
                        s["freqs"].append(1.0 / dt)
                    else:
                        s["bad_dt"] += 1
                s["prev"] = ts

        # Prepare summary rows
        rows = []
        for t in sorted(stats.keys()):
            s = stats[t]
            freqs = sorted(s["freqs"])
            f_med = median(freqs) if freqs else float("nan")
            f_lo = self._percentile_sorted(freqs, 0.005) if freqs else float("nan")  # 0.5%
            f_hi = self._percentile_sorted(freqs, 0.995) if freqs else float("nan")  # 99.5%
            rows.append({
                "topic": t,
                "count": s["count"],
                "t_min": (s["t_min"] if s["t_min"] is not None else float("nan")),
                "t_max": (s["t_max"] if s["t_max"] is not None else float("nan")),
                "f_med": f_med,
                "ci99_lo": f_lo,
                "ci99_hi": f_hi,
                "bad_dt": s["bad_dt"],
            })
        return rows

    def print_summary(self):
        rows = self.compute()
        header = f"{'topic':30s} {'count':>9s} {'t_min':>12s} {'t_max':>12s} {'f_med(Hz)':>12s} {'CI99_low':>12s} {'CI99_high':>12s} {'bad_dt':>7s}"
        print(header)
        print("-" * len(header))
        for r in rows:
            print(f"{r['topic']:30s} "
                  f"{r['count']:9d} "
                  f"{r['t_min']:12.3f} {r['t_max']:12.3f} "
                  f"{r['f_med']:12.2f} {r['ci99_lo']:12.2f} {r['ci99_hi']:12.2f} "
                  f"{r['bad_dt']:7d}")


if __name__ == "__main__":
    path = "/home/donkarlo/Dropbox/phd/data/experiements/oldest/robots/uav1/mind/memory/long_term/explicit/episodic/normal/all_modalities.schema.yaml"
    topics = [
        "/uav1/odometry/odom_gps",
        "/uav1/rplidar/scan",
    ]
    mf = MessageFrequency99CI(path, topics)
    mf.print_summary()
