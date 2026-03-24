---
name: "Refactor Incrementally"
description: "Step-by-step guidance for test-driven refactoring in the Gilded Rose kata"
applyTo: ["python/gilded_rose.py", "python/tests/**/*.py"]
---

# Gilded Rose: Refactor Incrementally

You're practicing the Gilded Rose Refactoring Kata. The goal is **small, safe steps with continuous testing** — not big rewrites.

## Your Refactoring Task

**Code area:** {selection or: `python/gilded_rose.py`}

**Change goal:** {goal or refactoring objective}

## Step-by-Step Workflow

### 1. **Establish the baseline (one-time)**
```bash
cd python
python -m pytest tests/ -v                    # All tests should pass
python -m pytest tests/test_gilded_rose_approvals.py -v  # Approval tests
```

If any test fails, fix it before starting.

### 2. **Plan one small change**

Keep it **minimal**. Examples:
- Extract a single method from a larger function
- Rename one variable for clarity
- Add one `ItemUpdater` subclass for a new item type
- Simplify one conditional branch

Ask: *"Can I make this change in < 5 minutes?"* If not, split it further.

### 3. **Implement the change**

Make **only** this one change. Don't refactor related code yet.

```python
# Example: Extract a helper method
def _clamp_quality(self, value):
    """Keep quality within min/max bounds."""
    return max(self.MIN_QUALITY, min(self.MAX_QUALITY, value))
```

### 4. **Run the tests immediately** ✅

```bash
cd python
python -m pytest tests/test_gilded_rose.py -v      # Fast unit tests first
python -m pytest tests/test_gilded_rose_approvals.py -v  # Then approval tests
```

**If all tests pass:** ✓ Commit or stage this change and move to step 5.  
**If a test fails:** Revert this change (undo in editor) and rethink the approach.

### 5. **Repeat or stop**

- **More changes?** Go to step 2 with your next small change.
- **Done?** Run full suite once more:
  ```bash
  python -m pytest tests/ --cov=gilded_rose --cov-report=term-pretty
  ```

## A Few Questions to Help

1. **What specific code section should we refactor?** (method, class, conditional block)
2. **What's the end goal?** (e.g., "Extract BackstagePassUpdater", "Remove deeply nested ifs")
3. **Are there edge cases we should test first?** (If so, write a unit test before refactoring)

## Key Principles

| Principle | Why It Matters |
|-----------|----------------|
| **Test after every change** | Catch mistakes instantly; revert is safe |
| **Never break tests** | If you break something, undo immediately—don't fix tests |
| **Small steps only** | Easier to debug, easier to review, builds confidence |
| **Approval tests are your friend** | They verify multi-day behavior automatically |

## Debugging Failed Tests

**Approval test failed?**
```bash
# See what changed
diff -u python/tests/approved_files/test_golden_21_days.approved.txt \
         python/tests/approved_files/test_golden_21_days.received.txt

# If the change is correct, rename to approve:
mv python/tests/approved_files/test_golden_21_days.received.txt \
   python/tests/approved_files/test_golden_21_days.approved.txt
```

**Unit test failed?** Run it in isolation:
```bash
python -m pytest tests/test_gilded_rose.py::test_conjured_item_degrades_twice_as_fast -v
```

## Common Refactoring Patterns in This Codebase

- **Add new item type:** Create `NewItemUpdater(ItemUpdater)` subclass → add to `GildedRose.get_updater()`
- **Simplify quality logic:** Extract helper methods like `_increase_quality()`, `_decrease_quality()`
- **Remove conditionals:** Use Strategy Pattern to replace `if item.name == ...` chains

## Remember

> "Easy is the way" — The kata isn't about the result; it's about **practicing the discipline of incremental change and continuous validation.**

Ready? Pick one small change and start with step 2 above.
