# 2026-ITCS386-Sec1-liu-qi

## PWC (Pair-Wise Coverage)

### PWC-1: isSlotAvailable()

#### 1. Testable Function
Function: isSlotAvailable(int row, int col)
<br> This method checks whether a specific slot is available for use by verifying that the position is within the board range, the slot is empty, and the slot is mutable.

#### 2. Parameters
| Parameter | Description |
|---|---|
| `row` | The row index of the Sudoku board |
| `col` | The column index of the Sudoku board |

#### 3. Return Value and Exceptional Behaviour
The method returns a boolean value:
- `true` if the slot is available (in range, empty, and mutable)
- `false` if the slot is unavailable

Exceptional behaviour: The method does not throw any exception. Because the condition uses short-circuit evaluation (`inRange(row,col) && board[row][col].equals("") && isSlotMutable(row,col)`), when the position is out of range the first condition returns `false` and the board array is never accessed. This prevents an `ArrayIndexOutOfBoundsException` from occurring for out-of-range positions such as `(-1, 0)`.

#### 4. Input Domain Modeling
##### Interface-based characteristic
C1: Position
| Partition | Description |
|---|---|
| A1: In range | Both `row` and `col` are within the Sudoku board range |
| A2: Out of range | `row` or `col` is outside the Sudoku board range |

##### Functionality-based characteristics
C2: Cell Content
| Partition | Description |
|---|---|
| B1: Empty | The slot value is an empty string `""` |
| B2: Has value | The slot already contains a value |

C3: Mutability
| Partition | Description |
|---|---|
| C1: Mutable | The slot is editable (`mutable = true`) |
| C2: Immutable | The slot is locked (`mutable = false`) |

#### 5. Combination Strategy (Pair-Wise Coverage)
Pair-Wise Coverage requires that every pair of blocks from different characteristics appears together in at least one test case. With three characteristics of two blocks each, All Combinations (ACoC) would need 2×2×2 = 8 test cases, but PWC covers every pair using only 4 test cases.

#### 6. PWC Test Requirements
| Test | Position | Cell Content | Mutability | Expected Result |
|---|---|---|---|---|
| T1 | A1: In range | B1: Empty | C1: Mutable | `true` |
| T2 | A1: In range | B2: Has value | C2: Immutable | `false` |
| T3 | A2: Out of range | B1: Empty | C2: Immutable | `false` |
| T4 | A2: Out of range | B2: Has value | C1: Mutable | `false` |

Pair coverage check:
- Position × Cell Content: (In range, Empty), (In range, Has value), (Out of range, Empty), (Out of range, Has value) — all covered.
- Position × Mutability: (In range, Mutable), (In range, Immutable), (Out of range, Immutable), (Out of range, Mutable) — all covered.
- Cell Content × Mutability: (Empty, Mutable), (Has value, Immutable), (Empty, Immutable), (Has value, Mutable) — all covered.

All required pairs appear at least once, so the four test cases satisfy Pair-Wise Coverage. Note that in T3 and T4 the Cell Content and Mutability blocks have no effect on the result because the out-of-range position short-circuits the evaluation. They are still assigned to complete the required pairs.

#### 7. Test Values
The test fixture uses a 9×9 board where all slots are initialized as empty (`""`) and mutable. For the "has value" and "immutable" case, the slot at `(0,1)` is set to `"5"` and locked (`mutable = false`).
| Test | `row` | `col` | Position | Cell Content | Mutability | Expected Result |
|---|---:|---:|---|---|---|---|
| T1 | `0` | `0` | In range | Empty | Mutable | `true` |
| T2 | `0` | `1` | In range | Has value | Immutable | `false` |
| T3 | `-1` | `0` | Out of range | Empty | Immutable | `false` |
| T4 | `0` | `-1` | Out of range | Has value | Mutable | `false` |

### PWC-2: boardFull()

#### 1. Testable Function
Function: boardFull()
<br> This method checks whether every slot on the board contains a value, returning `true` only when no empty slot remains.

#### 2. Parameters
This method takes no parameters. Its input is the internal board state, which is determined by the board size given to the constructor and by the values filled into the board.

#### 3. Return Value and Exceptional Behaviour
The method returns a boolean value:
- `true` if every slot contains a value
- `false` if at least one slot is empty

Exceptional behaviour: The method does not throw any exception. It iterates using the ROWS and COLUMNS values fixed at construction time, so it always stays within the board bounds.

#### 4. Input Domain Modeling
##### Interface-based characteristic
C1: Board Size
| Partition | Description |
|---|---|
| A1: 9×9 board | A standard 9×9 Sudoku board |
| A2: 12×12 board | A larger 12×12 Sudoku board |

##### Functionality-based characteristic
C2: Fill State
| Partition | Description |
|---|---|
| B1: Full | Every slot on the board contains a value |
| B2: Not full | At least one slot is still empty |

#### 5. Combination Strategy (Pair-Wise Coverage)
Pair-Wise Coverage requires every pair of blocks from different characteristics to appear together at least once. Because this method has only two characteristics, there is a single pair (Board Size × Fill State) to cover, and that pair has 2×2 = 4 combinations. In this case Pair-Wise Coverage is equivalent to All Combinations, so all four combinations are tested.

#### 6. PWC Test Requirements
| Test | Board Size | Fill State | Expected Result |
|---|---|---|---|
| T1 | A1: 9×9 | B1: Full | `true` |
| T2 | A1: 9×9 | B2: Not full | `false` |
| T3 | A2: 12×12 | B1: Full | `true` |
| T4 | A2: 12×12 | B2: Not full | `false` |

#### 7. Test Values
For each test a board of the given size is created. For the "full" case every slot is filled with `"1"`. For the "not full" case the slots are left empty except `(0,0)`, which is set to `"1"` to show a partially filled board.
| Test | Board Size | Fill State | Expected Result |
|---|---|---|---|
| T1 | 9×9 | Full | `true` |
| T2 | 9×9 | Not full | `false` |
| T3 | 12×12 | Full | `true` |
| T4 | 12×12 | Not full | `false` |
