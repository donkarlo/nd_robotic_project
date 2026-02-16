# bag_stats.py
# Python 3.13 — List topics and their frequency from either a ROS .bag (via CLI) or a YAML(.gz) dump.
# Keep all comments in English only.

import gzip
import re
import subprocess
from typing import Dict, List, Optional, TextIO, Tuple
from nd_robotic.platforms.ros.bag.topic_stat import TopicStat





class TopicFrequencyFinder:
    """
    Read either:
      - a YAML(.gz) dump created from rosbag (stream-parse header.stamp), or
      - a .bag file (query 'rosbag information --schema.yaml' and compute avg freq as count/duration).
    Reports, for each topic: episodic count and a frequency estimate.
    """

    _TOPIC_LINE = re.compile(r'^\s*(?:#\s*)?topic:\s*"?([^"\n]+)"?\s*$')
    _SECS_LINE = re.compile(r'^\s*secs:\s*(\d+)\s*$')
    _NSECS_LINE = re.compile(r'^\s*nsecs:\s*(\d+)\s*$')

    def __init__(self, path: str):
        self._path = path

    # ---------- Public API ----------

    def stats(self) -> Dict[str, TopicStat]:
        if self._path.endswith(".schema.yaml") or self._path.endswith(".yml") or self._path.endswith(
                ".schema.yaml.gz") or self._path.endswith(".yml.gz"):
            return self._stats_from_yaml_stream()
        elif self._path.endswith(".bag"):
            return self._stats_from_bag_cli()
        else:
            # Try YAML first; if fails, try bag CLI.
            try:
                return self._stats_from_yaml_stream()
            except Exception:
                return self._stats_from_bag_cli()

    # ---------- YAML(.gz) str_path ----------

    def _open_text(self) -> TextIO:
        p = self._path
        if p.endswith(".gz"):
            return gzip.open(p, "rt", encoding="utf-8", errors="ignore")
        return open(p, "r", encoding="utf-8", errors="ignore")

    def _stats_from_yaml_stream(self) -> Dict[str, TopicStat]:
        """
        Stream-parse YAML dump: detect 'topic:' lines and for each episodic emit a timestamp from header.stamp.
        Compute per-topic: count, span (t_max - t_min), avg frequency = (count-1)/span (using positive deltas implicitly).
        Note: If header.stamp is missing for some messages, those won'value contribute timestamps.
        """
        stats: Dict[str, Dict[str, object]] = {}
        curr_topic: Optional[str] = None
        in_header = False
        in_stamp = False
        have_secs = False
        have_nsecs = False
        secs = 0
        nsecs = 0

        with self._open_text() as fp:
            for raw in fp:
                line = raw.rstrip("\n")

                # topic line
                m = self._TOPIC_LINE.match(line)
                if m:
                    curr_topic = m.group(1).strip()
                    if curr_topic not in stats:
                        stats[curr_topic] = {
                            "count": 0,
                            "t_min": None,
                            "t_max": None,
                            "prev_ts": None,
                            "good_pairs": 0,  # count of positive dt
                        }
                    in_header = False
                    in_stamp = False
                    have_secs = have_nsecs = False
                    continue

                if curr_topic is None:
                    continue

                ls = line.strip()
                if ls == "header:":
                    in_header = True
                    in_stamp = False
                    have_secs = have_nsecs = False
                    secs = nsecs = 0
                    continue

                if in_header and ls == "stamp:":
                    in_stamp = True
                    have_secs = have_nsecs = False
                    secs = nsecs = 0
                    continue

                if in_header and in_stamp:
                    ms = self._SECS_LINE.match(ls)
                    if ms:
                        secs = int(ms.group(1))
                        have_secs = True
                        continue
                    mn = self._NSECS_LINE.match(ls)
                    if mn:
                        nsecs = int(mn.group(1))
                        have_nsecs = True
                        continue

                    # When both seen, emit exactly once per episodic
                    if have_secs and have_nsecs:
                        ts = float(secs) + float(nsecs) * 1e-9
                        s = stats[curr_topic]
                        # bump count for this episodic
                        s["count"] = int(s["count"]) + 1
                        # update t_min / t_max
                        tmin = s["t_min"]
                        tmax = s["t_max"]
                        s["t_min"] = ts if (tmin is None or ts < tmin) else tmin
                        s["t_max"] = ts if (tmax is None or ts > tmax) else tmax
                        # dt accounting (only to know how many valid action_potential_group exist)
                        prev = s["prev_ts"]
                        if prev is not None:
                            if ts - float(prev) > 0.0:
                                s["good_pairs"] = int(s["good_pairs"]) + 1
                        s["prev_ts"] = ts
                        # reset to avoid double emission
                        in_stamp = False
                        have_secs = have_nsecs = False

        # finalize
        out: Dict[str, TopicStat] = {}
        for t, s in stats.items():
            count = int(s["count"])
            t_min = s["t_min"]
            t_max = s["t_max"]
            span = None
            freq_avg = None
            if t_min is not None and t_max is not None:
                span = float(t_max) - float(t_min)
                # Prefer (good_pairs / span). If good_pairs==0 but count>1, we still can approximate with (count-1)/span.
                good_pairs = int(s["good_pairs"])
                if span > 0.0:
                    base_pairs = good_pairs if good_pairs > 0 else max(count - 1, 0)
                    freq_avg = base_pairs / span if base_pairs > 0 else 0.0
                else:
                    freq_avg = 0.0
            out[t] = TopicStat(topic=t, count=count, t_min=t_min, t_max=t_max, freq_avg_hz=freq_avg)
        return out

    # ---------- .bag str_path via 'rosbag information --schema.yaml' ----------

    def _stats_from_bag_cli(self) -> Dict[str, TopicStat]:
        """
        Use `rosbag information --schema.yaml <file.bag>` to get per-topic episodic counts and bag duration.
        Compute avg frequency per topic = count / duration (coarse but useful).
        Requires ROS Noetic 'rosbag' installed and on PATH.
        """
        try:
            res = subprocess.run(
                ["rosbag", "information", "--schema.yaml", self._path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except FileNotFoundError as e:
            raise RuntimeError("rosbag not found on PATH. Install ROS Noetic or provide a YAML dump.") from e
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"rosbag information failed: {e.stderr.strip()}") from e

        text = res.stdout
        duration = self._parse_duration_seconds(text)  # float or None
        topics = self._parse_topics_counts(text)  # List[(topic, count)]

        out: Dict[str, TopicStat] = {}
        for t, cnt in topics:
            freq = (cnt / duration) if (duration and duration > 0.0) else None
            out[t] = TopicStat(topic=t, count=cnt, t_min=None, t_max=None, freq_avg_hz=freq)
        return out

    @staticmethod
    def _parse_duration_seconds(info_yaml: str) -> Optional[float]:
        """
        Very small YAML-ish parser for the 'duration:' field line in rosbag information --schema.yaml.
        Accepts formats like 'duration: 123.456s' or 'duration: 123.456'.
        """
        for line in info_yaml.splitlines():
            line = line.strip()
            if line.startswith("duration:"):
                val = line.split(":", 1)[1].strip()
                if val.endswith("s"):
                    val = val[:-1]
                try:
                    return float(val)
                except ValueError:
                    return None
        return None

    @staticmethod
    def _parse_topics_counts(info_yaml: str) -> List[Tuple[str, int]]:
        """
        Parse the 'topics:' section of rosbag information --schema.yaml to get (topic_name, messages_count).
        """
        lines = info_yaml.splitlines()
        topics: List[Tuple[str, int]] = []
        in_topics = False
        current_topic = None
        for raw in lines:
            line = raw.rstrip("\n")
            stripped = line.strip()
            if stripped.startswith("topics:"):
                in_topics = True
                current_topic = None
                continue
            if not in_topics:
                continue
            # End of topics if a non-indented block starts (naive but good enough)
            if stripped and not line.startswith(" "):
                break
            # Look for '- topic:' lines
            if stripped.startswith("- topic:"):
                # e.g., "- topic: /uav1/odometry/odom_gps"
                current_topic = stripped.split(":", 1)[1].strip()
                continue
            if current_topic is not None and "messages:" in stripped:
                # e.g., "  messages: 434065"
                try:
                    cnt = int(stripped.split(":", 1)[1].strip())
                except ValueError:
                    cnt = 0
                topics.append((current_topic, cnt))
                current_topic = None
        return topics


# ---------- PublisherExample usage ----------
if __name__ == "__main__":
    # PublisherExample 1: YAML dump (recommended for Python 3.13)
    yaml_path = "/home/donkarlo/Dropbox/projs/research/data/self-aware-drones/ctumrs/two-drones/normal-inner_experiment/uav1-gps-lidar-uav2-gps-lidar.schema.yaml"
    bag1 = TopicFrequencyFinder(yaml_path)
    stats1 = bag1.stats()
    print(f"{'topic':30s} {'count':>10s} {'t_min':>14s} {'t_max':>14s} {'freq_avg(Hz)':>14s}")
    print("-" * 86)
    for t in sorted(stats1.keys()):
        s = stats1[t]
        f = "n/a" if s.freq_avg_hz is None else f"{s.freq_avg_hz:.2f}"
        tmin = "n/a" if s.t_min is None else f"{s.t_min:.3f}"
        tmax = "n/a" if s.t_max is None else f"{s.t_max:.3f}"
        print(f"{t:30s} {s.count:10d} {tmin:14s} {tmax:14s} {f:14s}")

    # PublisherExample 2: .bag (fallback via 'rosbag information --schema.yaml', gives avg freq as count/duration)
    # bag_path = "/str_path/to/file.bag"
    # bag2 = TopicFrequencyFinder(bag_path)
    # stats2 = bag2.stats()
    # ...
