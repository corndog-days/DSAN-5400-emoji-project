import setuptools
with open('README.md', 'r') as f:
    long_description = f.read()
setuptools.setup(
    name='matcher',
    version='0.0.1',
    author='Isabelle Reilly, Lillian Ehrhart, Shivani Ramesh',
    author_email='icr16@georgetown.edu, le290@georgetown.edu, sr1651@georgetown.edu',
    description='An information retrieval tool to input emojis through a keyboard GUI and receive book recommendations from a provided dataset of books',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    extras_requres={"dev": ["pytest", "flake8", "autopep8"]},
)
