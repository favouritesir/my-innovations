#!/usr/bin/env python3
"""
Artificial Sort Merge Logic - Exact Python Transliteration for Fuzzing
Tests the merge step directly on pre-sorted halves.
"""

import random
import sys

def artificial_merge_py(arr, l, mid, r):
    """Exact Python port of the C artificial_merge logic."""
    # Boundary guards
    if l >= r or mid < l or mid >= r:
        return
    if arr[mid] <= arr[mid + 1]:
        return

    ap = mid + 1  # Stream A head
    rp = mid + 1  # Stream B head
    lp = l        # Left pointer

    # Half-Pass Traversal
    while lp <= mid:
        if ap == rp:
            # Buffer Stream A is currently empty
            if rp > r or arr[lp] <= arr[rp]:
                lp += 1
            else:
                arr[lp], arr[rp] = arr[rp], arr[lp]
                lp += 1
                rp += 1
        else:
            cand_A = arr[ap]
            has_B = (rp <= r)
            # FIXED: Use infinity sentinel to match C's INT_MAX
            cand_B = arr[rp] if has_B else float('inf') 

            if arr[lp] <= cand_A and (not has_B or arr[lp] <= cand_B):
                lp += 1
            elif has_B and cand_B < cand_A:
                arr[lp], arr[rp] = arr[rp], arr[lp]
                lp += 1
                rp += 1
            else:
                # Stream A element is smallest
                arr[lp], arr[ap] = arr[ap], arr[lp]
                cur = ap
                while cur + 1 < rp:
                    arr[cur], arr[cur + 1] = arr[cur + 1], arr[cur]
                    cur += 1
                lp += 1

    split = rp - 1
    if mid + 1 < split: # Need at least 2 elements to recurse
        artificial_merge_py(arr, mid + 1, split, r)

def reference_merge(arr, l, mid, r):
    """Standard merge using extra space for verification."""
    left = arr[l:mid+1]
    right = arr[mid+1:r+1]
    i = j = 0
    k = l
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    while i < len(left):
        arr[k] = left[i]
        i += 1; k += 1
    while j < len(right):
        arr[k] = right[j]
        j += 1; k += 1

def test_merge_case(original_arr, l, mid, r, test_name):
    """Test a single merge case."""
    arr_test = original_arr[:]
    arr_ref = original_arr[:]
    
    artificial_merge_py(arr_test, l, mid, r)
    reference_merge(arr_ref, l, mid, r)
    
    if arr_test != arr_ref:
        print(f"\n❌ FAIL: {test_name}")
        print(f"   Input:    {original_arr}")
        print(f"   Range:    l={l}, mid={mid}, r={r}")
        print(f"   Left:     {original_arr[l:mid+1]}")
        print(f"   Right:    {original_arr[mid+1:r+1]}")
        print(f"   Got:      {arr_test}")
        print(f"   Expected: {arr_ref}")
        return False
    return True

