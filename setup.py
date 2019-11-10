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

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel, get_platform

    class bdist_wheel(_bdist_wheel):

        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            # Mark us as not a pure python package (we have platform specific ctpse lib)
            # if self.plat_name != "any":
            #     self.root_is_pure = False
            #     plat_name = (self.plat_name or get_platform()).replace('-', '_').replace('.', '_')
            #     if plat_name == "linux_x86_64" or plat_name == "manylinux1_x86_64":
            #         self.distribution.package_data[""] = ["ctpse/LinuxDataCollect64.so"]
            #     elif plat_name == "win32":
            #         self.distribution.package_data[""] = ["ctpse/WinDataCollect32.dll"]
            #     elif plat_name == "win_amd64":
            #         self.distribution.package_data[""] = ["ctpse/WinDataCollect64.dll"]
            self.distribution.package_data[""] = ["ctpse/WinDataCollect64.dll","ctpse/LinuxDataCollect64.so","ctpse/WinDataCollect32.dll"]
        def get_tag(self):
            # this set's us up to build generic wheels.
            python, abi, plat = _bdist_wheel.get_tag(self)
            # We don't contain any python source
            
            plat =  "any"
            python, abi = 'py3', 'none'
            return python, abi, plat
except ImportError:
    bdist_wheel = None

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
    version='1.9.2',
    description=DESCRIPTION,
    long_description='publisher and subscriber',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    install_requires=['websocket-client', 'quantaxis>=1.5.3'],
    entry_points={
        'console_scripts': [
            'QAOTG_test=QA_OTGBroker.app:app'
        ]
    },
    cmdclass={'bdist_wheel': bdist_wheel},
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True
)
