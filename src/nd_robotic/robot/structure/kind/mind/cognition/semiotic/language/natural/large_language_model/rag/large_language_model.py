
from pathlib import Path
import os

from nd_robotic.robot.robot import \
    AnswerPolicy
from nd_robotic.robot.robot import \
    AppFactory
from nd_robotic.robot.robot import \
    RuntimeConfig

os.environ.setdefault("LLAMA_LOG_LEVEL", "ERROR")
os.environ.setdefault("GGML_LOG_LEVEL", "ERROR")


def main() -> None:
    cfg = RuntimeConfig(
        root=Path("//data/"),
        instructions_yaml=Path("instructions.yaml"),
        embed_model_gguf=Path(
            "/llama/nomic-embed-text-v1.5.Q2_K.gguf"),
        chat_model_gguf=Path(
            "/llama/qwen2.5-3b-instruct-q4_k_m.gguf"),
        n_threads=min(4, os.cpu_count() or 4),
    )

    policy = AnswerPolicy(
        vector_min_score=0.22,
        keyword_min_score=0.6,
        allow_general_fallback=True,
        show_sources=True,
        max_sources=6,
    )

    app = AppFactory(cfg=cfg, policy=policy).build()
    app.run()


if __name__ == "__main__":
    main()
