## ECC (Each Choice Coverage)

### ECC-1: isSlotMutable()

#### 1. Testable Function
Function: isSlotMutable(int row, int col)
<br> This method returns whether the slot at the given position is currently editable, based solely on the internal `mutable` flag for that cell.

#### 2. Parameters
| Parameter | Description |
|---|---|
| `row` | The row index of the Sudoku board |
| `col` | The column index of the Sudoku board |

#### 3. Return Value and Exceptional Behaviour
The method returns a boolean value:
- `true` if the slot at `(row, col)` is mutable
- `false` if the slot at `(row, col)` is locked

Exceptional behaviour: Unlike `isSlotAvailable()`, this method does **not** call `inRange()` before accessing the array — it directly evaluates `this.mutable[row][col]`. Passing a `row` or `col` outside the board's bounds will therefore throw an uncaught `ArrayIndexOutOfBoundsException` instead of returning a boolean. This test suite focuses on the method's normal (in-range) contract; boundary/out-of-range behaviour for array access is covered separately in the ACoC/BCC/MBCC test suites written for other methods.

#### 4. Input Domain Modeling
##### Interface-based characteristic
C1: Column Position
| Partition | Description |
|---|---|
| A1: Boundary column | `col` is the first column of the board (`col = 0`) |
| A2: Non-boundary column | `col` is not the first column (`col = 1`) |

##### Functionality-based characteristic
C2: Slot Mutability State
| Partition | Description |
|---|---|
| B1: Mutable | The slot's `mutable` flag is `true` |
| B2: Immutable | The slot's `mutable` flag is `false` |

#### 5. Combination Strategy (Each Choice Coverage)
Each Choice Coverage requires that every block of every characteristic be exercised by at least one test case, using the minimum number of tests possible. Since both characteristics have exactly two blocks, the two blocks of C1 and the two blocks of C2 can each be paired once, so only **2 test cases** are needed to cover all four blocks — unlike All Combinations, which would require 2×2 = 4 test cases.

#### 6. ECC Test Requirements
| Test | Column Position | Mutability State | Expected Result |
|---|---|---|---|
| T1 | A1: Boundary column | B1: Mutable | `true` |
| T2 | A2: Non-boundary column | B2: Immutable | `false` |

Each-choice check:
- C1 blocks covered: A1 (T1), A2 (T2) — both appear.
- C2 blocks covered: B1 (T1), B2 (T2) — both appear.

All blocks from both characteristics appear at least once, so the two test cases satisfy Each Choice Coverage.

#### 7. Test Values
The test fixture (`SudokuPuzzleForTesting`) is a 9×9 board where slot `(0,0)` is set to value `"5"` and left mutable, and slot `(0,1)` is set to value `"3"` and locked (`mutable = false`).
| Test | `row` | `col` | Column Position | Mutability State | Expected Result |
|---|---:|---:|---|---|---|
| T1 | `0` | `0` | Boundary column | Mutable | `true` |
| T2 | `0` | `1` | Non-boundary column | Immutable | `false` |

### ECC-2: makeSlotEmpty()

#### 1. Testable Function
Function: makeSlotEmpty(int row, int col)
<br> This method clears the value at the given position by setting the corresponding board slot to an empty string, regardless of what value was previously stored there.

#### 2. Parameters
| Parameter | Description |
|---|---|
| `row` | The row index of the Sudoku board |
| `col` | The column index of the Sudoku board |

#### 3. Return Value and Exceptional Behaviour
This method has a `void` return type; it does not return a value. Its effect is observed indirectly through `getValue(row, col)` after the call.

Exceptional behaviour: Like `isSlotMutable()`, this method does not call `inRange()` before writing to the array — it directly assigns `this.board[row][col] = ""`. Passing a `row` or `col` outside the board's bounds will throw an uncaught `ArrayIndexOutOfBoundsException`. This test suite verifies the method's normal (in-range) behaviour for slots in different prior states.

#### 4. Input Domain Modeling
##### Interface-based characteristic
C1: Column Position
| Partition | Description |
|---|---|
| A1: Boundary column | `col` is the first column of the board (`col = 0`) |
| A2: Non-boundary column | `col` is a later column (`col = 2`) |

##### Functionality-based characteristic
C2: Prior Cell Content
| Partition | Description |
|---|---|
| B1: Has value | The slot already contains a non-empty value before clearing |
| B2: Already empty | The slot is already an empty string `""` before clearing |

#### 5. Combination Strategy (Each Choice Coverage)
As with ECC-1, both characteristics have two blocks each, so pairing one block from C1 with one block from C2 in each test covers all four blocks in the minimum of **2 test cases**.

#### 6. ECC Test Requirements
| Test | Column Position | Prior Cell Content | Expected Result (after clearing) |
|---|---|---|---|
| T1 | A1: Boundary column | B1: Has value | `""` |
| T2 | A2: Non-boundary column | B2: Already empty | `""` |

Each-choice check:
- C1 blocks covered: A1 (T1), A2 (T2) — both appear.
- C2 blocks covered: B1 (T1), B2 (T2) — both appear.

All blocks from both characteristics appear at least once, so the two test cases satisfy Each Choice Coverage. T2 additionally demonstrates that the method is idempotent: clearing an already-empty slot still leaves it empty.

#### 7. Test Values
Using the same `SudokuPuzzleForTesting` fixture: slot `(0,0)` holds value `"5"` (has value) before clearing; slot `(0,2)` is left at its default value `""` (already empty) and is not explicitly overridden by the fixture.
| Test | `row` | `col` | Column Position | Prior Cell Content | Expected Result |
|---|---:|---:|---|---|---|
| T1 | `0` | `0` | Boundary column | Has value | `""` |
| T2 | `0` | `2` | Non-boundary column | Already empty | `""` |
