/**
 * ============================================================================
 * 🤖 Artificial Sort (আর্টিফিশিয়াল সর্ট) — JavaScript (Node.js) Implementation
 * ============================================================================
 * Author: Ashikur Rahman
 * Institution: Department of CSE, Green University of Bangladesh
 * Core Innovation: Half-Pass Dual-Stream In-Place Merging (O(1) Auxiliary Space)
 * ============================================================================
 */

function swap(arr, i, j) {
  const temp = arr[i];
  arr[i] = arr[j];
  arr[j] = temp;
}

/**
 * In-place merge of arr[l..mid] and arr[mid+1..r]
 * with O(1) auxiliary heap space.
 */
function artificialMerge(arr, l, mid, r) {
  if (l >= r || mid < l || mid >= r) return;
  if (arr[mid] <= arr[mid + 1]) return; // Skip if boundary already sorted

  let ap = mid + 1; // Stream A head (displaced left elements buffer)
  let rp = mid + 1; // Stream B head (original right elements)
  let lp = l;       // Left pointer (active destination slot)

  // Half-Pass Traversal: Loop solely processes the left half (0 to mid)
  while (lp <= mid) {
    if (ap === rp) {
      if (rp > r || arr[lp] <= arr[rp]) {
        lp++;
      } else {
        swap(arr, lp++, rp++);
      }
    } else {
      const cand_A = arr[ap];
      const cand_B = (rp <= r) ? arr[rp] : Infinity;

      if (arr[lp] <= cand_A && arr[lp] <= cand_B) {
        lp++;
      } else if (cand_B < cand_A) {
        swap(arr, lp++, rp++);
      } else {
        swap(arr, lp, ap);
        let cur = ap;
        while (cur + 1 < rp) {
          swap(arr, cur, cur + 1);
          cur++;
        }
        lp++;
      }
    }
  }

  // Right half now consists of two contiguous sorted streams partitioned at split
  const split = rp - 1;
  artificialMerge(arr, mid + 1, split, r);
}

/**
 * Main Artificial Sort caller
 */
function artificialSort(arr, l = 0, r = arr.length - 1) {
  if (l >= r) return;
  const mid = l + ((r - l) >> 1);
  artificialSort(arr, l, mid);
  artificialSort(arr, mid + 1, r);
  artificialMerge(arr, l, mid, r);
}

// Module export for testing & external usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { artificialSort, artificialMerge };
}

// Demonstration run
if (require.main === module) {
  const arr = [15, 26, 27, 23, 1, 28, 24, 22, 11, 26, 27, 7, 5, 5, 18, 3];
  console.log("Original array:   ", arr);
  artificialSort(arr);
  console.log("Sorted array:     ", arr);
}
