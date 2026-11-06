/**
 * ============================================================================
 * 🤖 Artificial Sort (আর্টিফিশিয়াল সর্ট) — Reference C Implementation (FIXED)
 * ============================================================================
 * Author: Ashikur Rahman
 * Institution: Department of CSE, Green University of Bangladesh
 * Core Innovation: Half-Pass Dual-Stream In-Place Merging (O(1) Auxiliary Space)
 * Memory Model: Zero malloc, zero auxiliary arrays, pure in-situ memory.
 * Verified Invariants:
 *   1. Sentinel Bug Fix: cand_B uses INT_MAX (+Infinity) when Stream B is exhausted.
 *   2. Odd Size & Boundary Safety: Strict rp <= r guards prevent out-of-bounds reads.
 *   3. Safe Split Tail Recursion: Handled deterministically by artificial_merge
 *      boundary guards, guaranteeing 100% precision on single-element buffers.
 * ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <limits.h>  // Required for INT_MAX sentinel

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
    // Boundary guards: Handles empty sub-arrays, inverted ranges, and single elements
    if (l >= r || mid < l || mid >= r) return;
    if (arr[mid] <= arr[mid + 1]) return; // Skip if already globally ordered

    int ap = mid + 1; // Stream A head (displaced left elements buffer)
    int rp = mid + 1; // Stream B head (original right elements)
    int lp = l;       // Left pointer (active destination slot)

    // Half-Pass Traversal: Loop strictly iterates across the left half
    while (lp <= mid) {
        if (ap == rp) {
            // Buffer Stream A is currently empty
            // Safe guard: rp > r checks if right stream is exhausted
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
            // SENTINEL FIX: Use INT_MAX as +Infinity so negative numbers in Stream A won't miscompare
            int cand_B = has_B ? arr[rp] : INT_MAX;

            // Candidate Arbitration Logic
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
    // Test Case 1: Negative Numbers (Sentinel Fix Verification)
    int arr1[] = {-85, 78, -75, -5, 38};
    int n1 = sizeof(arr1) / sizeof(arr1[0]);
    printf("Test 1 (Negatives): ");
    artificial_sort(arr1, 0, n1 - 1);
    for (int i = 0; i < n1; i++) printf("%d ", arr1[i]);
    printf("\n"); // Expected: -85 -75 -5 38 78

    // Test Case 2: Alternating (Tail Verification)
    int arr2[] = {1, 3, 5, 7, 9, 2, 4, 6, 8, 10};
    int n2 = sizeof(arr2) / sizeof(arr2[0]);
    printf("Test 2 (Alternating): ");
    artificial_sort(arr2, 0, n2 - 1);
    for (int i = 0; i < n2; i++) printf("%d ", arr2[i]);
    printf("\n"); // Expected: 1 2 3 4 5 6 7 8 9 10

    // Test Case 3: Odd Size (Left > Right)
    int arr3[] = {-5, -4, 1, -8, -2};
    int n3 = sizeof(arr3) / sizeof(arr3[0]);
    printf("Test 3 (Odd Size): ");
    artificial_sort(arr3, 0, n3 - 1);
    for (int i = 0; i < n3; i++) printf("%d ", arr3[i]);
    printf("\n"); // Expected: -8 -5 -4 -2 1

    // Test Case 4: Single Displaced Element Merge
    int arr4[] = {1, 5, 2, 4};
    int n4 = sizeof(arr4) / sizeof(arr4[0]);
    printf("Test 4 (Single Displaced): ");
    artificial_sort(arr4, 0, n4 - 1);
    for (int i = 0; i < n4; i++) printf("%d ", arr4[i]);
    printf("\n"); // Expected: 1 2 4 5

    // Test Case 5: Large Random Mixed
    int arr5[] = {15, 26, 27, 23, 1, 28, 24, 22, 11, 26, 27, 7, 5, 5, 18, 3};
    int n5 = sizeof(arr5) / sizeof(arr5[0]);
    printf("Test 5 (Mixed): ");
    artificial_sort(arr5, 0, n5 - 1);
    for (int i = 0; i < n5; i++) printf("%d ", arr5[i]);
    printf("\n"); // Expected: 1 3 5 5 7 11 15 18 22 23 24 26 26 27 27 28

    return 0;
}
#endif
