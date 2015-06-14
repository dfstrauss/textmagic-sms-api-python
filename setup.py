from distutils.core import setup

setup(
    name="PyTextMagicSMS",
    version="0.2",

    description="TextMagic SMS API",
    long_description="A Python wrapper for the TextMagic HTTPS API to send SMS messages",

    author="Dawie Strauss",
    author_email="dfstrauss@gmail.com",
    url="https://github.com/dfstrauss/textmagic-sms-api-python",
    license="BSD",
    packages=['textmagic'],
    platforms=['any'],

    download_url="http://pypi.python.org/pypi/PyTextMagicSMS",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
