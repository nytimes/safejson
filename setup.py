# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from distutils.core import setup

# -----------------------------------------------------------------------------
# Setup code
# -----------------------------------------------------------------------------
setup(
	name='safeJSON',
    version='0.9b',
    py_modules=['safeJSON'],
    package_dir={'': 'src'},
    license = 'http://www.apache.org/licenses/LICENSE-2.0',
    author = 'Evan Sandhaus',
    author_email = 'evan@nytimes.com',
    description = "safeJSON simplifies the process of working with JSON object in python by suppressing both IndexError and KeyError exceptions on parsed objects."   
)
