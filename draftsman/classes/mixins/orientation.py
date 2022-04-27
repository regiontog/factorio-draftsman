# orientation.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman import signatures


class OrientationMixin(object):
    """
    Used in trains and wagons to specify their direction.
    """

    def __init__(self, name, similar_entities, **kwargs):
        # type: (str, list[str], **dict) -> None
        super(OrientationMixin, self).__init__(name, similar_entities, **kwargs)

        self.orientation = 0.0
        if "orientation" in kwargs:
            self.orientation = kwargs["orientation"]
            self.unused_args.pop("orientation")
        self._add_export("orientation", lambda x: x is not None and x != 0)

    # =========================================================================

    @property
    def orientation(self):
        # type: () -> float
        """
        The angle that the current Entity is facing, expressed as a ``float``
        in the range ``[0.0, 1.0]``, where ``0.0`` is North.

        .. NOTE::

            This is distinct from ``direction``, which is used on grid-aligned
            entities and can only be a max of 8 possible rotations.

        :getter: Gets the orientation of the Entity.
        :setter: Sets the orientation of the Entity.
        :type: ``float``

        :exception TypeError: If set to anything other than a ``float`` or
            ``None``.
        """
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        # type: (float) -> None
        # TODO: what happens when orientation is out of range?
        if value is None or isinstance(value, float):
            self._orientation = value
        else:
            raise TypeError("'orientation' must be a float or None")
