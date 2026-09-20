# 2026-ITCS386-Sec1-liu-qi

## PWC (Pair-Wise Coverage)

### PWC-1: isSlotAvailable()

#### 1. Testable Function
Function: isSlotAvailable(int row, int col)
<br> This method checks whether a slot can be used, by verifying that the position is within the board range, the slot is empty, and the slot is mutable.

#### 2. Parameters
| Parameter | Description |
|---|---|
| `row` | The row index of the Sudoku board |
| `col` | The column index of the Sudoku board |

#### 3. Return Value and Exceptional Behaviour
The method returns a boolean value:
- `true` if the slot is available (in range, empty, and mutable)
- `false` if the slot is unavailable

Exceptional behaviour: The method does not throw any exception. The condition uses short-circuit evaluation (`inRange(row,col) && board[row][col].equals("") && isSlotMutable(row,col)`). When the position is out of range, the first condition is `false` and the board array is never accessed, so no `ArrayIndexOutOfBoundsException` occurs for positions such as `(-1, 0)`.

#### 4. Input Domain Modeling
##### Interface-based characteristic
C1: Position
| Partition | Description |
|---|---|
| A1: In range | Both `row` and `col` are within the board range |
| A2: Out of range | `row` or `col` is outside the board range |

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
Pair-Wise Coverage requires every pair of blocks from two different characteristics to appear together in at least one test. This method has three characteristics of two blocks each, so All Combinations (ACoC) would need 2 x 2 x 2 = 8 tests. By the PWC formula the minimum is the product of the two largest characteristics, 2 x 2 = 4, and four tests are enough to cover every pair here.

#### 6. PWC Test Requirements
| Test | Position | Cell Content | Mutability | Expected Result |
|---|---|---|---|---|
| T1 | A1: In range | B1: Empty | C1: Mutable | `true` |
| T2 | A1: In range | B2: Has value | C2: Immutable | `false` |
| T3 | A2: Out of range | B1: Empty | C2: Immutable | `false` |
| T4 | A2: Out of range | B2: Has value | C1: Mutable | `false` |

Pair coverage check:
- Position x Cell Content: (In range, Empty), (In range, Has value), (Out of range, Empty), (Out of range, Has value). All covered.
- Position x Mutability: (In range, Mutable), (In range, Immutable), (Out of range, Immutable), (Out of range, Mutable). All covered.
- Cell Content x Mutability: (Empty, Mutable), (Has value, Immutable), (Empty, Immutable), (Has value, Mutable). All covered.

All required pairs appear at least once, so the four tests satisfy Pair-Wise Coverage. In T3 and T4 the Cell Content and Mutability blocks do not affect the result because the out-of-range position short-circuits the evaluation. They are still assigned to complete the required pairs.

#### 7. Test Values
The fixture uses a 9x9 board where every slot starts empty (`""`) and mutable. For the "has value" and "immutable" case, the slot at `(0,1)` is set to `"5"` and locked.
| Test | `row` | `col` | Position | Cell Content | Mutability | Expected Result |
|---|---:|---:|---|---|---|---|
| T1 | `0` | `0` | In range | Empty | Mutable | `true` |
| T2 | `0` | `1` | In range | Has value | Immutable | `false` |
| T3 | `-1` | `0` | Out of range | Empty | Immutable | `false` |
| T4 | `0` | `-1` | Out of range | Has value | Mutable | `false` |

### PWC-2: makeMove()

#### 1. Testable Function
Function: makeMove(int row, int col, String value, boolean isMutable)
<br> This method places a value into a slot only when the value is valid, the move does not conflict with the same row, column, or box, and the slot is currently mutable. Otherwise the board is left unchanged.

#### 2. Parameters
| Parameter | Description |
|---|---|
| `row` | The row index of the Sudoku board |
| `col` | The column index of the Sudoku board |
| `value` | The Sudoku value to be placed |
| `isMutable` | The mutability flag to set if the move is applied |

#### 3. Return Value and Exceptional Behaviour
The method returns `void`. Its effect is observed through the board state: after the call the target slot either holds the new value (accepted) or stays unchanged (rejected). The effect is verified with `getValue(row, col)`.

