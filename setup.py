from setuptools import setup

requirements = []
with open('requirements.txt') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            line = line.split('==')[0]
            requirements.append(line)

setup(
    name='elthranonline',
    packages=['elthranonline'],
    include_package_data=True,
    # install_requires=[
    #     'flask',
    # ],
    install_requires=requirements,
)


# additional requirements that should go in a requirements.txt file?
# SQLAlchemy          1.2.3
