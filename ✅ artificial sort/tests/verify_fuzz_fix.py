#!/usr/bin/env python3
"""
Exhaustive verification of Artificial Sort against the exact fuzzing cases
from the audit report (Negative numbers, Odd sizes, Alternating, Duplicates).
"""
import random
import sys

def artificial_merge(arr, l, mid, r):
    if l >= r or mid < l or mid >= r:
        return
    if arr[mid] <= arr[mid + 1]:
        return

    ap = mid + 1
    rp = mid + 1
    lp = l

    while lp <= mid:
        if ap == rp:
            if rp > r or arr[lp] <= arr[rp]:
                lp += 1
            else:
                arr[lp], arr[rp] = arr[rp], arr[lp]
                lp += 1
                rp += 1
        else:
            cand_A = arr[ap]
            has_B = (rp <= r)
            # FIXED SENTINEL: uses float('inf') / INT_MAX instead of 0
            cand_B = arr[rp] if has_B else float('inf')

            if arr[lp] <= cand_A and arr[lp] <= cand_B:
                lp += 1
            elif cand_B < cand_A:
                arr[lp], arr[rp] = arr[rp], arr[lp]
                lp += 1
                rp += 1
            else:
                arr[lp], arr[ap] = arr[ap], arr[lp]
                cur = ap
                while cur + 1 < rp:
                    arr[cur], arr[cur + 1] = arr[cur + 1], arr[cur]
                    cur += 1
                lp += 1

    split = rp - 1
    artificial_merge(arr, mid + 1, split, r)

def artificial_sort(arr, l=0, r=None):
    if r is None:
        r = len(arr) - 1
    if l >= r:
        return
    mid = l + ((r - l) >> 1)
    artificial_sort(arr, l, mid)
    artificial_sort(arr, mid + 1, r)
    artificial_merge(arr, l, mid, r)

print("=" * 70)
print("🎯 RUNNING THE EXACT AUDIT FAILING CASES WITH FIXED SENTINEL:")
print("=" * 70)

# 1. Audit Case: Alternating
arr1 = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10]
artificial_merge(arr1, 0, 4, 9)
print("1. Alternating [1,3,5,7,9 | 2,4,6,8,10]:")
print("   Result:  ", arr1)
print("   Expected:", sorted(arr1))
assert arr1 == sorted(arr1), "Alternating failed!"
print("   STATUS:   PASSED ✔️")

# 2. Audit Case: Odd Size & Negative Numbers
arr2 = [-5, -4, 1, -8, -2]
artificial_merge(arr2, 0, 2, 4)
print("\n2. Odd size with Negatives [-5, -4, 1 | -8, -2]:")
print("   Result:  ", arr2)
print("   Expected:", sorted(arr2))
assert arr2 == sorted(arr2), "Odd Size Negatives failed!"
print("   STATUS:   PASSED ✔️")

# 3. Audit Case: Sentinel Fails
arr3 = [-85, 78, -75, -5, 38]
artificial_merge(arr3, 0, 1, 4)
print("\n3. Negative & Mixed Sign [-85, 78 | -75, -5, 38]:")
print("   Result:  ", arr3)
print("   Expected:", sorted(arr3))
assert arr3 == sorted(arr3), "Sentinel case failed!"
print("   STATUS:   PASSED ✔️")

# 4. Stress Fuzzing 100,000 cases
print("\n" + "=" * 70)
print("🚀 STRESS FUZZING 100,000 RANDOM CASES (Negative, Odd, Duplicates)...")
fails = 0
for i in range(100000):
    n = random.randint(2, 60)
    mid = random.randint(0, n - 2)
    left = sorted([random.randint(-200, 200) for _ in range(mid + 1)])
    right = sorted([random.randint(-200, 200) for _ in range(n - mid - 1)])
    arr = left + right
    expected = sorted(arr)
    artificial_merge(arr, 0, mid, n - 1)
    if arr != expected:
        fails += 1
        if fails <= 3:
            print(f"Fail case: left={left}, right={right}, got={arr}")

print(f"Total Failures out of 100,000 runs: {fails}")
assert fails == 0, "Fuzzing found failures!"
print("🎉 ALL 100,000 FUZZING TESTS PASSED WITH ZERO ERRORS!")
print("=" * 70)
