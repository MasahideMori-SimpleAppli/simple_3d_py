from enum import Enum


class EnumSp3dDrawMode(Enum):
    """Drawing mode for Sp3dObj when rendered by a renderer.

    Attributes
    ----------
    normal : str
        Standard 3D drawing mode.
    rect : str
        Rectangle-based drawing mode. Use when speed is required but 3D
        structure is not necessary, such as scatter plots.
    """

    normal = "normal"
    rect = "rect"
