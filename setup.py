from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = ''.join(f.readlines())

setup(
    name='garage_system',
    version='0.1.0',
    description='System for managing garages',
    long_description=long_description,
    author='Ondřej Červenka',
    author_email='cerveon3@fit.cvut.cz',
    keywords='web',
    license='MIT',
    url='https://github.com/ggljzr/mi-dip-impl',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3.5',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP',
        'Environment :: Web Environment'
    ],
    entry_points={
        'console_scripts': ['garage_system = garage_system:run', ],
    },
    install_requires=['Flask>=0.12.2', 
                     'Jinja2>=2.8',
                     'Flask-SQLAlchemy>=2.3.2',
                     'Flask-WTF>=0.14.2',
                     'requests>=2.11.1',
                     'Werkzeug>=0.11.11',
                     'bcrypt>=3.1.3',
                     'APScheduler>=3.5.1'
                     ],
    setup_requires=[
        'pytest-runner',
        ],
    tests_require=[
        'pytest',
        'freezegun'
        ],
)