# Gilded Rose Refactoring Kata — Workspace Instructions

## Project Overview

The **Gilded Rose Refactoring Kata** is a classic coding exercise for practicing refactoring skills on legacy code. The code simulates an inventory management system for a shop, with complex business rules for different item types (normal items, Aged Brie, Sulfuras, Backstage passes, Conjured items).

For full requirements, see [GildedRoseRequirements.md](../GildedRoseRequirements.md).

## Primary Language: Python

This workspace focuses on the **Python implementation** in the `python/` directory.

### Current Architecture

- **Pattern**: Strategy Pattern (item type → updater class)
- **Classes**:
  - `Item`: immutable data class (DO NOT ALTER per kata rules)
  - `ItemUpdater`: base strategy for normal items
  - `AgedBrieUpdater`: increases in quality with age
  - `SulfurasUpdater`: legendary item, never changes
  - `BackstagePassUpdater`: quality increases as concert approaches
  - `ConjuredUpdater`: degrades twice as fast
  - `GildedRose`: main orchestrator

## Development Workflow

### Testing Framework
- **Unit tests**: `pytest` (run with `python -m pytest`)
- **Approval tests**: `approvaltests` for snapshot-based testing
- **Coverage**: enabled via `pytest-cov`

### Running Tests

```bash
# From the python/ directory

# Run all unit tests
python -m pytest tests/test_gilded_rose.py -v

# Run approval tests
python -m pytest tests/test_gilded_rose_approvals.py -v

# Run with coverage
python -m pytest tests/ --cov=gilded_rose --cov-report=term-pretty

# Run texttest fixture (for manual exploration)
python texttest_fixture.py 10
```

### Kata Best Practices

1. **Work in small steps**: make one small change, run the tests immediately
2. **Never break tests**: if a refactoring breaks a test, revert and try differently
3. **Add tests before refactoring**: write approval tests or unit tests to capture current behavior
4. **Avoid big rewrites**: the goal is to practice incremental refactoring, not rewriting from scratch

## Key Files

| File | Purpose |
|------|---------|
| `python/gilded_rose.py` | Main implementation (Item, GildedRose, updater strategies) |
| `python/tests/test_gilded_rose.py` | Unit tests (add test cases here) |
| `python/tests/test_gilded_rose_approvals.py` | Snapshot-based approval tests |
| `python/texttest_fixture.py` | Interactive test runner (main code execution) |
| `python/requirements.txt` | Dependencies (pytest, approvaltests, coverage) |
| `python/tests/conftest.py` | Pytest configuration & fixtures |

## Common Tasks

### Add a New Test Case
Edit `python/tests/test_gilded_rose.py` and add a test method. For example:
```python
def test_conjured_item_degrades_twice_as_fast():
    items = [Item("Conjured Mana Cake", 3, 6)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].quality == 4  # degraded by 2
```

### Run a Single Approval Test
```bash
cd python
python -m pytest tests/test_gilded_rose_approvals.py::test_golden_21_days -v
```

### View/Approve Snapshot Changes
After running approval tests, `.received.txt` files appear in `python/tests/approved_files/`. Rename them to `.approved.txt` to accept the change.

## Constraints (Kata Rules)

- ⚠️ **DO NOT** modify the `Item` class definition (the "goblin in the corner" rule)
- ⚠️ **DO NOT** alter the `GildedRose.items` property
- ✅ **DO** refactor the `update_quality()` method and add new code as needed

## Architecture Notes

### Current Refactored Design

The codebase uses the **Strategy Pattern** to eliminate the original giant conditional nest. Each item type (`ItemUpdater`, `AgedBrieUpdater`, etc.) encapsulates its own update logic:

```python
# Instead of:
# if name == "Aged Brie":
#     # brie logic
# elif name == "Sulfuras":
#     # sulfuras logic
# else:
#     # normal logic

# We use:
updater = strategy_map[item.name]
updater.update(item)
```

Benefits:
- Easier to add new item types
- Each updater is testable in isolation
- Clear separation of concerns

## Additional Testing Resources

- **TextTest** (approval testing, text-based): See [texttests/README.md](../texttests/README.md)
- **ApprovalTests.Python**: Snapshot testing for verifying behavior across multiple days
- **Manual testing**: Use `python texttest_fixture.py <days>` to see output

## Related Documentation

- [GildedRoseRequirements.md](../GildedRoseRequirements.md) — full business rules
- [CONTRIBUTING.md](../CONTRIBUTING.md) — how to contribute to the repo
- [python/README.md](./python/README.md) — Python-specific setup instructions
