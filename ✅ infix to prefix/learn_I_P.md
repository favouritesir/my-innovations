# 🎓 Learn In-Place Infix to Prefix (Zero Learning Curve Tutorial)

> *"Why allocate new memory and perform three tedious passes of string reversals when you can transform the expression right inside its own skin?"*  
> **Author & Researcher:** Ashikur Rahman (Department of CSE, Green University of Bangladesh)  
> 🌐 **[বাংলায় টিউটোরিয়ালটি পড়তে এখানে ক্লিক করুন (learn_I_P_Bangla.md) &raquo;](learn_I_P_Bangla.md)**

---

## 📖 Table of Contents
1. [The Big Picture: What Problem Are We Solving?](#1-the-big-picture-what-problem-are-we-solving)
2. [The Textbook Way vs. The In-Place Way](#2-the-textbook-way-vs-the-in-place-way)
3. [The Core Intuition: The "Right-to-Left Dual Runner" Model](#3-the-core-intuition-the-right-to-left-dual-runner-model)
4. [The Golden Safety Invariant: Why You Never Step on Your Own Toes](#4-the-golden-safety-invariant-why-you-never-step-on-your-own-toes)
5. [The Operator Stack: An Orderly Parking Lot](#5-the-operator-stack-an-orderly-parking-lot)
6. [Step-by-Step Visual Walkthrough (Tracing `(A+B)*C`)](#6-step-by-step-visual-walkthrough-tracing-abc)
7. [Line-by-Line Code Breakdown (C Reference)](#7-line-by-line-code-breakdown-c-reference)
8. [The Grand Finale: The Index-0 Shift](#8-the-grand-finale-the-index-0-shift)
9. [Beginner FAQ & Common Confusions](#9-beginner-faq--common-confusions)

---

## 1. The Big Picture: What Problem Are We Solving?

In computer science, humans write mathematical expressions in **Infix Notation**, where the operator sits comfortably between operands:
$$\text{Human Friendly (Infix): } A + B$$

However, compilers, calculators, and hardware stack machines find Infix ambiguous without parentheses. They prefer **Prefix Notation** (also known as *Polish Notation*, invented by Jan Łukasiewicz in 1924), where the operator comes before its operands:
$$\text{Machine Friendly (Prefix): } + A B$$

### Another Example:
- **Infix:** `(A + B) * C`
- **Prefix:** `* + A B C`

Our challenge: Build an algorithm that takes an Infix string and converts it directly to Prefix.

---

## 2. The Textbook Way vs. The In-Place Way

If you open almost any Data Structures textbook (or Google "Infix to Prefix"), you will be taught a cumbersome 3-pass pipeline:

```text
The Traditional Textbook Pipeline (3 Passes + Extra Memory):
[ (A + B) * C ] 
      │
      ▼  Pass 1: Reverse String & Swap Parentheses '(' <-> ')'
[ C * (B + A) ]
      │
      ▼  Pass 2: Standard Infix-to-Postfix (allocates NEW array of size N)
[ C B A + * ]
      │
      ▼  Pass 3: Reverse Resulting Postfix String
[ * + A B C ]  ==> Done, but burned extra RAM & 3 full memory passes!
```

### Why this is inefficient:
1. **Wastes RAM ($O(N)$ space):** On tiny microcontrollers (e.g., Arduino Uno with only 2 KB RAM), allocating secondary strings leads directly to **Out-Of-Memory (OOM) crashes**.
2. **Poor Cache Performance:** Reversing back and forth across different memory buffers causes CPU cache thrashing.

### The In-Place Innovation:
Instead of flipping the string back and forth, **we scan directly from Right to Left, and write the output from Right to Left into the EXACT SAME array!**

```text
The In-Place Single-Buffer Pipeline (Zero Extra String Memory):
Input Buffer:  [ ( A + B ) * C ]
                 ▲           ▲
                 │           │
             read_idx    write_idx (both start at the end and walk backward!)
```

---

## 3. The Core Intuition: The "Right-to-Left Dual Runner" Model

Imagine an asphalt road with characters painted on it. You have two walkers moving from **right to left**:

1. **The Reader (`read_idx`):** Inspects the character currently painted on the ground.
2. **The Writer (`write_idx`):** Paints the final prefix characters onto the asphalt.

```text
Direction of motion: <================== (Walking Backward)

  Index:    0    1    2    3    4    5    6
  Array:  [ ( ][ A ][ + ][ B ][ ) ][ * ][ C ]
                                          ▲
                                          │
                                 read_idx, write_idx
```

Both start at `len - 1` (the very last character).

---

## 4. The Golden Safety Invariant: Why You Never Step on Your Own Toes

The first question every smart student asks:  
> *"If the writer is writing into the same array that the reader is reading from, won't the writer overwrite and destroy characters that haven't been read yet?"*

The answer is: **No, absolutely never!**

### The Invariant:
$$\mathbf{read\_idx \le write\_idx} \quad \text{(At every single micro-step)}$$

Why is `read_idx` always ahead of (or equal to) `write_idx`?

1. **Operands are written 1-to-1:** When `read_idx` sees an operand (like `C`, `B`, `A`), it immediately writes it to `write_idx`. Both pointers decrement by 1. The distance between them remains zero!
2. **Parentheses disappear:** When `read_idx` sees `)` or `(`, it **does not write them**. `read_idx` takes a step backward, but `write_idx` stands still! This opens up a **safety gap** where `write_idx` stays safely behind `read_idx`.
3. **Operators go to the Stack:** When `read_idx` sees `+` or `*`, it pushes it onto an operator stack instead of immediately writing it. Again, `read_idx` steps backward, but `write_idx` stays behind.

Because characters are either dropped (parentheses) or held temporarily in the stack (operators), **the reader is ALWAYS ahead of the writer.** Unread characters are never overwritten!

---

## 5. The Operator Stack: An Orderly Parking Lot

When moving Right-to-Left, the rules of operator precedence and associativity are slightly adjusted to naturally produce Prefix notation:

### Precedence Table:
| Operator | Priority | Associativity |
| :---: | :---: | :---: |
| `+`, `-` | **1** | Left-to-Right |
| `*`, `/`, `%` | **2** | Left-to-Right |
| `^` (Power) | **3** | Right-to-Left |

### The Right-to-Left Popping Rule:
When incoming operator `current` meets `stack.top()`:
- For **Left-associative** (`+`, `-`, `*`, `/`): Pop the stack if incoming priority is **strictly less than** stack top (`priority(curr) < priority(top)`).
- For **Right-associative** (`^`): Pop the stack if incoming priority is **less than or equal** (`priority(curr) <= priority(top)`).

*(Parentheses rule: `)` is pushed onto the stack. When `(` arrives, pop and write everything until `)` is popped, then discard both brackets).*

---

## 6. Step-by-Step Visual Walkthrough (Tracing `(A+B)*C`)

Let us trace the famous textbook expression: `(A+B)*C`  
Length $L = 7$. Initial indices: `read_idx = 6`, `write_idx = 6`.

```text
Initial State:
Index:     0   1   2   3   4   5   6
Array:   [ (   A   +   B   )   *   C ]
                                   ▲
                           read_idx, write_idx
Stack: []
```

### Step 1: `read_idx = 6` (Token = `'C'`)
- `'C'` is an operand.
- Action: Write directly `str[write_idx--] = 'C'`.
- `read_idx` decrements to 5.
```text
Array:   [ (   A   +   B   )   *   C ]
                               ▲   ▲
                        read_idx   write_idx
Stack: []
```

### Step 2: `read_idx = 5` (Token = `'*'`)
- `'*'` is an operator. Stack is empty, so push `'*'`.
- `write_idx` stays at 5. `read_idx` decrements to 4.
```text
Array:   [ (   A   +   B   )   *   C ]
                           ▲       ▲
                    read_idx       write_idx (Gap opened!)
Stack: ['*']
```

### Step 3: `read_idx = 4` (Token = `')'`)
- `')'` is a closing bracket. Push `')'` to stack.
- `read_idx` decrements to 3.
```text
Stack: ['*', ')']
```

### Step 4: `read_idx = 3` (Token = `'B'`)
- `'B'` is an operand.
- Action: Write `str[write_idx--] = 'B'`.
- `write_idx` was 5, so `'B'` is written at index 5!
- Notice: Index 5 previously held `'*'`, but `'*'` is already safely saved in our stack!
```text
Array:   [ (   A   +   B   )   B   C ]
                       ▲       ▲
                read_idx       write_idx
Stack: ['*', ')']
```

### Step 5: `read_idx = 2` (Token = `'+'`)
- `'+'` is an operator. Stack top is `')'`, so push `'+'`.
- `read_idx` decrements to 1.
```text
Stack: ['*', ')', '+']
```

### Step 6: `read_idx = 1` (Token = `'A'`)
- `'A'` is an operand.
- Action: Write `str[write_idx--] = 'A'` at index 4.
```text
Array:   [ (   A   +   B   A   B   C ]
                   ▲       ▲
            read_idx       write_idx
Stack: ['*', ')', '+']
```

### Step 7: `read_idx = 0` (Token = `'('`)
- `'('` is an opening bracket!
- Pop stack until `')'`:
  - Pop `'+'` $\rightarrow$ Write at `str[write_idx--]` (index 3).
  - Pop `')'` $\rightarrow$ Discard.
- `read_idx` decrements to -1 (Reading complete!).
```text
Array:   [ (   A   +   +   A   B   C ]
                       ▲
                   write_idx = 2
Stack: ['*']
```

### Step 8: Drain Stack
- Stack still holds `['*']`.
- Pop `'*'` $\rightarrow$ Write at `str[write_idx--]` (index 2).
- `write_idx` becomes 1.
```text
Final Raw Buffer:
Index:     0   1   2   3   4   5   6
Array:   [ (   A   *   +   A   B   C ]
                   ▲               ▲
             write_idx+1          len-1
                   └──────┬────────┘
                    Valid Prefix Output!
```

Look at indices 2 through 6: **`* + A B C`**!  
The prefix expression has formed naturally at the right side of our array!

---

## 7. Line-by-Line Code Breakdown (C Reference)

Here is the clean ~45 lines C function:

```c
void makePrefixInPlace(char str[]) {
    int len = strlen(str);
    int read_idx = len - 1;   // Pointer 1: Walking backward reading tokens
    int write_idx = len - 1;  // Pointer 2: Walking backward writing output

    while (read_idx >= 0) {
        char current = str[read_idx];

        // 1. Closing bracket is pushed directly
        if (current == ')') {
            push(current);
        } 
        // 2. Opening bracket unloads stack until matching ')'
        else if (current == '(') {
            char x;
            while ((x = pop()) != ')' && x != -1) {
                str[write_idx--] = x;
            }
        } 
        // 3. Operator: pop higher/equal priority, then push
        else if (priority(current) > 0) {
            while (top != -1 && stack[top] != ')') {
                int p_curr = priority(current);
                int p_top = priority(stack[top]);
                if (p_curr < p_top || (p_curr == p_top && isRightAssociative(current))) {
                    str[write_idx--] = pop();
                } else {
                    break;
                }
            }
            push(current);
        } 
        // 4. Operand: written immediately
        else if (isalnum(current)) {
            str[write_idx--] = current;
        }
        
        read_idx--;
    }

    // Drain remaining operators from stack
    while (top != -1) {
        char x = pop();
        if (x != ')' && x != '(') {
            str[write_idx--] = x;
        }
    }

    // Step 5: Shift prefix substring to start at index 0
    int new_len = len - 1 - write_idx;
    for (int i = 0; i < new_len; i++) {
        str[i] = str[write_idx + 1 + i];
    }
    str[new_len] = '\0'; // Null terminator
}
```

---

## 8. The Grand Finale: The Index-0 Shift

Because parentheses were dropped, the final prefix string is shorter than the original infix string:
- Original Infix length: 7 (`(A+B)*C`)
- Final Prefix length: 5 (`*+ABC`)

At the end of the loop, our result is sitting at indices `2..6` (`write_idx + 1` to `len - 1`).

All we do is a simple linear shift:
```text
From:  [ ( ][ A ][ * ][ + ][ A ][ B ][ C ]
                   ▲
             write_idx + 1

To:    [ * ][ + ][ A ][ B ][ C ][ \0 ]
         0    1    2    3    4     5
```
Now `str` is a perfectly valid, standard, null-terminated C string starting at index `0`!

---

## 9. Beginner FAQ & Common Confusions

### Q1: Is the stack itself in-place?
**Answer:** The *string buffer* is 100% in-place ($O(1)$ auxiliary string allocation). We use a small operator stack for precedence handling, which takes at most $O(N)$ characters. In microcontrollers, a tiny fixed stack of 30–50 bytes handles even the most monstrous math formulas.

### Q2: What happens if an expression has unmatched parentheses like `(A+B`?
**Answer:** The code contains guards (`x != -1`, `top != -1`, and boundary checks). It will safely flush valid operators without crashing or freezing.

### Q3: Why is right-associativity (`^`) treated with `<=` instead of `<`?
**Answer:**  
In Infix, `A^B^C` means $A^{(B^C)}$.  
When reading backward (Right to Left):
1. `C` is written.
2. `^` (right one) is pushed.
3. `B` is written.
4. When `^` (left one) arrives, its priority is equal to stack top. Because it is right-associative, the right power must execute first. Therefore, the stack top is popped and written before pushing the new `^`. This produces `^A^BC`, which correctly evaluates as $A^{(B^C)}$.

---

## 🌟 Summary: Three Words to Remember
1. **Backward Scan:** Read from right to left.
2. **Backward Write:** Write from right to left into the same array.
3. **Shift Left:** Move the final compact string to index 0.

*Zero extra string arrays. Zero string reversals. Pure algorithmic elegance.*