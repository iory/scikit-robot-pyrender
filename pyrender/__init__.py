import sys

from .camera import (Camera, PerspectiveCamera, OrthographicCamera,
                     IntrinsicsCamera)
from .light import Light, PointLight, DirectionalLight, SpotLight
from .sampler import Sampler
from .texture import Texture
from .material import Material, MetallicRoughnessMaterial
from .primitive import Primitive
from .mesh import Mesh
from .node import Node
from .scene import Scene
from .renderer import Renderer
from .viewer import Viewer
from .offscreen import OffscreenRenderer
from .constants import RenderFlags, TextAlign, GLTF


def determine_version(module_name):
    """Determine version of the package."""
    if (sys.version_info[0] == 3 and sys.version_info[1] >= 8) \
        or sys.version_info[0] > 3:
        import importlib.metadata
        return importlib.metadata.version(module_name)
    else:
        import pkg_resources
        return pkg_resources.get_distribution(module_name).version


try:
    __version__ = determine_version('pyrender')
except Exception:
    __version__ = '0.1.45'  # fallback version

__all__ = [
    'Camera', 'PerspectiveCamera', 'OrthographicCamera', 'IntrinsicsCamera',
    'Light', 'PointLight', 'DirectionalLight', 'SpotLight',
    'Sampler', 'Texture', 'Material', 'MetallicRoughnessMaterial',
    'Primitive', 'Mesh', 'Node', 'Scene', 'Renderer', 'Viewer',
    'OffscreenRenderer', '__version__', 'RenderFlags', 'TextAlign',
    'GLTF'
]
