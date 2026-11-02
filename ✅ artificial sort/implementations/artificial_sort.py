"""
============================================================================
🤖 Artificial Sort (আর্টিফিশিয়াল সর্ট) — Python 3 Implementation
============================================================================
Author: Ashikur Rahman
Institution: Department of CSE, Green University of Bangladesh
Core Innovation: Half-Pass Dual-Stream In-Place Merging (O(1) Auxiliary Space)
============================================================================
"""

def artificial_merge(arr, l, mid, r):
    """
    Merges arr[l..mid] and arr[mid+1..r] in-place with O(1) auxiliary space.
    """
    if l >= r or mid < l or mid >= r:
        return
    if arr[mid] <= arr[mid + 1]:
        return

    ap = mid + 1  # Stream A head (displaced left elements buffer)
    rp = mid + 1  # Stream B head (original right elements)
    lp = l

    # Half-Pass: Traverses exclusively across left half (lp <= mid)
    while lp <= mid:
        if ap == rp:
            if rp > r or arr[lp] <= arr[rp]:
                lp += 1
            else:
                arr[lp], arr[rp] = arr[rp], arr[lp]
                lp += 1
                rp += 1
        else:
            cand_a = arr[ap]
            cand_b = arr[rp] if rp <= r else float('inf')

            if arr[lp] <= cand_a and arr[lp] <= cand_b:
                lp += 1
            elif cand_b < cand_a:
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
    """
    Main Artificial Sort caller.
    """
    if r is None:
        r = len(arr) - 1
    if l >= r:
        return
    mid = l + ((r - l) >> 1)
    artificial_sort(arr, l, mid)
    artificial_sort(arr, mid + 1, r)
    artificial_merge(arr, l, mid, r)


if __name__ == "__main__":
    test_arr = [15, 26, 27, 23, 1, 28, 24, 22, 11, 26, 27, 7, 5, 5, 18, 3]
    print("Original array: ", test_arr)
    artificial_sort(test_arr)
    print("Sorted array:   ", test_arr)
