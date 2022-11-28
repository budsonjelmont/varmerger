import setuptools

setuptools.setup(
    name='varmerger',
    version='1.0.0',
    url='https://git01.ops.medplus.com/Judson.X.Belmont/varmerger',
    author='Judson Belmont',
    author_email='judson.x.belmont@questdiagnostics.com',
    description='Variant manipulation utilities',
    long_description=open('varmerger/README.md').read(),
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['pandas','numpy','pyvcf'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ]
)

