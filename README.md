# simple-3d

(en) This is the English README.  
(ja) 日本語版は[こちら](https://github.com/MasahideMori-SimpleAppli/simple_3d_py/blob/main/README_JA.md)です。

## Overview

This package is a Python port of the [simple_3d](https://pub.dev/packages/simple_3d) Dart/Flutter package.
It is a working Python implementation of Simple 3D Format.

Simple 3D Format is a file format that makes it easy for non-experts to handle 3D objects.
Files output in this format have the extension `.sp3d`, and the internal classes are converted to JSON.
All data about one object is contained in one file.

This specification aims to minimize complexity, make it easier to read in a text editor, and make it versatile.
Made for science, it can be difficult to use in other genres.
For the development of science, the goal is to be able to use it without being affected by interests and conflicts.

The JSON serialization is fully compatible with the Dart version, so `.sp3d` files can be exchanged between Python and Dart/Flutter environments.

## Installation

```bash
pip install simple-3d
```

## Usage

### Quick Start

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

### Object Operations

```python
# Move
sp3d_obj.move(Sp3dV3D(1, 0, 0))

# Rotate
sp3d_obj.rotate(Sp3dV3D(0, 1, 0), 45 * math.pi / 180)

# Vertex manipulation
# You can do many other things with the Sp3dV3D features.
sp3d_obj.vertices[0] += Sp3dV3D(1, 0, 0)
```

### Convert to Dictionary (for JSON serialization)

```python
import json

sp3d_obj_dict = sp3d_obj.to_dict()
json_str = json.dumps(sp3d_obj_dict)
```

### Restore from Dictionary

```python
restored_dict = json.loads(json_str)
restored = Sp3dObj.from_dict(restored_dict)
```

## Color

Unlike the Dart version which uses Flutter's `Color` class, this package provides `Sp3dColor`.
Colors are stored as ARGB float values in the range `[0.0, 1.0]`.

```python
from simple_3d import Sp3dColor

# From integer ARGB values (0-255)
color = Sp3dColor.from_argb_int(255, 0, 255, 0)   # opaque green

# From float ARGB values (0.0-1.0)
color = Sp3dColor(1.0, 0.0, 1.0, 0.0)

# Convert back to integer ARGB
a, r, g, b = color.to_argb_int()
```

## Sp3dV3D — 3D Vector

```python
from simple_3d import Sp3dV3D
import math

v1 = Sp3dV3D(1.0, 0.0, 0.0)
v2 = Sp3dV3D(0.0, 1.0, 0.0)

# Arithmetic
v3 = v1 + v2
v4 = v1 * 2.0
v5 = v3 / 2.0

# Length and normalization
length = v1.len()
unit = v1.nor()

# Dot and cross products
d = Sp3dV3D.dot(v1, v2)
c = Sp3dV3D.cross(v1, v2)

# Rotation (around a normalized axis)
z_axis = Sp3dV3D(0, 0, 1)
rotated = v1.rotated(z_axis, math.pi / 2)   # returns new vector
v1.rotate(z_axis, math.pi / 2)              # mutates in place

# Signed angle
angle = Sp3dV3D.signed_angle(v1, v2, z_axis)   # radians, with sign
```

## Format Name

Simple 3D Format

## File Extension

`.sp3d`

## MIME Type (Temporary)

`model/x.sp3d`

## Suitable

Science (e.g., physics calculations), simple games, etc.

## Not Suitable

Advanced graphics.

## Structure (Decoded Object)

- `Sp3dObj`
    - `vertices`: list of `Sp3dV3D`
    - `fragments`: list of `Sp3dFragment`
        - `faces`: list of `Sp3dFace`
            - `vertex_index_list`: list of int — counterclockwise from upper-left
            - `material_index`: int or None
        - `is_particle`: bool
        - `r`: float — radius for particle type
        - `physics`: `Sp3dPhysics` or None
        - `is_touchable`: bool — if False, excluded from touch calculations
        - `name`: str or None
        - `option`: dict or None — app-specific optional attributes (must be JSON-serializable)
    - `materials`: list of `Sp3dMaterial`
        - `bg`: `Sp3dColor` — ARGB background color
        - `is_fill`: bool — if False, stroke line only
        - `stroke_width`: float
        - `stroke_color`: `Sp3dColor` — ARGB stroke color
        - `image_index`: int or None — fills the face with the specified image when not None
        - `texture_coordinates`: list of `(float, float)` or None — 3 or 6 points (square = two triangles)
        - `name`: str or None
        - `option`: dict or None
    - `images`: list of `bytes` — PNG data
    - `id`: str or None
    - `name`: str or None
    - `author`: str or None
    - `physics`: `Sp3dPhysics` or None
        - `is_locked`: bool — if True, treated as a fixed object
        - `mass`: float or None — (kg)
        - `speed`: float or None — (m/s)
        - `direction`: `Sp3dV3D` or None — unit direction vector
        - `velocity`: `Sp3dV3D` or None — used for movement
        - `rotate_axis`: `Sp3dV3D` or None
        - `angular_velocity`: float or None — (rad/s)
        - `angle`: float or None — (rad)
        - `name`: str or None
        - `others`: dict or None
    - `option`: dict or None
    - `layer_num`: int — drawing priority in the depth direction
    - `draw_mode`: `EnumSp3dDrawMode` — drawing mode for renderers

## Parameter Note

If you use `Sp3dObj` to calculate a large number of atoms, consider using the `is_particle` flag and `r` (radius).
Each atom has one vertex when calculated or saved, and you can draw a sphere only when rendering.

## JSON Compatibility with Dart Version

`to_dict()` / `from_dict()` produce output compatible with Dart version 21 and later (camelCase keys).
For compatibility with older versions (≤ v20, snake_case keys), use `to_dict_v14()`.
`from_dict()` automatically detects the version and calls the appropriate loader.

## License

This software is released under the MIT License. See the LICENSE file for details.

## Trademarks

- “Dart” and “Flutter” are trademarks of Google LLC.  
  *This package is not developed or endorsed by Google LLC.*

- “Python” is a trademark of the Python Software Foundation.  
  *This package is not affiliated with the Python Software Foundation.*

- GitHub and the GitHub logo are trademarks of GitHub, Inc.  
  *This package is not affiliated with GitHub, Inc.*
