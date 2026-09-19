# 2026-ITCS386-Sec1-liu-qi
## BCC (Base Choice Coverage)
### BCC-1: IsValidMove()
#### 1.Testable Function
Function: isValidMove(int row,int col, String Value) 
<br> This method will check position is in the range and the value is unique in row, column and box.

#### 2. Parameters
| Parameter | Description |
|---|---|
| `row` | The row index of the Sudoku board |
| `col` | The column index of the Sudoku board |
| `value` | The Sudoku value to be checked |

#### 3. Return Value
The method returns a boolean value:
- 'true' if the move is valid
- 'false' if the move is invalid

#### 4. Input Domain Modeling 
##### Interface-based characteristic
C1: Row Position
| Partition | Description |
|---|---|
| A1: Valid position | `row` is within the Sudoku board range |
| A2: Invalid position | `row` is outside the Sudoku board range |

C2: Column Position
| Partition | Description |
|---|---|
| B1: Valid column | `col` is within the Sudoku board range |
| B2: Invalid column | `col` is outside the Sudoku board range |


##### Functionality-based Characteristic
C3: Move Conflict
| Partition | Description |
|---|---|
| C1: No conflict | The value does not already exist in the same row, column, or box. |
| C2: Conflict | The value already exists in the same row, column, or box. |

#### 5. Base Choice
The base choices are:
- C1: Row Position = A1: Valid row
- C2: Column Position = B1: Valid column
- C3: Move Conflict = C1: No conflict
Therefore, the base test is: A1, B1, C1

#### 6. BCC Test Requirements
| Test | Row Position | Column Position | Move Conflict | Expected Result |
|---|---|---|---|---|
| T1 (Base) | A1: Valid | B1: Valid | C1: No conflict | `true` |
| T2 | A2: Invalid | B1: Valid | C1: No conflict | `false` |
| T3 | A1: Valid | B2: Invalid | C1: No conflict | `false` |
| T4 | A1: Valid | B1: Valid | C2: Conflict | `false` |

T1 is the base test.

T2 changes only the Row Position characteristic from the base
choice while keeping Column Position and Move Conflict at their
base choices.

T3 changes only the Column Position characteristic from the base
choice while keeping Row Position and Move Conflict at their
base choices.

T4 changes only the Move Conflict characteristic from the base
choice while keeping Row Position and Column Position at their
base choices.

#### 7. Test Values
The test values are derived from the BCC test requirements and the existing Sudoku board used in the project
| Test | `row` | `col` | `value` | Row Position | Column Position | Move Conflict | Expected Result |
|---|---:|---:|---|---|---|---|---|
| T1 (Base) | `0` | `0` | `"1"` | Valid | Valid | No conflict | `true` |
| T2 | `-1` | `0` | `"1"` | Invalid | Valid | No conflict | `false` |
| T3 | `0` | `-1` | `"1"` | Valid | Invalid | No conflict | `false` |
| T4 | `0` | `0` | `"8"` | Valid | Valid | Conflict | `false` |

### BCC-2: IsSlotAvailable()
#### 1.Testable Function
Function: isSlotAvailable(int row, int col)
<br> This method will whether a specific slot is available for use by verifying that the position is within the board range, the slot is empty, and the slot is mutable.

#### 2. Parameters
| Parameter | Description |
|---|---|
| `row` | The row index of the Sudoku board |
| `col` | The column index of the Sudoku board |

#### 3. Return Value
The method returns a boolean value:
- `true` if the slot is available
- `false` if the slot is unavailable

#### 4. Input Domain Modeling 
##### Interface-based characteristic
C1: Row Position
| Partition | Description |
|---|---|
| A1: Valid row | `row` is within the Sudoku board range |
| A2: Invalid row | `row` is outside the Sudoku board range |

C2: Column Position
| Partition | Description |
|---|---|
| B1: Valid column | `col` is within the Sudoku board range |
| B2: Invalid column | `col` is outside the Sudoku board range |

##### Functionality-based characteristic

C3: Slot State
| Partition | Description |
|---|---|
| C1: Available slot | The slot is empty and mutable |
| C2: Unavailable slot | The slot is not empty |

#### 5. Base Choice
The base choices are:
- C1: Row Position = A1: Valid row
- C2: Column Position = B1: Valid column
- C3: Slot State = C1: Available slot
Therefore, the base test is: A1, B1, C1

T1 is the base test.

T2 changes only the Row Position characteristic from the base choice while keeping Column Position and Slot State at their base choices.

T3 changes only the Column Position characteristic from the base choice while keeping Row Position and Slot State at their base choices.

T4 changes only the Slot State characteristic from the base choice while keeping Row Position and Column Position at their base choices.

#### 7. Test Values
The test values are derived from the BCC test requirements and the existing Sudoku board in the project.
| Test | `row` | `col` | Slot State | Expected Result |
|---|---:|---:|---|---|
| T1 (Base) | `0` | `0` | Available | `true` |
| T2 | `-1` | `0` | Available | `false` |
| T3 | `0` | `-1` | Available | `false` |
| T4 | `0` | `2` | Unavailable | `false` |
