import sys

from .camera import Camera
from .camera import IntrinsicsCamera
from .camera import OrthographicCamera
from .camera import PerspectiveCamera
from .constants import GLTF
from .constants import RenderFlags
from .constants import TextAlign
from .light import DirectionalLight
from .light import Light
from .light import PointLight
from .light import SpotLight
from .material import Material
from .material import MetallicRoughnessMaterial
from .mesh import Mesh
from .node import Node
from .offscreen import OffscreenRenderer
from .primitive import Primitive
from .renderer import Renderer
from .sampler import Sampler
from .scene import Scene
from .texture import Texture
from .viewer import Viewer


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
