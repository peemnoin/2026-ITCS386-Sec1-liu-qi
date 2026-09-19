# 2026-ITCS386-Sec1-liu-qi
## BCC (Base Choice Coverage)
### BCC-1: IsValidMove()
#### 1.Testable Function
Function: isValidMove(int row,int col, String Value) 
<br> This method will check position is in the range and the value is unique in row, column and box.
#### 2. Parameters
| Parameter | Description |
|---|---|
| `row` | The row index of the Sudoku board. |
| `col` | The column index of the Sudoku board. |
| `value` | The Sudoku value to be checked. |

#### 3. Return Value
The method returns a boolean value:
- 'true' if the move is valid
- 'false' if the move is invalid

#### 4. Input Domain Modeling 
##### Interface-based characteristic
C1: Board Position
| Partition | Description |
|---|---|
| P1: Valid position | `row` and `col` are within the Sudoku board range. |
| P2: Invalid position | `row` or `col` is outside the Sudoku board range. |

##### Functionality-based Characteristic
C2: Move Conflict
| Partition | Description |
|---|---|
| P1: No conflict | The value does not already exist in the same row, column, or box. |
| P2: Conflict | The value already exists in the same row, column, or box. |

#### 5. Base Choice

The base choices are:
- C1: Board Position = Valid position
- C2: Move Conflict = No conflict
Therefore, the base test is valid position and no conflict

#### 6. BCC Test Requirements

| Test | Board Position | Move Conflict | Expected Result |
|---|---|---|---|
| T1 (Base) | Valid | No conflict | `true` |
| T2 | Invalid | No conflict | `false` |
| T3 | Valid | Conflict | `false` |

T1 is the base test.

T2 changes only the Board Position characteristic from the base
choice while keeping Move Conflict as No conflict.

T3 changes only the Move Conflict characteristic from the base
choice while keeping Board Position as Valid.

#### 7. Test Values

