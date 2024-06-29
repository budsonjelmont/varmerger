import setuptools

setuptools.setup(
    name='varmerger',
    version='1.0.0',
    url='https://github.com/budsonjelmont/varmerger',
    author='Judson Belmont',
    author_email='budsonjelmont@gmail.com',
    description='Variant manipulation utilities',
    long_description=open('varmerger/README.md').read(),
    packages=setuptools.find_packages(include=['varmerger', 'varmerger.*']),
    include_package_data=True,
    install_requires=['pandas','numpy','pyvcf3'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ]
)

