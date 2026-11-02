/**
 * ============================================================================
 * 🤖 Artificial Sort (আর্টিফিশিয়াল সর্ট) — Reference C Implementation
 * ============================================================================
 * Author: Ashikur Rahman
 * Institution: Department of CSE, Green University of Bangladesh
 * Core Innovation: Half-Pass Dual-Stream In-Place Merging (O(1) Auxiliary Space)
 * Memory Model: Zero malloc, zero auxiliary arrays, pure in-situ memory.
 * ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

/**
 * In-place element swap using pointers
 */
static inline void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

/**
 * artificial_merge: Merges arr[l..mid] and arr[mid+1..r] in-place
 * with zero auxiliary memory using dual-stream artificial buffering.
 * 
 * @param arr: The array containing both sorted segments
 * @param l: Start index of the left segment
 * @param mid: End index of the left segment
 * @param r: End index of the right segment
 */
void artificial_merge(int arr[], int l, int mid, int r) {
    // Boundary guards
    if (l >= r || mid < l || mid >= r) return;
    if (arr[mid] <= arr[mid + 1]) return; // Skip if already globally ordered

    int ap = mid + 1; // Stream A head (displaced left elements buffer)
    int rp = mid + 1; // Stream B head (original right elements)
    int lp = l;       // Left pointer (active destination slot)

    // Half-Pass Traversal: Loop strictly iterates across the left half
    while (lp <= mid) {
        if (ap == rp) {
            // Buffer Stream A is currently empty
            if (rp > r || arr[lp] <= arr[rp]) {
                lp++;
            } else {
                swap(&arr[lp], &arr[rp]);
                lp++;
                rp++;
            }
        } else {
            int cand_A = arr[ap];
            bool has_B = (rp <= r);
            int cand_B = has_B ? arr[rp] : 0;

            if (arr[lp] <= cand_A && (!has_B || arr[lp] <= cand_B)) {
                // Current left element is the smallest; stays in-situ
                lp++;
            } else if (has_B && cand_B < cand_A) {
                // Stream B element is smallest; swap into active left slot
                swap(&arr[lp], &arr[rp]);
                lp++;
                rp++;
            } else {
                // Stream A element is smallest; swap and cycle displaced element to buffer tail
                swap(&arr[lp], &arr[ap]);
                int cur = ap;
                while (cur + 1 < rp) {
                    swap(&arr[cur], &arr[cur + 1]);
                    cur++;
                }
                lp++;
            }
        }
    }

    // Split point directly separates remaining sorted Stream A and Stream B
    int split = rp - 1;
    artificial_merge(arr, mid + 1, split, r);
}

/**
 * artificial_sort: Main recursive entry point for Artificial Sort
 * 
 * @param arr: The array to sort
 * @param l: Left boundary
 * @param r: Right boundary
 */
void artificial_sort(int arr[], int l, int r) {
    if (l >= r) return;
    int mid = l + ((r - l) >> 1);
    artificial_sort(arr, l, mid);
    artificial_sort(arr, mid + 1, r);
    artificial_merge(arr, l, mid, r);
}

#ifdef TEST_MAIN
int main(void) {
    int arr[] = {15, 26, 27, 23, 1, 28, 24, 22, 11, 26, 27, 7, 5, 5, 18, 3};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("Original Array:\n");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n\n");

    artificial_sort(arr, 0, n - 1);

    printf("Artificially Sorted Array:\n");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");

    return 0;
}
#endif
