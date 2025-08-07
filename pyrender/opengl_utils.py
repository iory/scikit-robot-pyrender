"""OpenGL utilities for version detection and compatibility checking."""

import warnings
from .constants import TARGET_OPEN_GL_MAJOR, TARGET_OPEN_GL_MINOR, MIN_OPEN_GL_MAJOR, MIN_OPEN_GL_MINOR


def get_available_opengl_versions():
    """Get list of available OpenGL versions to try, in order of preference.
    
    Returns
    -------
    list of tuple
        List of (major, minor) version tuples in order of preference.
        Includes target version, minimum version, and additional fallback versions.
    """
    versions = []
    
    # Add target version first
    target = (TARGET_OPEN_GL_MAJOR, TARGET_OPEN_GL_MINOR)
    minimum = (MIN_OPEN_GL_MAJOR, MIN_OPEN_GL_MINOR)
    
    if target != minimum:
        versions.append(target)
    
    # Add intermediate versions between target and minimum if significant gap
    if target[0] > minimum[0] or (target[0] == minimum[0] and target[1] > minimum[1]):
        # Add some common intermediate versions
        intermediate_versions = [
            (4, 0), (3, 3), (3, 2), (3, 1), (3, 0)
        ]
        
        for ver in intermediate_versions:
            if (ver > minimum and ver < target and ver not in versions):
                versions.append(ver)
    
    # Add minimum version
    if minimum not in versions:
        versions.append(minimum)
    
    # Add even lower versions as last resort for problematic systems
    fallback_versions = [(2, 1), (2, 0), (1, 5), (1, 4), (1, 3), (1, 2), (1, 1)]
    for ver in fallback_versions:
        if ver not in versions:
            versions.append(ver)
    
    return versions


def create_opengl_configs():
    """Create OpenGL configurations to try, in order of preference.
    
    Returns
    -------
    list of tuple
        List of (description, major, minor, mode_name, pyglet.gl.Config) tuples
    """
    import pyglet.gl
    
    configs = []
    versions = get_available_opengl_versions()
    
    for major, minor in versions:
        version_desc = "TARGET" if (major, minor) == (TARGET_OPEN_GL_MAJOR, TARGET_OPEN_GL_MINOR) else "FALLBACK"
        if (major, minor) == (MIN_OPEN_GL_MAJOR, MIN_OPEN_GL_MINOR):
            version_desc = "MINIMUM"
        elif (major, minor) < (MIN_OPEN_GL_MAJOR, MIN_OPEN_GL_MINOR):
            version_desc = "LEGACY"
        
        # For OpenGL 3.0+, try with explicit version
        if major >= 3:
            # Try with multisampling first
            configs.append((
                version_desc, major, minor, "multisampling",
                pyglet.gl.Config(
                    sample_buffers=1, samples=4,
                    depth_size=24,
                    double_buffer=True,
                    major_version=major,
                    minor_version=minor
                )
            ))
            
            # Then try without multisampling
            configs.append((
                version_desc, major, minor, "basic",
                pyglet.gl.Config(
                    depth_size=24,
                    double_buffer=True,
                    major_version=major,
                    minor_version=minor
                )
            ))
        else:
            # For older OpenGL versions, don't specify version explicitly
            # Let the system choose the best available
            configs.append((
                version_desc, major, minor, "auto",
                pyglet.gl.Config(
                    depth_size=24,
                    double_buffer=True
                )
            ))
    
    # Add a final fallback with absolutely minimal requirements
    configs.append((
        "MINIMAL", 0, 0, "minimal",
        pyglet.gl.Config(
            double_buffer=False
        )
    ))
    
    return configs


def warn_fallback_version(used_major, used_minor, target_major, target_minor):
    """Emit a warning when falling back to a lower OpenGL version.
    
    Parameters
    ----------
    used_major, used_minor : int
        The OpenGL version that was successfully initialized
    target_major, target_minor : int
        The target OpenGL version that failed
    """
    if (used_major, used_minor) < (target_major, target_minor):
        warnings.warn(
            f"OpenGL fallback: Using OpenGL {used_major}.{used_minor} "
            f"(Target {target_major}.{target_minor} not available). "
            f"Some features may be limited.",
            RuntimeWarning
        )