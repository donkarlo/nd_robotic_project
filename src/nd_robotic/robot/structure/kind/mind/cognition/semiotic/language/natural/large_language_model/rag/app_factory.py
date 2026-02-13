# -----------------------------
# AppFactory (OOP)
# -----------------------------
from nd_robotic.robot.robot import \
    AnswerPolicy
from nd_robotic.robot.robot import \
    RagEngine
from nd_robotic.robot.robot import \
    RuntimeConfig
from nd_robotic.robot.robot import \
    TerminalApp


class AppFactory:
    def __init__(self, cfg: RuntimeConfig, policy: AnswerPolicy):
        self._cfg = cfg
        self._policy = policy

    def build(self) -> TerminalApp:
        rag = RagEngine(cfg=self._cfg, policy=self._policy)
        return TerminalApp(rag=rag)