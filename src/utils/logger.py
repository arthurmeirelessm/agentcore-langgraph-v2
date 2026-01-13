import logging
import sys
from typing import Optional


def setup_logger(
    name: str,
    level: int = logging.INFO
) -> logging.Logger:
    """
    Cria e configura um logger padronizado para o projeto.

    - Evita handlers duplicados
    - Loga para stdout (ideal para Lambda / AgentCore)
    - Inclui timestamp, nível e nome do módulo
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evita adicionar handlers múltiplas vezes
    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Evita log duplicado pelo root logger
    logger.propagate = False

    return logger
