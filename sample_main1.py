"""
sample_main1.py
PhantomX Mk-2 の脚の可動範囲を計算する基本的なサンプルプログラム.
"""

# Copyright (c) 2023-2025 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php


import hexareach as hxr


if __name__ == "__main__":
    # まずは，GraphDisplayer クラスをインスタンス化してください．
    graph = hxr.GraphDisplayer()

    # display 関数を呼ぶことで描画されます．
    # マウスカーソルを動かすことで，脚先の位置を変化させることができます.
    # 左クリックすることで result/sample_main1.png に画像を保存できます.
    # 右クリックすることで, 左クリック時に生成される軌跡を削除することができます.
    # ホイールクリックによって，逆運動学解を反転させることができます.
    graph.display(
        hxr.PhantomxMk2Param(),
        # 保存先のファイル名を指定することができます.
        image_file_name="result/sample_main1.png")
