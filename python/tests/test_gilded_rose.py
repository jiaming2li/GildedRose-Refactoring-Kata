# -*- coding: utf-8 -*-
# import unittest

# from gilded_rose import Item, GildedRose


# class GildedRoseTest(unittest.TestCase):
#     def test_foo(self):
#         items = [Item("foo", 0, 0)]
#         gilded_rose = GildedRose(items)
#         gilded_rose.update_quality()
#         self.assertEqual("fixme", items[0].name)

        
# if __name__ == '__main__':
#     unittest.main()
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):

    # ─────────────────────────────────────────
    #  Original placeholder (now fixed)
    # ─────────────────────────────────────────

    def test_normal_item_name_unchanged(self):
        """Item name should never be altered by update_quality."""
        items = [Item("foo", 0, 0)]
        GildedRose(items).update_quality()
        self.assertEqual("foo", items[0].name)

    # ─────────────────────────────────────────
    #  4 core failing tests (TDD starting point)
    # ─────────────────────────────────────────

    def test_normal_item_quality_degrades_by_one(self):
        """A normal item loses 1 quality per day before sell-by date."""
        items = [Item("Normal Item", 10, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(19, items[0].quality)

    def test_normal_item_quality_degrades_twice_after_sell_by(self):
        """After sell-by date, quality degrades twice as fast."""
        items = [Item("Normal Item", 0, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(18, items[0].quality)

    def test_backstage_pass_quality_drops_to_zero_after_concert(self):
        """Backstage pass quality becomes 0 after the concert (sell_in < 0)."""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 0, 40)]
        GildedRose(items).update_quality()
        self.assertEqual(0, items[0].quality)

    def test_conjured_item_degrades_twice_as_fast(self):
        """Conjured items degrade by 2 per day (twice normal speed)."""
        items = [Item("Conjured Mana Cake", 10, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(18, items[0].quality)

    # ─────────────────────────────────────────
    #  Quality boundary tests
    # ─────────────────────────────────────────

    def test_quality_never_negative(self):
        """Quality of an item is never negative."""
        items = [Item("Normal Item", 5, 0)]
        GildedRose(items).update_quality()
        self.assertEqual(0, items[0].quality)

    def test_aged_brie_quality_never_exceeds_50(self):
        """Quality of any item never exceeds 50."""
        items = [Item("Aged Brie", 10, 50)]
        GildedRose(items).update_quality()
        self.assertEqual(50, items[0].quality)

    # ─────────────────────────────────────────
    #  Aged Brie tests
    # ─────────────────────────────────────────

    def test_aged_brie_increases_in_quality(self):
        """Aged Brie increases in quality the older it gets."""
        items = [Item("Aged Brie", 10, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(21, items[0].quality)

    def test_aged_brie_increases_twice_after_sell_by(self):
        """Aged Brie increases by 2 after sell-by date."""
        items = [Item("Aged Brie", 0, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(22, items[0].quality)

    # ─────────────────────────────────────────
    #  Sulfuras tests
    # ─────────────────────────────────────────

    def test_sulfuras_quality_never_changes(self):
        """Sulfuras, being legendary, never loses quality."""
        items = [Item("Sulfuras, Hand of Ragnaros", 5, 80)]
        GildedRose(items).update_quality()
        self.assertEqual(80, items[0].quality)

    def test_sulfuras_sell_in_never_changes(self):
        """Sulfuras never has to be sold – sell_in stays the same."""
        items = [Item("Sulfuras, Hand of Ragnaros", 5, 80)]
        GildedRose(items).update_quality()
        self.assertEqual(5, items[0].sell_in)

    # ─────────────────────────────────────────
    #  Backstage pass tests
    # ─────────────────────────────────────────

    def test_backstage_pass_increases_by_1_when_far_from_concert(self):
        """Quality increases by 1 when sell_in > 10."""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 15, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(21, items[0].quality)

    def test_backstage_pass_increases_by_2_within_10_days(self):
        """Quality increases by 2 when sell_in is 6–10."""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 10, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(22, items[0].quality)

    def test_backstage_pass_increases_by_3_within_5_days(self):
        """Quality increases by 3 when sell_in is 1–5."""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(23, items[0].quality)

    # ─────────────────────────────────────────
    #  Conjured tests
    # ─────────────────────────────────────────

    def test_conjured_degrades_by_4_after_sell_by(self):
        """Conjured items degrade by 4 after sell-by date (2× the double rate)."""
        items = [Item("Conjured Mana Cake", 0, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(16, items[0].quality)

    def test_conjured_quality_never_negative(self):
        """Conjured item quality floor is still 0."""
        items = [Item("Conjured Mana Cake", 5, 1)]
        GildedRose(items).update_quality()
        self.assertEqual(0, items[0].quality)


if __name__ == '__main__':
    unittest.main()