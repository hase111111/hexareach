
# Hexareach

Trossen Robotics社製の6脚ロボット，PhantomX のような，yaw - pitch - pitch の間接配置の脚の可動域を表示するプログラムです．

プログラムのパラメータを調整することで，様々な脚ロボットの表示に対応可能です．

<div align="center">
    <img src="/docs/img/leg_range.gif" width="70%" class="center">
</div>

## 概要

3関節（yaw - pitch - pitch）の脚を持つ脚ロボットの1脚の可動域を表示するプログラムです．
yaw軸周りの回転は無視し，2次元平面上で表示を行います．
つまり実質的に2リンクのマニピュレータの可動域のように表示します．
グラフや表はmatplotlibを用いて表示しています．

卒業研究のために作成したプログラムのため，Trossen Robotics社の6脚ロボットPhantomX Mk-2の脚のパラメータを用いていますが，パラメータを変更することで他の脚ロボットにも対応可能です．
しかし，間接配置を変更することはできません（yaw-pitch-pitchあるいはyaw-pitchにのみ対応）．

可動範囲のほかに，逆運動学計算による間接角度の算出や，脚先力の算出も行うことができます．
逆運動学は解析解を用いて計算しています．
これらに加えて，実機を動作させるためのサーボモータへの指令値の算出も行うことができます．
また，指令値がサーボモータの可動域を超える場合には，エラーを出力します．

<div align="center">
    <img src="/docs/img/table.jpg" width="95%">
    <p>
        <img src="/docs/img/coordinate_axis.png" width="40%">
    </p>
</div>

## 使い方

簡単に使用することができるように，パッケージ化しています．
まずは，このレポジトリからインストールしてください．

```bash
pip install git+[このレポジトリのURL]
pip3 install git+[このレポジトリのURL] # Python3の場合

# ex) pip install git+https://github.com/hase111111/hexareach.git

# 更新する場合は以下のコマンドを実行してください
# pip install --upgrade git+[このレポジトリのURL] -U
```

インストールが完了したら，以下のコマンドでプログラムを実行してください．
バージョン情報が表示されればインストールは成功です．

```bash
python -m hexareach  # Python2の場合
pyton3 -m hexareach  # Python3の場合
```

tkinterがない，というエラーが出た場合は，以下のコマンドでtkinterをインストールしてください．

```bash
sudo pip3 install pytk
sudo apt-get install python3-tk
```

### GraphDisplayerクラス

脚の図示はGraphDisplayerクラスを用いて行います．
下記のコードを実行すると，脚の可動域が表示されます．
詳細な使用方法については，[GraphDisplayerについて](/docs/about_graph_displayer.md)を参照してください．

```python
import hexareach as hxr

graph = hxr.GraphDisplayer()
graph.display(hxr.PhantomxMk2Param())
```

### HexapodParam

脚のパラメータは構造体HexapodParamを用いて設定します．
パラメータを変更することで，他の脚ロボットにも対応可能です．
詳細な使用方法については，[HexapodParamについて](/docs/about_hexapod_param.md)を参照してください．

```python
import hexareach as hxr

class OriginalRobotParam(hxr.HexapodParamProtocol):
    coxa_length: float = 0.0  # [mm]
    femur_length: float = 100.0  # [mm]
    tibia_length: float = 100.0  # [mm]
    theta1_max: float = math.radians(0.0)  # [rad]
    theta1_min: float = math.radians(0.0)  # [rad]
    theta2_max: float = math.radians(100.0)  # [rad]
    theta2_min: float = math.radians(-100)  # [rad]
    theta3_max: float = math.radians(100.0)  # [rad]
    theta3_min: float = math.radians(-100.0)  # [rad]
    torque_max: float = 0.0  # [N*mm] ストールトルク(停動トルク)
    approx_min_radius: float = 0  # [mm]
    approx_max_radius: float = 250.0  # [mm]

gd = hxr.GraphDisplayer(hp)
param = OriginalRobotParam()
gd.display(param)
```

### 操作方法

脚は青色の線で表示され，脚先はマウスに追従します．
脚先が可動範囲外に出た場合は，脚が赤色に変わります．
また，間接の可動範囲外に出た場合は，ジョイントが赤色に変わります．

左クリックすると脚先の位置が固定され，画像が保存されます．
右クリックすると，脚先の位置がリセットされます．
ホイールクリックすると，もうひとつの逆運動学解に切り替わります．

## ライセンス

MITライセンスです．

詳細は，[LICENSE](LICENSE.txt)を参照してください．
