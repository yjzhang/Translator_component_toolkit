from dataclasses import dataclass

from .translator_node import TranslatorNode, TranslatorEdge

@dataclass
class PathfinderGraph:
    """
    Output for TCT_pathfinder.pathfinder and ARAGORN_pathfinder.pathfinder
    """
    nodes: list[TranslatorNode]
    edges: list[TranslatorEdge]


