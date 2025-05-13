"""
setup.py
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

from setuptools import setup, find_packages  # type: ignore[import]

setup(
    name="phantom_cross",  # パッケージ名（pip listで表示される）
    version="1.0.1",  # バージョン.
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
            "phantom_cross = phantom_cross.__main__:main",
        ]
    },
)
