from setuptools import setup

from pie import __version__

with open('README.md', 'r') as reader:
    readme = reader.read()

setup(
    author='Jaedson Silva',
    author_email='imunknowuser@protonmail.com',
    name='pie-cli',
    description='Pie, a complete version control.',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/jaedsonpys/pie',
    license='GPL v3.0',
    version=__version__,
    packages=['pie'],
    python_requires='>=3.7',
    install_requires=['utokeniz'],
    keywords=['control', 'version', 'versioning', 'file']
)
