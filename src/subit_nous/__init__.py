"""SUBIT-NOUS: Knowledge graph from chaos using 4 transversal modes (MICRO, MACRO, MESO, META)."""

__version__ = "2.0.0"
__author__ = "SUBIT Ecosystem"
__license__ = "MIT"

# Core functions
from .core import (
    text_to_subit,
    subit_to_name,
    subit_to_coords,
    archetype_color,
    get_mode,
    # enums
    Who,
    Where,
    When,
    Why,
    # markers
    MARKERS,
)

# Graph building and visualization
from .graph import build_graph, visualize_4d

# Exports
from .exports import export_obsidian, export_report

# I/O (multimodal)
from .io import read_file, file_to_subit

__all__ = [
    # version
    "__version__",
    # core
    "text_to_subit",
    "subit_to_name",
    "subit_to_coords",
    "archetype_color",
    "get_mode",
    "Who",
    "Where",
    "When",
    "Why",
    "MARKERS",
    # graph
    "build_graph",
    "visualize_4d",
    # exports
    "export_obsidian",
    "export_report",
    # io
    "read_file",
    "file_to_subit",
]