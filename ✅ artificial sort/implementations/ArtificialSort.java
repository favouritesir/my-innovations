/**
 * ============================================================================
 * 🤖 Artificial Sort (আর্টিফিশিয়াল সর্ট) — Java Implementation
 * ============================================================================
 * Author: Ashikur Rahman
 * Institution: Department of CSE, Green University of Bangladesh
 * Core Innovation: Half-Pass Dual-Stream In-Place Merging (O(1) Auxiliary Space)
 * ============================================================================
 */

import java.util.Arrays;

public class ArtificialSort {

    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    /**
     * In-place merge of arr[l..mid] and arr[mid+1..r] with O(1) auxiliary space.
     */
    public static void artificialMerge(int[] arr, int l, int mid, int r) {
        if (l >= r || mid < l || mid >= r) return;
        if (arr[mid] <= arr[mid + 1]) return; // Skip if boundary is already sorted

        int ap = mid + 1; // Stream A head (displaced left elements buffer)
        int rp = mid + 1; // Stream B head (original right elements)
        int lp = l;       // Left pointer (active destination slot)

        // Half-Pass Traversal: Loop iterates strictly over left sub-array (lp <= mid)
        while (lp <= mid) {
            if (ap == rp) {
                if (rp > r || arr[lp] <= arr[rp]) {
                    lp++;
                } else {
                    swap(arr, lp++, rp++);
                }
            } else {
                int candA = arr[ap];
                boolean hasB = (rp <= r);
                int candB = hasB ? arr[rp] : Integer.MAX_VALUE;

                if (arr[lp] <= candA && arr[lp] <= candB) {
                    lp++;
                } else if (hasB && candB < candA) {
                    swap(arr, lp++, rp++);
                } else {
                    swap(arr, lp, ap);
                    int cur = ap;
                    while (cur + 1 < rp) {
                        swap(arr, cur, cur + 1);
                        cur++;
                    }
                    lp++;
                }
            }
        }

        int split = rp - 1;
        artificialMerge(arr, mid + 1, split, r);
    }

    /**
     * Main recursive Artificial Sort method.
     */
    public static void sort(int[] arr, int l, int r) {
        if (l >= r) return;
        int mid = l + ((r - l) >> 1);
        sort(arr, l, mid);
        sort(arr, mid + 1, r);
        artificialMerge(arr, l, mid, r);
    }

    public static void sort(int[] arr) {
        if (arr != null && arr.length > 1) {
            sort(arr, 0, arr.length - 1);
        }
    }

    public static void main(String[] args) {
        int[] arr = {15, 26, 27, 23, 1, 28, 24, 22, 11, 26, 27, 7, 5, 5, 18, 3};
        System.out.println("Original: " + Arrays.toString(arr));
        sort(arr);
        System.out.println("Sorted:   " + Arrays.toString(arr));
    }
}
