# burner_generator.py
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from draftsman.classes import Entity
from draftsman.classes.mixins import DirectionalMixin
from draftsman.warning import DraftsmanWarning

from draftsman.data.entities import burner_generators

import warnings


class BurnerGenerator(DirectionalMixin, Entity):
    """
    TODO: think about, because burner generators from mods like Space
    Exploration don't have orientation. Are they the same entity type?
    """

    def __init__(self, name=burner_generators[0], **kwargs):
        # type: (str, **dict) -> None
        super(BurnerGenerator, self).__init__(name, burner_generators, **kwargs)

        for unused_arg in self.unused_args:
            warnings.warn(
                "{} has no attribute '{}'".format(type(self), unused_arg),
                DraftsmanWarning,
                stacklevel=2,
            )
