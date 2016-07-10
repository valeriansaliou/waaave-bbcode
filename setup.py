from distutils.core import setup

setup(
    name='waaave-bbcode',
    version='0.5.10',
    description='BBCode support in Django (Waaave version)',
    author='Valerian Saliou',
    author_email='valerian@valeriansaliou.name',
    url='https://github.com/valeriansaliou/waaave-bbcode',
    packages=[
        'bbcode',
        'bbcode.bbtags',
        'bbcode.templatetags',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
