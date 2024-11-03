from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='zxp2gus',
    version='0.1',
    author='Raül Torralba',
    description='Convert ZX Paintbrush files to GuSprites ZXBasic code',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    entry_points='''
        [console_scripts]
        zxp2gus=zxp2gus.cli:main
    ''',
    url = 'https://github.com/rtorralba/zxp2gus',
    install_requires=[
        'numpy',
        'opencv-python'
    ],
)