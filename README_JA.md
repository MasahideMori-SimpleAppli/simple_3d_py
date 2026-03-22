# simple-3d

日本語版の解説です。
英語版は[こちら](README.md)です。

## 概要

このパッケージは、Dart/Flutter向け [simple_3d](https://pub.dev/packages/simple_3d) パッケージのPython移植版です。
Simple 3D FormatのPython実装です。

Simple 3D Formatは、3次元オブジェクトを専門家以外でも手軽に扱えるようにするためのファイル・フォーマットです。
このフォーマットで出力されたファイルは拡張子 `.sp3d` を持ち、内部クラスがJSONに変換されます。
１つのオブジェクトに関する全てのデータが１つのファイル内に含まれています。

この仕様は様々な用途に使用できるように複雑さを最小限に抑え、かつ簡単にテキストエディタで内容が確認できることを目的としています。
科学のために作られたので、他のジャンルで使いにくい可能性があります。
科学の発展のため、利権や争いなどに影響されずに利用できることを目指しています。

JSONシリアライズはDart版と完全に互換性があるため、`.sp3d` ファイルをPythonとDart/Flutter環境間で交換できます。

## インストール

```bash
pip install simple-3d
```

## 利用方法

### クイックスタート

```python
from simple_3d import Sp3dObj, Sp3dV3D, Sp3dFragment, Sp3dFace, Sp3dMaterial, Sp3dColor
import math

sp3d_obj = Sp3dObj(
    [Sp3dV3D(0, 0, 0)],
    [
        Sp3dFragment(
            [Sp3dFace([0], 0)],
            is_particle=True,
            r=1.0,
        )
    ],
    [
        Sp3dMaterial(
            Sp3dColor.from_argb_int(255, 0, 255, 0),
            True,
            1.0,
            Sp3dColor.from_argb_int(255, 0, 255, 0),
        )
    ],
    [],
)
```

### オブジェクトの操作例

```python
# 移動
sp3d_obj.move(Sp3dV3D(1, 0, 0))

# 回転
sp3d_obj.rotate(Sp3dV3D(0, 1, 0), 45 * math.pi / 180)

# 頂点の操作
# Sp3dV3Dの機能を使うと、他にも様々なことが出来ます。
sp3d_obj.vertices[0] += Sp3dV3D(1, 0, 0)
```

### 保存用の変換（JSONシリアライズ）

```python
import json

sp3d_obj_dict = sp3d_obj.to_dict()
json_str = json.dumps(sp3d_obj_dict)
```

### 復元

```python
restored_dict = json.loads(json_str)
restored = Sp3dObj.from_dict(restored_dict)
```

## カラー

Dart版ではFlutterの `Color` クラスを使用していますが、このパッケージでは `Sp3dColor` を提供しています。
色はARGB形式のfloat値（`[0.0, 1.0]` の範囲）で保持されます。

```python
from simple_3d import Sp3dColor

# 整数ARGB値（0〜255）から生成
color = Sp3dColor.from_argb_int(255, 0, 255, 0)   # 不透明な緑

# float ARGB値（0.0〜1.0）から生成
color = Sp3dColor(1.0, 0.0, 1.0, 0.0)

# 整数ARGBに変換
a, r, g, b = color.to_argb_int()
```

## Sp3dV3D — 3次元ベクトル

```python
from simple_3d import Sp3dV3D
import math

v1 = Sp3dV3D(1.0, 0.0, 0.0)
v2 = Sp3dV3D(0.0, 1.0, 0.0)

# 四則演算
v3 = v1 + v2
v4 = v1 * 2.0
v5 = v3 / 2.0

# 長さと正規化
length = v1.len()
unit = v1.nor()

# 内積・外積
d = Sp3dV3D.dot(v1, v2)
c = Sp3dV3D.cross(v1, v2)

# 回転（正規化された軸まわり）
z_axis = Sp3dV3D(0, 0, 1)
rotated = v1.rotated(z_axis, math.pi / 2)   # 新しいベクトルを返す
v1.rotate(z_axis, math.pi / 2)              # 自身を変更する

# 符号付き角度
angle = Sp3dV3D.signed_angle(v1, v2, z_axis)   # ラジアン、符号あり
```

## フォーマット名

Simple 3D Format

## 拡張子

`.sp3d`

## MIME Type（仮）

`model/x.sp3d`

## このオブジェクトが有用なもの

科学（例えば物理計算）や簡単なゲームなどに向いています。

## このオブジェクトが有用でないもの

高度なグラフィックを必要とするものには向いていません。

## 内部構造（デコードされた状態）

- `Sp3dObj`
    - `vertices`: `Sp3dV3D` のリスト
    - `fragments`: `Sp3dFragment` のリスト
        - `faces`: `Sp3dFace` のリスト
            - `vertex_index_list`: int のリスト — 左上から逆時計回りで定義
            - `material_index`: int または None
        - `is_particle`: bool
        - `r`: float — パーティクルタイプの半径
        - `physics`: `Sp3dPhysics` または None
        - `is_touchable`: bool — False の場合、タッチ計算の対象外になります
        - `name`: str または None
        - `option`: dict または None — アプリ毎に拡張可能なオプション属性（JSON化できる値のみ）
    - `materials`: `Sp3dMaterial` のリスト
        - `bg`: `Sp3dColor` — ARGB背景色
        - `is_fill`: bool — False の場合は輪郭線のみ表示
        - `stroke_width`: float
        - `stroke_color`: `Sp3dColor` — ARGBストローク色
        - `image_index`: int または None — null でない時、指定された画像でfaceを塗りつぶします
        - `texture_coordinates`: `(float, float)` のリスト または None — 3点または6点（四角の場合は三角形2つで指定）
        - `name`: str または None
        - `option`: dict または None
    - `images`: `bytes` のリスト — PNGデータ
    - `id`: str または None
    - `name`: str または None
    - `author`: str または None
    - `physics`: `Sp3dPhysics` または None
        - `is_locked`: bool — True の場合、固定オブジェクトとして扱われます
        - `mass`: float または None — 質量（kg）
        - `speed`: float または None — 速さ（m/s）
        - `direction`: `Sp3dV3D` または None — 進行方向の単位ベクトル
        - `velocity`: `Sp3dV3D` または None — moveする時に使います
        - `rotate_axis`: `Sp3dV3D` または None — 回転軸
        - `angular_velocity`: float または None — 角速度（rad/s）
        - `angle`: float または None — 角度（rad）
        - `name`: str または None — 動作の名前
        - `others`: dict または None
    - `option`: dict または None
    - `layer_num`: int — 奥行方向の描画優先度（レイヤー番号が小さい方から先に描画）
    - `draw_mode`: `EnumSp3dDrawMode` — レンダラーで描画される時のモード

## パラメータのメモ

多数の原子の計算に `Sp3dObj` を使用する場合は、`is_particle` フラグと `r`（半径）の使用を検討してください。
各原子は計算または保存時に1つの頂点を持ち、画面上に描画する場合にのみ球を描画することができます（つまり、描画の時には新しい `Sp3dObj` を作ります）。

## Dart版とのJSON互換性

`to_dict()` / `from_dict()` は、Dart版バージョン21以降と互換性のある出力（camelCaseキー）を生成します。
旧バージョン（v20以下、snake_caseキー）との互換性が必要な場合は `to_dict_v14()` を使用してください。
`from_dict()` はバージョンを自動判定し、適切な読み込み処理を呼び出します。

## ライセンス

このソフトウェアはMITライセンスの元配布されます。LICENSEファイルの内容をご覧ください。
