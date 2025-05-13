"""
setup.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

from setuptools import setup, find_packages  # type: ignore[import]

setup(
    name="hexareach",  # パッケージ名（pip listで表示される）
    version="2.0.0",  # バージョン.
    description="Inverse kinematics of PhantomX and display of results.",  # 説明.
    license="MIT",  # ライセンス.
    author="taisei hasegawa",  # 作者名.
    author_email="hasehasehase61@gmail.com",  # 作者の連絡先.
    packages=find_packages(),  # 使うモジュール一覧を指定する.
    install_requires=[
        "numpy",
        "matplotlib",
        "scipy",
        "tqdm",
    ],  # 依存するパッケージのリスト.
    entry_points={
        "console_scripts": [
            "hexareach = hexareach.__main__:main",
        ]
    },
)
