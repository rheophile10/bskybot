import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pw_bsky',
    version='1.0.0',
    author='Plains Wraith',
    author_bsky='@plainswraith.bsky.social',
    description=('python client for bsky'),
    long_description=long_description,
    #url='https://github.com/Antrikshy/Rackfocus',
    packages=['bsky'],
    entry_points = {
        'console_scripts': [
            'bsky=__init__'
        ]
    },
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)