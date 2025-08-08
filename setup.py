import sys

from setuptools import setup


version = '0.1.48'


def get_imageio_dep():
    if sys.version[0] == "2":
        return 'imageio<=2.6.1'
    return 'imageio'


requirements = [
    'freetype-py',                # For font loading
    get_imageio_dep(),            # For Image I/O
    'networkx',                   # For the scene graph
    'numpy',                      # Numpy
    'Pillow',                     # For Trimesh texture conversions
    'pyglet>=1.4.10',             # For the pyglet viewer
    'PyOpenGL~=3.1.0',            # For OpenGL
#    'PyOpenGL_accelerate~=3.1.0', # For OpenGL
    'scipy',                      # Because of trimesh missing dep
    'six',                        # For Python 2/3 interop
    'trimesh',                    # For meshes
]

dev_requirements = [
    'flake8',            # Code formatting checker
    'pre-commit',        # Pre-commit hooks
    'pytest',            # Code testing
    'pytest-cov',        # Coverage testing
    'tox',               # Automatic virtualenv testing
]

docs_requirements = []
with open('requirements_docs.txt') as f:
    for line in f:
        req = line.split('#')[0].strip()
        if req:  # Skip empty lines
            docs_requirements.append(req)


setup(
    name='scikit-robot-pyrender',
    version=version,
    description='Easy-to-use Python renderer for 3D visualization',
    long_description='A simple implementation of Physically-Based Rendering '
                       '(PBR) in Python. Compliant with the glTF 2.0 standard. '
                       'This is a fork of pyrender with improved OpenGL fallback capabilities.',
    author='Matthew Matl (original), Iori Yanokura (fork)',
    author_email='yanokura@jsk.imi.i.u-tokyo.ac.jp',
    license='MIT License',
    url='https://github.com/iory/scikit-robot-pyrender',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering'
    ],
    keywords='rendering graphics opengl 3d visualization pbr gltf',
    packages=['pyrender', 'pyrender.platforms'],
    setup_requires=requirements,
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements,
        'docs': docs_requirements,
    },
    include_package_data=True
)
