from distutils.core import setup


setup(
    name='acbutils',
    version='0.0.1',
    description='misc python utilties',
    long_description='misc python utilties',
    url='https://github.com/alexcb/acbutils',
    author='Alex Couture-Beil and contributors',
    license='BSD',
    packages=['acbutils'],
    scripts=[
        'scripts/python-pipe',
        'scripts/acbssh',
        'scripts/acbcat',
        'scripts/acbgallery',
        'scripts/githublink',
        'scripts/utc',
        'scripts/epoch',
        ],
)
