# mining_drill.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman.classes import Entity
from draftsman.classes.mixins import (
    RequestItemsMixin,
    CircuitReadResourceMixin,
    CircuitConditionMixin,
    EnableDisableMixin,
    LogisticConditionMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    DirectionalMixin,
)
from draftsman.error import InvalidItemError
from draftsman.warning import DraftsmanWarning, ItemLimitationWarning

from draftsman.data.entities import mining_drills
from draftsman.data import modules
from draftsman.data import signals

import warnings


class MiningDrill(
    RequestItemsMixin,
    CircuitReadResourceMixin,
    CircuitConditionMixin,
    EnableDisableMixin,
    LogisticConditionMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    DirectionalMixin,
    Entity,
    object,
):
    def __init__(self, name=mining_drills[0], **kwargs):
        # type: (str, **dict) -> None
        super(MiningDrill, self).__init__(name, mining_drills, **kwargs)

        for unused_arg in self.unused_args:
            warnings.warn(
                "{} has no attribute '{}'".format(type(self), unused_arg),
                DraftsmanWarning,
                stacklevel=2,
            )

    def set_item_request(self, item, amount):
        # type: (str, int) -> None
        """
        Overwritten
        """
        # Make sure the item exists
        if item not in signals.item:  # TODO: maybe items.all instead?
            raise InvalidItemError(item)

        if item not in modules.raw:
            warnings.warn(
                "Item '{}' cannot be placed in MiningDrill".format(item),
                ItemLimitationWarning,
                stacklevel=2,
            )

        super(MiningDrill, self).set_item_request(item, amount)
