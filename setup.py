import ez_setup
ez_setup.use_setuptools()

#    From: http://peak.telecommunity.com/DevCenter/setuptools#egg-info-examples
#    Creating a dated "nightly build" snapshot egg:
#    python setup.py egg_info --tag-date --tag-build=DEV bdist_egg
#    Creating and uploading a release with no version tags, even if some default tags are specified in setup.cfg:
#    python setup.py egg_info -RDb "" sdist bdist_egg register upload
#    (Notice that egg_info must always appear on the command line before any commands that you want the version changes to apply to.)

from setuptools import setup, find_packages
setup(
    name = "py-textmagic",
    version = "0.0.1",

    description="TextMagic SMS HTTPS API",
    long_description="This is a Python wrapper for the TextMagic SMS sending web service",

    author="Dawie Strauss",
    author_email="dfstrauss@gmail.com",
    url="http://undefined.org/python/#simplejson",
    license="BSD",
    packages=find_packages(exclude=['ez_setup']),
    platforms=['any'],
    test_suite="textmagic.test.main.py",

    zip_safe=False,
)
