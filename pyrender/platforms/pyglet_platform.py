import os
from pyrender.constants import (TARGET_OPEN_GL_MAJOR, TARGET_OPEN_GL_MINOR,
                                MIN_OPEN_GL_MAJOR, MIN_OPEN_GL_MINOR)
from pyrender.opengl_utils import create_opengl_configs, warn_fallback_version
from .base import Platform

import OpenGL


__all__ = ['PygletPlatform']


class PygletPlatform(Platform):
    """Renders on-screen using a 1x1 hidden Pyglet window for getting
    an OpenGL context.
    """

    def __init__(self, viewport_width, viewport_height):
        super(PygletPlatform, self).__init__(viewport_width, viewport_height)
        self._window = None

    def init_context(self):
        import pyglet
        pyglet.options['shadow_window'] = False

        try:
            pyglet.lib.x11.xlib.XInitThreads()
        except Exception:
            pass

        self._window = None
        
        # Get OpenGL configurations to try
        confs = create_opengl_configs()
        
        errors = []
        for desc, major, minor, mode, conf in confs:
            try:
                # For problematic systems, try setting software rendering
                if desc in ["LEGACY", "MINIMAL"] and not os.environ.get('LIBGL_ALWAYS_SOFTWARE'):
                    os.environ['LIBGL_ALWAYS_SOFTWARE'] = '1'
                
                self._window = pyglet.window.Window(config=conf, visible=False,
                                                    resizable=False,
                                                    width=1, height=1)
                # Success - warn if using fallback version
                warn_fallback_version(major, minor, TARGET_OPEN_GL_MAJOR, TARGET_OPEN_GL_MINOR)
                break
            except Exception as e:
                # Catch all exceptions during context creation
                error_msg = f"OpenGL {major}.{minor} {mode}: {type(e).__name__}: {e}"
                errors.append(error_msg)
                continue

        if not self._window:
            error_summary = "\n".join([f"  - {err}" for err in errors])
            
            # Detect WSL for specific troubleshooting
            is_wsl = False
            try:
                with open('/proc/version', 'r') as f:
                    if 'microsoft' in f.read().lower():
                        is_wsl = True
            except:
                pass
            
            # Suggest troubleshooting steps
            if is_wsl:
                troubleshooting = (
                    "\nWSL2 Troubleshooting suggestions:\n"
                    "1. Install X11 server on Windows (VcXsrv, Xming)\n"
                    "2. export DISPLAY=:0 (or your X server display)\n"
                    "3. For software rendering: export LIBGL_ALWAYS_SOFTWARE=1\n"
                    "4. Install OpenGL libraries: sudo apt install mesa-utils libgl1-mesa-glx\n"
                    "5. For debugging: export PYRENDER_DEBUG_OPENGL=1\n"
                    "6. Test with: glxinfo | grep 'OpenGL version'\n"
                    "7. Alternative: Use Docker with X11 forwarding"
                )
            else:
                troubleshooting = (
                    "\nTroubleshooting suggestions:\n"
                    "1. For SSH/headless: export DISPLAY=:0 or use VirtualGL\n"
                    "2. For software rendering: export LIBGL_ALWAYS_SOFTWARE=1\n"
                    "3. For Mesa override: export MESA_GL_VERSION_OVERRIDE=3.3\n"
                    "4. For debugging: export PYRENDER_DEBUG_OPENGL=1\n"
                    "5. Check: glxinfo | grep 'OpenGL version'"
                )
            
            raise ValueError(
                f'Failed to initialize Pyglet window with any OpenGL context.\n'
                f'Attempted configurations:\n{error_summary}\n'
                f'{troubleshooting}'
            )

    def make_current(self):
        if self._window:
            self._window.switch_to()

    def make_uncurrent(self):
        try:
            import pyglet
            pyglet.gl.xlib.glx.glXMakeContextCurrent(self._window.context.x_display, 0, 0, None)
        except Exception:
            pass

    def delete_context(self):
        if self._window is not None:
            self.make_current()
            cid = OpenGL.contextdata.getContext()
            try:
                self._window.context.destroy()
                self._window.close()
            except Exception:
                pass
            self._window = None
            OpenGL.contextdata.cleanupContext(cid)
            del cid

    def supports_framebuffers(self):
        return True
