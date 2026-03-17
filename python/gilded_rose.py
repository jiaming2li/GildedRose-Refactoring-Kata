# # -*- coding: utf-8 -*-

# class Item:
#     def __init__(self, name, sell_in, quality):
#         self.name = name
#         self.sell_in = sell_in
#         self.quality = quality

#     def __repr__(self):
#         return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


# class GildedRose(object):

#     def __init__(self, items):
#         self.items = items

#     def update_quality(self):
#         for item in self.items:
#             if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert":
#                 if item.quality > 0:
#                     if item.name != "Sulfuras, Hand of Ragnaros":
#                         item.quality = item.quality - 1
#             else:
#                 if item.quality < 50:
#                     item.quality = item.quality + 1
#                     if item.name == "Backstage passes to a TAFKAL80ETC concert":
#                         if item.sell_in < 11:
#                             if item.quality < 50:
#                                 item.quality = item.quality + 1
#                         if item.sell_in < 6:
#                             if item.quality < 50:
#                                 item.quality = item.quality + 1
#             if item.name != "Sulfuras, Hand of Ragnaros":
#                 item.sell_in = item.sell_in - 1
#             if item.sell_in < 0:
#                 if item.name != "Aged Brie":
#                     if item.name != "Backstage passes to a TAFKAL80ETC concert":
#                         if item.quality > 0:
#                             if item.name != "Sulfuras, Hand of Ragnaros":
#                                 item.quality = item.quality - 1
#                     else:
#                         item.quality = item.quality - item.quality
#                 else:
#                     if item.quality < 50:
#                         item.quality = item.quality + 1


# -*- coding: utf-8 -*-

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


# ─────────────────────────────────────────────
#  Strategy Pattern: one class per item type
# ─────────────────────────────────────────────

class ItemUpdater:
    """Base strategy – handles a normal item."""

    MAX_QUALITY = 50
    MIN_QUALITY = 0

    def update(self, item):
        self._decrement_sell_in(item)
        self._update_quality(item)

    # ── helpers ──────────────────────────────
    def _decrement_sell_in(self, item):
        item.sell_in -= 1

    def _clamp(self, value):
        return max(self.MIN_QUALITY, min(self.MAX_QUALITY, value))

    def _update_quality(self, item):
        """Normal items degrade by 1; by 2 after sell-by date."""
        degradation = 2 if item.sell_in < 0 else 1
        item.quality = self._clamp(item.quality - degradation)


class AgedBrieUpdater(ItemUpdater):
    """Aged Brie increases in quality the older it gets."""

    def _update_quality(self, item):
        increase = 2 if item.sell_in < 0 else 1
        item.quality = self._clamp(item.quality + increase)


class SulfurasUpdater(ItemUpdater):
    """Sulfuras never changes – no sell_in decrement, no quality change."""

    def update(self, item):
        pass  # legendary item: immutable


class BackstagePassUpdater(ItemUpdater):
    """
    Backstage passes increase in quality as sell_in approaches:
      - More than 10 days: +1
      - 10 days or less:   +2
      -  5 days or less:   +3
      - After concert:      0 (quality drops to 0)
    """

    def _update_quality(self, item):
        if item.sell_in < 0:
            item.quality = 0
        elif item.sell_in < 5:
            item.quality = self._clamp(item.quality + 3)
        elif item.sell_in < 10:
            item.quality = self._clamp(item.quality + 2)
        else:
            item.quality = self._clamp(item.quality + 1)


class ConjuredUpdater(ItemUpdater):
    """Conjured items degrade in quality twice as fast as normal items."""

    def _update_quality(self, item):
        degradation = 4 if item.sell_in < 0 else 2
        item.quality = self._clamp(item.quality - degradation)


# ─────────────────────────────────────────────
#  Factory Pattern: maps item names → strategies
# ─────────────────────────────────────────────

class UpdaterFactory:
    _registry = {
        "Aged Brie":                                AgedBrieUpdater(),
        "Sulfuras, Hand of Ragnaros":               SulfurasUpdater(),
        "Backstage passes to a TAFKAL80ETC concert": BackstagePassUpdater(),
        "Conjured Mana Cake":                       ConjuredUpdater(),
    }

    @classmethod
    def get_updater(cls, item_name):
        return cls._registry.get(item_name, ItemUpdater())


# ─────────────────────────────────────────────
#  GildedRose: delegates to the right strategy
# ─────────────────────────────────────────────

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            updater = UpdaterFactory.get_updater(item.name)
            updater.update(item)