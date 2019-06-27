import codecs
import io
import os
import re
import sys
import webbrowser
import platform

try:
    from setuptools import setup
except:
    from distutils.core import setup


NAME = "quantaxis_otgbroker"
"""
名字，一般放你包的名字即可
"""
PACKAGES = ["QA_OTGBroker"]
"""
包含的包，可以多个，这是一个列表
"""

DESCRIPTION = "QUANTAXIS OTGBroker:QUANTAXIS OPEN_TRADE_GATEWAY BROKER"
KEYWORDS = ["quantaxis", "quant", "finance", "Backtest", 'Framework']
AUTHOR_EMAIL = "yutiansut@qq.com"
AUTHOR = 'yutiansut'
URL = "https://gitee.com/yutiansut/QAOTGBROKERS"


LICENSE = "MIT"

setup(
    name=NAME,
    version='1.6',
    description=DESCRIPTION,
    long_description='publisher and subscriber',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    install_requires=['websocket-client', 'quantaxis>=1.1.10.dev2'],
    entry_points={
        'console_scripts': [
            'QAOTG_test=QA_OTGBroker.app:app'
        ]
    },
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True
)
