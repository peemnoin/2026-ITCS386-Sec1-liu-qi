# 2026-ITCS386-Sec1-liu-qi
## BCC (Base Choice Coverage)
### BCC-1: isValidMove()
#### 1. Testable Function
Function: isValidMove(int row, int col, String value)
<br> This method checks whether the position is within the board range and the value is unique in the same row, column, and box.
#### 2. Parameters
| Parameter | Description |
|---|---|
| `row` | The row index of the Sudoku board |
| `col` | The column index of the Sudoku board |
| `value` | The Sudoku value to be checked |

#### 3. Return Value
The method returns a boolean value:
- `true` if the move is valid
- `false` if the move is invalid

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

#### 6.  BCC Test Cases
| Test | Row Position | Column Position | Move Conflict | Expected Result |
|---|---|---|---|---|
| T1 (Base) | A1: Valid | B1: Valid | C1: No conflict | `true` |
| T2 | A2: Invalid | B1: Valid | C1: No conflict | `false` |
| T3 | A1: Valid | B2: Invalid | C1: No conflict | `false` |
| T4 | A1: Valid | B1: Valid | C2: Conflict | `false` |

- **T1** is the base test using all base choices.
- **T2** changes only the Row Position from valid to invalid.
- **T3** changes only the Column Position from valid to invalid.
- **T4** changes only the Move Conflict from no conflict to conflict.

#### 7. Test Values
The test values are derived from the BCC test requirements and the existing Sudoku board used in the project.
| Test | `row` | `col` | `value` | Row Position | Column Position | Move Conflict | Expected Result |
|---|---:|---:|---|---|---|---|---|
| T1 (Base) | `0` | `0` | `"1"` | Valid | Valid | No conflict | `true` |
| T2 | `-1` | `0` | `"1"` | Invalid | Valid | No conflict | `false` |
| T3 | `0` | `-1` | `"1"` | Valid | Invalid | No conflict | `false` |
| T4 | `0` | `0` | `"8"` | Valid | Valid | Conflict | `false` |

T1: Position (0,0) is within the board range, and value "1" does not conflict with any existing value in the same row, column, or box.
T2: row = -1 represents an invalid row position, causing the method to return false.
T3: col = -1 represents an invalid column position, causing the method to return false.
T4: Value "8" already exists in the same row at position (0,2), creating a move conflict. Therefore, the method returns false.

### BCC-2: isSlotAvailable()

#### 1. Testable Function
Function: isSlotAvailable(int row, int col)
<br> This method checks whether a specific slot is available for use by verifying that the position is within the board range, the slot is empty, and the slot is mutable.

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
##### Interface-based characteristics
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
| C2: Unavailable slot |The slot is either not empty or not mutable |

#### 5. Base Choice
The base choices are:
- C1: Row Position = A1: Valid row
- C2: Column Position = B1: Valid column
- C3: Slot State = C1: Available slot
Therefore, the base test is: A1, B1, C1

#### 6. BCC Test Cases
| Test | Row Position | Column Position | Slot State | Expected Result |
|---|---|---|---|---|
| T1 (Base) | A1: Valid | B1: Valid | C1: Available | `true` |
| T2 | A2: Invalid | B1: Valid | C1: Available | `false` |
| T3 | A1: Valid | B2: Invalid | C1: Available | `false` |
| T4 | A1: Valid | B1: Valid | C2: Unavailable | `false` |

- **T1** is the base test using all base choices.
- **T2** changes only the Row Position from valid to invalid.
- **T3** changes only the Column Position from valid to invalid.
- **T4** changes only the Slot State from available to unavailable.

#### 7. Test Values
The test values are derived from the BCC test requirements and the behavior of the `SudokuPuzzle` class. The test fixture uses a 9×9 board where the slots are initialized as empty (`""`) and mutable. For T4, the slot at `(0,2)` is set to `"8"` to represent an unavailable slot.
| Test | `row` | `col` | Slot State | Expected Result |
|---|---:|---:|---|---|
| T1 (Base) | `0` | `0` | Available | `true` |
| T2 | `-1` | `0` | Available | `false` |
| T3 | `0` | `-1` | Available | `false` |
| T4 | `0` | `2` | Unavailable | `false` |

T1: Position (0,0) is within the board range, and the slot is empty and mutable, so it is available.
T2: row = -1 represents an invalid row position, causing the method to return false.
T3: col = -1 represents an invalid column position, causing the method to return false.
T4: The slot at (0,2) contains "8", so the slot is not empty and is therefore unavailable. The method returns false.

#### 8. Test Execution Results
<img width="843" height="761" alt="BCC_Test" src="https://github.com/user-attachments/assets/a333c4aa-7456-4afc-9396-d0fa798175e2" />
