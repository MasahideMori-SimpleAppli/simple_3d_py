from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .sp3d_v3d import Sp3dV3D


class Sp3dPhysics:
    """Physics parameter container for ``Sp3dObj`` or ``Sp3dFragment``.

    Stores parameters used in physics simulations.
    Mirrors the Dart ``Sp3dPhysics`` class.

    Parameters
    ----------
    is_locked : bool, optional
        If ``True``, treat the object as a fixed (immovable) object.
        Defaults to ``False``.
    mass : float or None, optional
        The mass of the object in kg.  The unit should be adapted for
        atomic-scale calculations.
    speed : float or None, optional
        The speed of the object in m/s.  Retained primarily for convenience
        in calculations.
    direction : Sp3dV3D or None, optional
        The direction of travel as a unit vector.  Retained primarily for
        convenience in calculations.
    velocity : Sp3dV3D or None, optional
        The velocity vector of the object.  Used for moving objects.
    rotate_axis : Sp3dV3D or None, optional
        The rotation axis of the object.
    angular_velocity : float or None, optional
        The angular velocity of the object in rad/s.
    angle : float or None, optional
        The accumulated rotation angle of the object in radians.
    name : str or None, optional
        A name describing the physics action.
    force : Sp3dV3D or None, optional
        Accumulated force buffer for the current timestep (application-defined units).
        Zero → accumulate → integrate → zero each tick.
    torque : Sp3dV3D or None, optional
        Accumulated torque buffer for the current timestep (application-defined units).
        Same lifecycle as force.
    others : dict or None, optional
        Additional optional attributes.  Only JSON-serializable values
        are accepted.
    """

    CLASS_NAME = "Sp3dPhysics"
    VERSION = "6"

    def __init__(
        self,
        is_locked: bool = False,
        mass: float | None = None,
        speed: float | None = None,
        direction: Sp3dV3D | None = None,
        velocity: Sp3dV3D | None = None,
        rotate_axis: Sp3dV3D | None = None,
        angular_velocity: float | None = None,
        angle: float | None = None,
        name: str | None = None,
        force: Sp3dV3D | None = None,
        torque: Sp3dV3D | None = None,
        others: dict[str, Any] | None = None,
    ) -> None:
        self.is_locked = is_locked
        self.mass = mass
        self.speed = speed
        self.direction = direction
        self.velocity = velocity
        self.rotate_axis = rotate_axis
        self.angular_velocity = angular_velocity
        self.angle = angle
        self.name = name
        self.force = force
        self.torque = torque
        self.others = others

    def deep_copy(self) -> Sp3dPhysics:
        """Return a deep copy of this physics object.

        Returns
        -------
        Sp3dPhysics
            A new ``Sp3dPhysics`` with all fields copied.
        """
        return Sp3dPhysics(
            is_locked=self.is_locked,
            mass=self.mass,
            speed=self.speed,
            direction=self.direction.deep_copy() if self.direction is not None else None,
            velocity=self.velocity.deep_copy() if self.velocity is not None else None,
            rotate_axis=self.rotate_axis.deep_copy() if self.rotate_axis is not None else None,
            angular_velocity=self.angular_velocity,
            angle=self.angle,
            name=self.name,
            force=self.force.deep_copy() if self.force is not None else None,
            torque=self.torque.deep_copy() if self.torque is not None else None,
            others=dict(self.others) if self.others is not None else None,
        )

    # ------------------------------------------------------------------
    # Serialization (current format)
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Convert this physics object to a dictionary (current camelCase format).

        Returns
        -------
        dict
            A dictionary containing all physics parameters with camelCase keys.
        """
        return {
            "className": self.CLASS_NAME,
            "version": self.VERSION,
            "isLocked": self.is_locked,
            "mass": self.mass,
            "speed": self.speed,
            "direction": self.direction.to_dict() if self.direction is not None else None,
            "velocity": self.velocity.to_dict() if self.velocity is not None else None,
            "rotateAxis": self.rotate_axis.to_dict() if self.rotate_axis is not None else None,
            "angularVelocity": self.angular_velocity,
            "angle": self.angle,
            "name": self.name,
            "force": self.force.to_dict() if self.force is not None else None,
            "torque": self.torque.to_dict() if self.torque is not None else None,
            "others": self.others,
        }

    @classmethod
    def from_dict(cls, src: dict[str, Any]) -> Sp3dPhysics:
        """Restore a physics object from a dictionary produced by :meth:`to_dict`.

        Parameters
        ----------
        src : dict
            A dictionary made with :meth:`to_dict`.

        Returns
        -------
        Sp3dPhysics
            The restored physics object.
        """
        from .sp3d_v3d import Sp3dV3D

        return cls(
            is_locked=src["isLocked"],
            mass=src["mass"],
            speed=src["speed"],
            direction=Sp3dV3D.from_dict(src["direction"]) if src.get("direction") is not None else None,
            velocity=Sp3dV3D.from_dict(src["velocity"]) if src.get("velocity") is not None else None,
            rotate_axis=Sp3dV3D.from_dict(src["rotateAxis"]) if src.get("rotateAxis") is not None else None,
            angular_velocity=src["angularVelocity"],
            angle=src["angle"],
            name=src["name"],
            force=Sp3dV3D.from_dict(src["force"]) if src.get("force") is not None else None,
            torque=Sp3dV3D.from_dict(src["torque"]) if src.get("torque") is not None else None,
            others=src["others"],
        )

    def to_dict_v14(self) -> dict[str, Any]:
        """Convert this physics object to a dictionary (compatibility format for version <= 14).

        Returns
        -------
        dict
            A dictionary including ``"class_name"`` and ``"version"`` keys,
            using the older snake_case format.
        """
        return {
            "class_name": self.CLASS_NAME,
            "version": "4",
            "is_locked": self.is_locked,
            "mass": self.mass,
            "speed": self.speed,
            "direction": self.direction.to_dict_v14() if self.direction is not None else None,
            "velocity": self.velocity.to_dict_v14() if self.velocity is not None else None,
            "rotate_axis": self.rotate_axis.to_dict_v14() if self.rotate_axis is not None else None,
            "angular_velocity": self.angular_velocity,
            "angle": self.angle,
            "name": self.name,
            "others": self.others,
        }

    @classmethod
    def from_dict_v14(cls, src: dict[str, Any]) -> Sp3dPhysics:
        """Restore a physics object from an older-format dictionary (version <= 14).

        Parameters
        ----------
        src : dict
            A dictionary made with :meth:`to_dict_v14`.

        Returns
        -------
        Sp3dPhysics
            The restored physics object.
        """
        from .sp3d_v3d import Sp3dV3D

        return cls(
            is_locked=src["is_locked"],
            mass=src["mass"],
            speed=src["speed"],
            direction=Sp3dV3D.from_dict_v14(src["direction"]) if src.get("direction") is not None else None,
            velocity=Sp3dV3D.from_dict_v14(src["velocity"]) if src.get("velocity") is not None else None,
            rotate_axis=Sp3dV3D.from_dict_v14(src["rotate_axis"]) if src.get("rotate_axis") is not None else None,
            angular_velocity=src.get("angular_velocity"),
            angle=src.get("angle"),
            name=src.get("name"),
            others=src.get("others"),
        )
