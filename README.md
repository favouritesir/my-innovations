# 🚀 My Innovations | Original Algorithms & Systems Research

[![Author](https://img.shields.io/badge/Author-Ashikur_Rahman-blue.svg?style=for-the-badge&logo=github)](https://github.com/favouritesir)
[![DOI Infix-Prefix](https://img.shields.io/badge/DOI_Infix--Prefix-10.5281%2Fzenodo.23657544-107c10.svg?style=for-the-badge&logo=doi)](https://doi.org/10.5281/zenodo.23657544)
[![DOI Cloud-Sort](https://img.shields.io/badge/DOI_Cloud--Sort-10.5281%2Fzenodo.23665548-107c10.svg?style=for-the-badge&logo=doi)](https://doi.org/10.5281/zenodo.23665548)
[![Established](https://img.shields.io/badge/Origin-2022_--_Present-purple.svg?style=for-the-badge)](https://github.com/favouritesir/my-innovations)
[![Languages](https://img.shields.io/badge/Languages-C_|_JS_|_Python_|_Java_|_C%23-informational?style=for-the-badge)](https://github.com/favouritesir/my-innovations)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Testing Rigor](https://img.shields.io/badge/Validation-3--Tier_Stress_Tested-brightgreen.svg?style=for-the-badge)](https://github.com/favouritesir/my-innovations)

> *"Challenging textbook orthodoxies through aggressive memory optimization, in-place pointer discipline, and mathematical verification."*

Welcome to **`my-innovations`**. Unlike conventional repositories that replicate standard textbook implementations, this repository serves as a permanent research archive for **original algorithms, novel low-level optimizations, and systems programming experiments** conceived and developed by **Ashikur Rahman**.

---

## 📑 Table of Contents
- [📌 Repository Overview](#-repository-overview)
- [✨ Core Engineering Philosophy](#-core-engineering-philosophy)
- [📂 Featured Projects Catalog](#-featured-projects-catalog)
- [🗺️ Upcoming Research & Projects Roadmap](#️-upcoming-research--projects-roadmap-inshaallah)
- [🏛️ Repository Structure](#️-repository-structure)
- [📬 Author & Contact](#-author--contact)

---

## 📌 Repository Overview

This repository archives original algorithmic contributions designed to solve foundational computer science challenges with **extreme memory efficiency**:

1. **Zero-Allocation Execution ($O(1)$ Auxiliary Space):** Eliminating unnecessary buffer allocations in algorithms that traditionally demand $O(N)$ auxiliary heap or stack memory.
2. **Embedded & Systems Readiness:** Crafting algorithms that run safely in severely memory-constrained environments (bare-metal microcontrollers, IoT firmware, real-time operating systems).
3. **Multi-Tier Mathematical Verification:** Ensuring every design is verified through formal invariant proofs, differential cross-testing, and large-scale automated stress testing.

---

## ✨ Core Engineering Philosophy

| Principle | Traditional Approach | Our Philosophy |
| :--- | :--- | :--- |
| **Memory Footprint** | Lazy allocation of intermediate string/array buffers ($O(N)$) | **Aggressive In-Place Transformation ($O(1)$ auxiliary space)** |
| **Pass Count** | Multi-pass reductions (e.g., Reverse $\rightarrow$ Postfix $\rightarrow$ Reverse) | **Single-pass directional scanning with dual pointers** |
| **Verification** | 5–10 hand-crafted test cases | **Multi-tier automated fuzzing across 40,000+ random inputs** |
| **Portability** | Language-bound snippets | **Reference C with idiomatic ports across modern languages** |

---

## 📂 Featured Projects Catalog

### 1. 🔄 [In-Place Infix to Prefix Converter](✅%20infix%20to%20prefix/)
*A novel dual-pointer right-to-left scan that overwrites the input buffer in-place with zero auxiliary string allocation.*

- **Origin & Provenance:** Conceived and submitted as **Lab Report No. 01 (Problem 2)** in **December 2022** for Course *CSE-104: Structured Programming Lab* at the **Department of CSE, Green University of Bangladesh** (Student: Ashikur Rahman, ID: 221902131; Lecturer: Md. Abu Rumman Refat).
  - 📑 [View Original 2022 Lab Report Presentation (Google Slides)](https://docs.google.com/presentation/d/1ogiW8eGX2eApdnQU1bEeGhEWsG034DrZ7xZPR5uvhVY/edit?usp=sharing)
  - 📄 **Official Preprint (CERN/Zenodo DOI):** [10.5281/zenodo.23657544](https://doi.org/10.5281/zenodo.23657544)
- **The Breakthrough:** Traditional textbook algorithms require 3 full string passes and an extra $O(N)$ buffer (Reverse $\rightarrow$ Postfix $\rightarrow$ Reverse). This algorithm performs the complete conversion **in-place** directly inside the original buffer using a backward read/write pointer discipline.
- **Safety Proof:** Mathematically proves the invariant `read_idx <= write_idx`, guaranteeing unread data is never overwritten.
- **Languages Provided:** C (Reference), JavaScript (Node.js), Python 3, Java, C#.
- **Robustness:** Validated across **40,000 randomized expressions** across 3 independent tiers with **0% corruption and 100.00% accuracy**.
- 👉 **[Explore Project & Full Documentation &raquo;](✅%20infix%20to%20prefix/)**

---

### 2. 🌩️ [Cloud Sort](✅%20cloud%20merge%20sort/)
*An overhead single-buffer in-situ merge sort challenging standard textbook memory waste by reducing auxiliary space to $\lceil N/2 \rceil$, eliminating dynamic `malloc` overhead, saving 25% memory bus energy, and eliminating the right-hand drain loop.*

- **Origin & Provenance:** Conceived in **Spring 2023** during the *Data Structures & Algorithms* semester at the **Department of CSE, Green University of Bangladesh** (Ashikur Rahman).
  - 📄 **Official Preprint (CERN/Zenodo DOI):** [10.5281/zenodo.23665548](https://doi.org/10.5281/zenodo.23665548)
  - 📑 **Academic Paper:** [Read the full research paper (PAPER.md)](✅%20cloud%20merge%20sort/PAPER.md)
  - 📜 **The Inventor's Journey:** [Behind the scenes: Door-marker traces, in-place trials & breakthroughs](✅%20cloud%20merge%20sort/ORIGIN_AND_JOURNEY.md)
  - 🔬 **Prototype Archive:** [Explore original experimental code (`prototypes/`)](✅%20cloud%20merge%20sort/prototypes/)
- **The Breakthrough:** Standard textbooks mandate allocating $N$ auxiliary slots with complex dynamic `malloc`/`free` routines and executing 4 loops. Cloud Sort allows the caller to provide a simple overhead `cloud` buffer of size $\lceil N/2 \rceil$. The active slice `arr[l..m]` temporarily ascends to the cloud to vacate ground writing slots, while `arr[m+1..r]` remains directly on the ground in-situ.
- **Loop Economy:** Uses only **3 loops** instead of 4. The ground drain loop is completely eliminated (**Zero-Move Right Tail Property**).
- **Embedded & IoT Energy Efficiency:** Reduces SRAM write bus activity by **25.0%**, cutting dynamic power dissipation and extending battery lifespan on microcontrollers (Arduino Uno / ATmega328P). Delivers **25% faster throughput** with safe execution where standard merge sort triggers out-of-memory crashes.
- **Stability & Safety:** Strictly stable sort, mathematically proven read-before-write safety invariant ($L_t \le R_t$), and verified across **10,000 random arrays** against V8 Native TimSort with **100.0000% precision**.
- **Languages Provided:** C (Reference), JavaScript (Node.js), Python 3.
- 👉 **[Explore Project & Full Documentation &raquo;](✅%20cloud%20merge%20sort/)**

---

### 3. 🤖 [Artificial Sort](✅%20artificial%20sort/)
*A novel in-situ divide-and-conquer merge sort that achieves $O(1)$ auxiliary heap space using a concise ~35-line directional half-pass loop, dynamic artificial buffering, and split-point tail recursion.*

- **Origin & Conception:** Conceived and refined in **2024–2026** by **Ashikur Rahman** (*Department of CSE, Green University of Bangladesh*).
- **The Breakthrough:** For over half a century, in-place merging with $O(1)$ extra space required 300 to 500 lines of arcane block-tagging and key extraction (Kronrod, Huang-Langston, SymMerge). Artificial Sort demonstrates that a directional loop across just the left half ($l \le mid$) can naturally partition displaced elements into an artificial queue in the right half, terminating with a clean recursive merge at `split = rp - 1`.
- **Zero-Allocation Safety:** Demands **0 bytes of auxiliary heap memory**, eliminating Out-Of-Memory (OOM) risks that plague TimSort and standard merge sort on memory-constrained embedded microcontrollers (Arduino, STM32) and high-volume database engines.
- **Bounded Recursion Stack:** Stack depth is mathematically bounded by $\mathcal{O}(\log N)$ (measuring only 26 frames for 50,000 integers, $< 1 \text{ KB}$), with full tail-call optimization compatibility.
- **Languages Provided:** C (Reference), C++, JavaScript (Node.js), Python 3, Java.
- **Verification Rigor:** Verified across **6 independent tiers** covering powers-of-two, odd/prime lengths, extreme repetitions, adversarial alternating patterns, and large-scale fuzzing with **100.00% precision**.
- 👉 **[Explore Project & Full Documentation &raquo;](✅%20artificial%20sort/)**

---

## 🗺️ Upcoming Research & Projects Roadmap (Insha'Allah)

This repository is continuously expanding with ongoing research and original algorithmic designs:

| Project | Domain | Core Innovation / Research Goal | Status |
| :--- | :--- | :--- | :---: |
| **In-Place Infix to Prefix** | Compiler Design & Expression Parsing | Dual-pointer backward in-place conversion with $O(1)$ auxiliary string space. | 🏆 Published (DOI: 10.5281/zenodo.23657544) |
| **Cloud Sort** | Sorting Pedagogy & Embedded Optimization | Overhead-buffer in-situ merge sort with $\lceil N/2 \rceil$ space, zero-malloc simplicity, and zero-move tail. | 🏆 Published (DOI: 10.5281/zenodo.23665548) |
| **Artificial Sort** | Embedded Sorting & Memory Optimization | In-situ half-pass dual-stream merge sort with $O(1)$ auxiliary heap memory in ~35 lines. | 🏆 Complete & Verified |
| **JSON Boundary Tracker** | High-Throughput Parsing | Zero-copy stream tokenization and lexical boundary detection without AST heap overhead. | 🔬 In Design |
| **Adaptive In-Place Cache Eviction** | Operating Systems & Caching | Low-overhead pointer-indexed cache replacement for resource-constrained micro-kernels. | 💡 Planned |
| **Bounded Stack Math Evaluator** | Embedded Firmware | Fixed-depth evaluation of mathematical trees with guaranteed zero-overflow guarantees. | 💡 Planned |

---

## 🏛️ Repository Structure

```text
my-innovations/
│
├── README.md                          # Main repository overview & research catalog
├── .gitignore                         # Excludes bytecode, OS metadata & private drafts
│
├── ✅ infix to prefix/                 # Project 1: In-Place Infix to Prefix Converter
│   ├── README.md                      # Comprehensive academic & practical documentation
│   ├── infix to prefix.c              # Core reference implementation in C (memory-guarded)
│   │
│   ├── implementations/               # Idiomatic multi-language ports
│   │   ├── infix_to_prefix.js         # JavaScript (Node.js) implementation
│   │   ├── infix_to_prefix.py         # Python 3 implementation
│   │   ├── InfixToPrefix.java         # Java implementation
│   │   └── InfixToPrefix.cs           # C# / .NET implementation
│   │
│   └── tests/                         # Public test suite & validation harness
│       ├── test_vectors.json          # 27 verified golden test vectors
│       ├── test_suite.js              # Vector suite + differential random harness (JS)
│       └── test_stress.py             # Full 40,000-expression 3-layer stress harness (Python)
│
└── ✅ cloud merge sort/                # Project 2: Cloud Sort (Overhead-Buffer In-Situ)
    ├── README.md                      # Comprehensive theory, benchmarks & embedded analysis
    ├── PAPER.md                       # Formal academic research paper (peer-review format)
    ├── ORIGIN_AND_JOURNEY.md          # Behind the scenes: Door-marker traces & inventor's journey
    ├── learnCS.md                     # Zero-learning curve tutorial (English)
    ├── learnCS_Bangla.md              # জিরো লার্নিং কার্ভ বাংলা টিউটোরিয়াল
    ├── cloud_merge_sort.c             # Pure Cloud Sort in C (Reference, caller-buffer model)
    ├── standard_merge_sort.c          # Pure Standard Merge Sort in C (Canonical comparison)
    │
    ├── prototypes/                    # Precursor in-place & rotational experimental archive
    │   ├── angle_inplace_experiment.js# Early ~70-80% in-place swap experiment (angleSort)
    │   ├── c_inplace_cross_swap.c     # C-based boundary swap trial (test.c)
    │   └── queue_merge_experiment.js  # Rotational queue-merge trial (cloudMarge.js)
    │
    ├── implementations/               # Production multi-language standalone implementations
    │   ├── cloud_merge_sort.js        # Pure Cloud Sort (JavaScript)
    │   ├── standard_merge_sort.js     # Pure Standard Merge Sort (JavaScript)
    │   ├── cloud_merge_sort.py        # Pure Cloud Sort (Python 3)
    │   └── standard_merge_sort.py     # Pure Standard Merge Sort (Python 3)
    │
    └── tests/                         # Verification & empirical hardware harness
        ├── test_suite.js              # 5-layer test suite: edge-cases, 10k random & moves
        ├── test_stress.py             # 10,000-array differential test vs Python TimSort
        └── test_arduino_benchmark.py  # Arduino Uno / IoT RAM & SRAM bus energy benchmark
│
└── ✅ artificial sort/                 # Project 3: Artificial Sort (In-Situ Dual-Stream)
    ├── README.md                      # Academic theory, proofs, memory & FAQ documentation
    ├── README_Bangla.md               # সম্পূর্ণ বাংলা ডকুমেন্টেশন ও গাণিতিক বিশ্লেষণ
    ├── ORIGIN_AND_JOURNEY.md          # ক্লাউড কম্পিউটিং যুগ থেকে হোলি গ্রেইল অন্বেষণের ইতিহাস
    ├── learnAS.md                     # Zero-learning curve tutorial (English)
    ├── learnAS_Bangla.md              # জিরো লার্নিং কার্ভ বাংলা টিউটোরিয়াল
    │
    ├── implementations/               # Idiomatic multi-language implementations
    │   ├── artificial_sort.c          # Pure reference C implementation
    │   ├── artificial_sort.cpp        # Modern C++ implementation
    │   ├── artificial_sort.js         # JavaScript (Node.js) implementation
    │   ├── artificial_sort.py         # Python 3 implementation
    │   └── ArtificialSort.java        # Java implementation
    │
    └── tests/                         # Multi-tier verification & benchmarks
        ├── test_suite.js              # 6-tier stress suite across edge cases & fuzzing
        └── test_benchmark.py          # Heap memory, speed & stack depth benchmark
```

---

## 🧪 Testing & Reproduction

Anyone can independently reproduce and verify the algorithms in this repository in seconds:

### 1. In-Place Infix to Prefix Converter
```bash
cd my-innovations/"✅ infix to prefix"

# Run fast JavaScript validation (vectors + differential + invariants)
node tests/test_suite.js

# Run full 3-layer Python stress harness (40,000 expressions)
python tests/test_stress.py
```

### 2. Cloud Merge Sort
```bash
cd my-innovations/"✅ cloud merge sort"

# Run 5-layer validation suite
node tests/test_suite.js

# Run 10,000-array differential test vs V8/TimSort
python tests/test_stress.py
```

### 3. Artificial Sort
```bash
cd my-innovations/"✅ artificial sort"

# Run 6-tier comprehensive automated verification
node tests/test_suite.js

# Run O(1) heap memory vs standard merge sort benchmark
python tests/test_benchmark.py
```
```bash
cd my-innovations/"✅ cloud merge sort"

# Run 5-layer JavaScript verification (edge cases, 10,000 arrays, stability, move counters)
node tests/test_suite.js

# Run Python differential stress test (10,000 arrays vs native C-Timsort)
python -m tests.test_stress

# Run Arduino Uno & Embedded IoT RAM + Power/Energy Benchmark
python tests/test_arduino_benchmark.py
```

---

## 📬 Author & Contact

**Ashikur Rahman**  
*Computer Systems & Algorithms Researcher / Software Engineer*  
- **GitHub:** [@favouritesir](https://github.com/favouritesir)  
- **Email:** [ashikur.gub@gmail.com](mailto:ashikur.gub@gmail.com)  

---

<p align="center">
  <i>"Simplicity and extreme memory efficiency are not accidents; they are the result of disciplined mathematical design."</i>
</p>
