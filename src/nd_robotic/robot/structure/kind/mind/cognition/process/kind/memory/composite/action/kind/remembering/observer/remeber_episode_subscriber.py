from typing import Protocol

from nd_robotic.mind.cognition.process.kind.memory.kind.long_term.explicit.episodic.experience.episode.episode import Episode


class RememberEpisodeSubscriber(Protocol):
    def do_with_remebered_episode(self, episode: Episode) -> None: ...