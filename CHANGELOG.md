# Changelog

## [17.3.1] - 2026-04-30

### Fixed
- `Sp3dPhysics`: `from_dict` and `from_dict_v14` now safely convert `mass`, `speed`,
  `angular_velocity`, and `angle` to `float` to handle JSON-decoded integer values correctly.

## [17.3.0] - 2026-04-12

### Added
- `Sp3dPhysics`: added `force` (`Sp3dV3D | None`) and `torque` (`Sp3dV3D | None`) fields (version `"6"`).
  - Per-step scratch buffers: zero → accumulate forces/torques → integrate → zero each tick.
  - Included in `to_dict()` / `from_dict()` and `deep_copy()`.
  - Unit system is application-defined; must be consistent with `mass`, `velocity`, inertia tensor, and the simulation time step.

## [17.2.0] - 2026-04-01

### Added
- Initial Python port of `simple_3d` (Dart version 17.2.0).
- `Sp3dV3D`, `Sp3dObj`, `Sp3dFragment`, `Sp3dFace`, `Sp3dMaterial`, `Sp3dColor`, `Sp3dPhysics`, `EnumSp3dDrawMode`.
- Full JSON serialization (`to_dict` / `from_dict`) compatible with Dart version 21+.
- Backward-compatible serialization (`to_dict_v14` / `from_dict_v14`) for Dart versions ≤ 20.