Exceptional behaviour: The method does not throw any exception for the selected cases. The guard uses short-circuit evaluation (`isValidValue(value) && isValidMove(row,col,value) && isSlotMutable(row,col)`). An invalid value fails the first condition, and an out-of-range position makes `isValidMove` return `false` at its `inRange` check, so `isSlotMutable` (which has no bounds check) is never reached and no `ArrayIndexOutOfBoundsException` occurs.

#### 4. Input Domain Modeling
##### Interface-based characteristics
C1: Value Validity
| Partition | Description |
|---|---|
| V: Valid value | The value is one of the board's valid values |
| I: Invalid value | The value is not a valid value |

C2: Position
| Partition | Description |
|---|---|
| R: In range | Both `row` and `col` are within the board range |
| O: Out of range | `row` or `col` is outside the board range |

##### Functionality-based characteristics
C3: Move Conflict
| Partition | Description |
|---|---|
| n: No conflict | The value does not exist in the same row, column, or box |
| c: Conflict | The value already exists in the same row, column, or box |

C4: Mutability
| Partition | Description |
|---|---|
| m: Mutable | The slot is editable |
| k: Locked | The slot is immutable |

#### 5. Combination Strategy (Pair-Wise Coverage)
Pair-Wise Coverage requires every pair of blocks from two different characteristics to appear together in at least one test. This method has four characteristics of two blocks each, so All Combinations (ACoC) would need 2 x 2 x 2 x 2 = 16 tests. By the PWC formula the minimum is 2 x 2 = 4, but four tests are not enough to cover all pairs across four characteristics. Five tests are sufficient.

#### 6. PWC Test Requirements
| Test | Value | Position | Conflict | Mutability | Expected Result |
|---|---|---|---|---|---|
| T1 | V: Valid | R: In range | n: No conflict | m: Mutable | Accepted |
| T2 | V: Valid | R: In range | c: Conflict | k: Locked | Rejected |
| T3 | V: Valid | O: Out of range | n: No conflict | k: Locked | Rejected |
| T4 | I: Invalid | R: In range | n: No conflict | k: Locked | Rejected |
| T5 | I: Invalid | O: Out of range | c: Conflict | m: Mutable | Rejected |

Pair coverage check:
- Value x Position: VR (T1), VO (T3), IR (T4), IO (T5). All covered.
- Value x Conflict: Vn (T1), Vc (T2), In (T4), Ic (T5). All covered.
- Value x Mutability: Vm (T1), Vk (T2), Ik (T4), Im (T5). All covered.
- Position x Conflict: Rn (T1), Rc (T2), On (T3), Oc (T5). All covered.
- Position x Mutability: Rm (T1), Rk (T2), Ok (T3), Om (T5). All covered.
- Conflict x Mutability: nm (T1), ck (T2), nk (T3), cm (T5). All covered.

All 24 required pairs appear at least once, so these five tests satisfy Pair-Wise Coverage, compared with 16 for All Combinations. For out-of-range or invalid-value cases, the conflict and mutability blocks do not affect the result; they are still assigned to complete the required pairs.

#### 7. Test Values
The fixture uses a 9x9 board that starts empty and mutable. Specific cells are adjusted per test to create the required conflict or locked state. Each test uses a fresh puzzle so an applied move in one test does not affect another. The witness cell `(0,0)` is checked to confirm no unintended change for the rejected cases.
| Test | `row` | `col` | `value` | Setup | Expected `getValue(0,0)` |
|---|---:|---:|---|---|---|
| T1 | `0` | `0` | `"5"` | empty, mutable | `"5"` |
| T2 | `0` | `0` | `"5"` | `(0,4)="5"` conflict, `(0,0)` locked | `""` |
| T3 | `-1` | `0` | `"5"` | `(0,0)` locked | `""` |
| T4 | `0` | `0` | `"X"` | `(0,0)` locked | `""` |
| T5 | `-1` | `-1` | `"X"` | `(0,4)="5"` conflict, mutable | `""` |
