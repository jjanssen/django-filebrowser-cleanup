from distutils.core import setup

setup(
    name='django-filebrowser-cleanup',
    version='0.1dev',
    author='Janneke Janssen',
    author_email='j.janssen@lukkien.com',
    url='http://github.com/jjanssen/django-filebrowser-cleanup',
    description='Cleanup all unused files in the uploads folder which are no longer used by the Filebrowse field.',
    long_description=open('README.rst').read(),
    license='BSD',
    packages=[
        'filebrowser_cleanup',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
)