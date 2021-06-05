from setuptools import setup, find_packages
import os

readme_path = "README.md"
long_description = None
if os.path.isfile(readme_path):
    with open(readme_path, "r") as f:
        long_description = f.read()

requirements_pth = "requirements.txt"
install_requires = None
if os.path.isfile(requirements_pth):
    with open(requirements_pth) as f:
        install_requires = [r.strip() for r in f.readlines()]

name = 'pbar_pool'
setup(
    name=name,
    packages=find_packages(),
    version='0.0.1',
    license='MIT',
    description="A straightforward, dependency free way to update multiple progress bars with python's multiprocessing library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f'https://github.com/sdtblck/{name}',
    author='Sid Black',
    author_email='sdtblck@gmail.com',
    install_requires=install_requires,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
)