def fuzz_sorted_halves(iterations=100000):
    """Generate random arrays where halves are pre-sorted."""
    print(f"🔬 Fuzzing {iterations} random sorted-halves cases...")
    
    fail_cases = []
    
    for i in range(iterations):
        # Random size 2 to 50
        n = random.randint(2, 50)
        mid = random.randint(0, n - 2) # Ensure both halves have at least 1 element
        l = 0
        r = n - 1
        
        # Generate random sorted halves
        # Include negative numbers, duplicates, large ranges
        left = sorted([random.randint(-100, 100) for _ in range(mid - l + 1)])
        right = sorted([random.randint(-100, 100) for _ in range(r - mid)])
        
        arr = left + right
        
        if not test_merge_case(arr, l, mid, r, f"RandomFuzz_{i}"):
            fail_cases.append((arr[:], l, mid, r))
            if len(fail_cases) >= 10:
                break
    
    # Specific Adversarial Patterns
    print("\n🎯 Testing Specific Adversarial Patterns...")
    
    # 1. Alternating (Classic worst case)
    for n in [8, 10, 12, 14, 16, 15, 17, 31, 32, 33]:
        left = list(range(1, n//2 + 1, 2)) + list(range(2, n//2 + 1, 2)) # Not strictly alternating halves
        # True alternating merge input: Left=[1,3,5...], Right=[2,4,6...]
        left = [2*i + 1 for i in range((n+1)//2)]
        right = [2*i + 2 for i in range(n//2)]
        arr = left + right
        mid = len(left) - 1
        if not test_merge_case(arr, 0, mid, n-1, f"Alternating_N={n}"):
            fail_cases.append((arr[:], 0, mid, n-1))

    # 2. Negative Numbers (Sentinel Bug)
    print("\n🧪 Testing Negative Numbers (Sentinel 0 Bug)...")
    for _ in range(1000):
        n = random.randint(4, 20)
        mid = random.randint(1, n-2)
        left = sorted([random.randint(-50, -1) for _ in range(mid + 1)])
        right = sorted([random.randint(-50, -1) for _ in range(n - mid - 1)])
        arr = left + right
        if not test_merge_case(arr, 0, mid, n-1, "NegativeNumbers"):
            fail_cases.append((arr[:], 0, mid, n-1))
            break
            
    # 3. Mixed Sign
    print("\n🧪 Testing Mixed Sign...")
    for _ in range(1000):
        n = random.randint(4, 20)
        mid = random.randint(1, n-2)
        left = sorted([random.randint(-10, 10) for _ in range(mid + 1)])
        right = sorted([random.randint(-10, 10) for _ in range(n - mid - 1)])
        arr = left + right
        if not test_merge_case(arr, 0, mid, n-1, "MixedSign"):
            fail_cases.append((arr[:], 0, mid, n-1))
            break

    # 4. All Duplicates
    print("\n🧪 Testing All Duplicates...")
    for val in [-5, 0, 5, 100]:
        for n in [3, 4, 5, 6, 7, 8, 9, 10, 15, 16, 17]:
            mid = n // 2
            arr = [val] * n
            if not test_merge_case(arr, 0, mid, n-1, f"Duplicates_{val}_N={n}"):
                fail_cases.append((arr[:], 0, mid, n-1))

    # 5. Odd Sizes (Left larger than Right)
    print("\n🧪 Testing Odd Sizes (Left > Right)...")
    for n in [3, 5, 7, 9, 11, 15, 17, 31]:
        mid = (n - 1) // 2 # Left has one more
        left = sorted([random.randint(-10, 10) for _ in range(mid + 1)])
        right = sorted([random.randint(-10, 10) for _ in range(n - mid - 1)])
        arr = left + right
        if not test_merge_case(arr, 0, mid, n-1, f"OddSize_N={n}"):
            fail_cases.append((arr[:], 0, mid, n-1))

    return fail_cases

if __name__ == "__main__":
    fails = fuzz_sorted_halves(50000)
    
    print("\n" + "="*60)
    if fails:
        print(f"💥 TOTAL FAILURES FOUND: {len(fails)}")
        print("="*60)
        for i, (arr, l, mid, r) in enumerate(fails[:5]): # Show first 5 unique
            print(f"\n--- Failure #{i+1} ---")
            print(f"Array: {arr}")
            print(f"l={l}, mid={mid}, r={r}")
            print(f"Left (sorted):  {arr[l:mid+1]}")
            print(f"Right (sorted): {arr[mid+1:r+1]}")
            
            # Run again to show output
            arr_test = arr[:]
            artificial_merge_py(arr_test, l, mid, r)
            arr_ref = arr[:]
            reference_merge(arr_ref, l, mid, r)
            print(f"Algorithm Output: {arr_test}")
            print(f"Correct Output:   {arr_ref}")
    else:
        print("✅ ALL TESTS PASSED - No correctness bugs found in this run.")
    print("="*60)