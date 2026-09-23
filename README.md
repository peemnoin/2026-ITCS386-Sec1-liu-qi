# 2026-ITCS386-Sec1-liu-qi

## Multiple Base Choice Coverage (MBCC)

### MBCC-1: makeMove()

#### 1. Testable Function

* **Function:** `makeMove(int row, int col, String value, boolean isMutable)`
* **Description:** Performs a move on the board by assigning `value` and setting the target cell's mutability flag to `isMutable` if valid (valid digit, target currently editable, and no row/column/box conflict). If invalid, the board state remains unchanged.

#### 2. Parameters

| Parameter | Description |
| :--- | :--- |
| `row` | The row index of the target cell |
| `col` | The column index of the target cell |
| `value` | The proposed Sudoku value to store |
| `isMutable` | Requested mutability flag after an accepted move |

#### 3. Return Value

* **Return Type:** `void`
* **Observation:** Verified via state assertions on the board array and mutability matrix after execution.

#### 4. Input Domain Modeling

#### Interface-based Characteristics

| Characteristic | Partition ID | Partition Description | Test Value / Condition |
| :--- | :--- | :--- | :--- |
| **C1: Row Position** | A1 | Interior row | `row = 4` |
| | A2 | First row | `row = 0` |
| | A3 | Last row | `row = 8` |
| **C2: Column Position** | B1 | Interior column | `col = 4` |
| | B2 | First column | `col = 0` |
| | B3 | Last column | `col = 8` |
| **C3: Input Value Category** | C1 | Allowed digit | `"5"` |
| | C2 | Unsupported string | `"X"` |
| | C3 | Empty string | `""` |
| | C4 | Null reference | `null` |
| **C7: Requested Mutability** | G1 | Mutable | `true` |
| | G2 | Locked | `false` |


#### Functionality-based Characteristics

| Characteristic | Partition ID | Partition Description | Test Value / Condition |
| :--- | :--- | :--- | :--- |
| **C4: Move Conflict** | D1 | No conflict | `NONE` |
| | D2 | Row conflict | `ROW` |
| | D3 | Column conflict | `COLUMN` |
| | D4 | Box conflict | `BOX` |
| | D5 | Multiple conflicts | `MULTIPLE` |
| **C5: Target Current Mutability** | E1 | Currently editable | `true` |
| | E2 | Currently locked | `false` |
| **C6: Existing Target Content** | F1 | Empty cell | `""` |
| | F2 | Different allowed digit | `"2"` |

#### 5. Base Choice

Two base choices ($M = 2$) are selected to cover both post-move mutability states (`isMutable = true` and `isMutable = false`) under valid conditions:

* **Base Choice A (Editable):** `(row=4, col=4, value="5", conflict=NONE, currentMutable=true, existing="", requestedMutable=true)` $\rightarrow$ **(A1, B1, C1, D1, E1, F1, G1)**
* **Base Choice B (Locked):** `(row=4, col=4, value="5", conflict=NONE, currentMutable=true, existing="", requestedMutable=false)` $\rightarrow$ **(A1, B1, C1, D1, E1, F1, G2)**

#### 6. MBCC Test Cases

| Test | Base Origin | Varied Characteristic | Tuple (row, col, value, conflict, currentMut, existVal, reqMut) | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **MM01** | Base A | Base Choice A | `(4, 4, "5", NONE, true, "", true)` | `ACCEPT`: target = `"5"`, mutable = `true` |
| **MM02** | Base A | C1 $\rightarrow$ A2 (Row 0) | `(0, 4, "5", NONE, true, "", true)` | `ACCEPT`: target = `"5"`, mutable = `true` |
| **MM03** | Base A | C1 $\rightarrow$ A3 (Row 8) | `(8, 4, "5", NONE, true, "", true)` | `ACCEPT`: target = `"5"`, mutable = `true` |
| **MM04** | Base A | C2 $\rightarrow$ B2 (Col 0) | `(4, 0, "5", NONE, true, "", true)` | `ACCEPT`: target = `"5"`, mutable = `true` |
| **MM05** | Base A | C2 $\rightarrow$ B3 (Col 8) | `(4, 8, "5", NONE, true, "", true)` | `ACCEPT`: target = `"5"`, mutable = `true` |
| **MM06** | Base A | C3 $\rightarrow$ C2 (Value "X") | `(4, 4, "X", NONE, true, "", true)` | `REJECT`: state unchanged |
| **MM07** | Base A | C3 $\rightarrow$ C3 (Value "") | `(4, 4, "", NONE, true, "", true)` | `REJECT`: state unchanged |
| **MM08** | Base A | C3 $\rightarrow$ C4 (Value null) | `(4, 4, null, NONE, true, "", true)` | `REJECT`: state unchanged |
| **MM09** | Base A | C4 $\rightarrow$ D2 (ROW conflict) | `(4, 4, "5", ROW, true, "", true)` | `REJECT`: state unchanged |
| **MM10** | Base A | C4 $\rightarrow$ D3 (COL conflict) | `(4, 4, "5", COLUMN, true, "", true)` | `REJECT`: state unchanged |
| **MM11** | Base A | C4 $\rightarrow$ D4 (BOX conflict) | `(4, 4, "5", BOX, true, "", true)` | `REJECT`: state unchanged |
| **MM12** | Base A | C4 $\rightarrow$ D5 (MULTIPLE) | `(4, 4, "5", MULTIPLE, true, "", true)` | `REJECT`: state unchanged |
| **MM13** | Base A | C5 $\rightarrow$ E2 (currentMut false) | `(4, 4, "5", NONE, false, "", true)` | `REJECT`: state unchanged |
| **MM14** | Base A | C6 $\rightarrow$ F2 (existVal "2") | `(4, 4, "5", NONE, true, "2", true)` | `ACCEPT`: target = `"5"`, mutable = `true` |
| **MM15** | Base B | Base Choice B | `(4, 4, "5", NONE, true, "", false)` | `ACCEPT`: target = `"5"`, mutable = `false` |
| **MM16** | Base B | C1 $\rightarrow$ A2 (Row 0) | `(0, 4, "5", NONE, true, "", false)` | `ACCEPT`: target = `"5"`, mutable = `false` |
| **MM17** | Base B | C1 $\rightarrow$ A3 (Row 8) | `(8, 4, "5", NONE, true, "", false)` | `ACCEPT`: target = `"5"`, mutable = `false` |
| **MM18** | Base B | C2 $\rightarrow$ B2 (Col 0) | `(4, 0, "5", NONE, true, "", false)` | `ACCEPT`: target = `"5"`, mutable = `false` |
| **MM19** | Base B | C2 $\rightarrow$ B3 (Col 8) | `(4, 8, "5", NONE, true, "", false)` | `ACCEPT`: target = `"5"`, mutable = `false` |
| **MM20** | Base B | C3 $\rightarrow$ C2 (Value "X") | `(4, 4, "X", NONE, true, "", false)` | `REJECT`: state unchanged |
| **MM21** | Base B | C3 $\rightarrow$ C3 (Value "") | `(4, 4, "", NONE, true, "", false)` | `REJECT`: state unchanged |
| **MM22** | Base B | C3 $\rightarrow$ C4 (Value null) | `(4, 4, null, NONE, true, "", false)` | `REJECT`: state unchanged |
| **MM23** | Base B | C4 $\rightarrow$ D2 (ROW conflict) | `(4, 4, "5", ROW, true, "", false)` | `REJECT`: state unchanged |
| **MM24** | Base B | C4 $\rightarrow$ D3 (COL conflict) | `(4, 4, "5", COLUMN, true, "", false)` | `REJECT`: state unchanged |
| **MM25** | Base B | C4 $\rightarrow$ D4 (BOX conflict) | `(4, 4, "5", BOX, true, "", false)` | `REJECT`: state unchanged |
| **MM26** | Base B | C4 $\rightarrow$ D5 (MULTIPLE) | `(4, 4, "5", MULTIPLE, true, "", false)` | `REJECT`: state unchanged |
| **MM27** | Base B | C5 $\rightarrow$ E2 (currentMut false) | `(4, 4, "5", NONE, false, "", false)` | `REJECT`: state unchanged |
| **MM28** | Base B | C6 $\rightarrow$ F2 (existVal "2") | `(4, 4, "5", NONE, true, "2", false)` | `ACCEPT`: target = `"5"`, mutable = `false` |

#### 7. Test Values

* **MM01–MM05 & MM15–MM19:** Test spatial validity across interior and boundary locations (Rows 0/8, Columns 0/8).
* **MM06–MM08 & MM20–MM22:** Test input value validation by passing unsupported string `"X"`, empty string `""`, or `null`.
* **MM09–MM12 & MM23–MM26:** Test conflict checking by pre-filling conflicting values in the target row, column, box, or multiple regions simultaneously.
* **MM13 & MM27:** Test target current mutability by setting `mutable[4][4] = false` prior to making the move.
* **MM14 & MM28:** Test replacement functionality on an editable cell containing an existing digit `"2"`.


### MBCC-2: boardFull()

#### 1. Testable Function

* **Function:** `boardFull()`
* **Description:** Checks whether every cell on the Sudoku board is filled with a non-empty string.

#### 2. Parameters

* **Parameters:** None (queries internal board state).

#### 3. Return Value

The method returns a boolean value:
* `true` if all cells contain non-empty strings.
* `false` if at least one cell contains an empty string (`""`).

#### 4. Input Domain Modeling

#### Functionality-based Characteristics

| Characteristic | Partition ID | Partition Description | Test Value / Condition |
| :--- | :--- | :--- | :--- |
| **C1: Board Completeness** | A1 | Completely Full | 100% of cells filled |
| | A2 | Almost Full | Boundary state; exactly 1 cell empty |
| | A3 | Partially Filled | Multiple cells empty |
| | A4 | Completely Empty | All cells empty |


#### Interface-based Characteristics

| Characteristic | Partition ID | Partition Description | Test Value / Condition |
| :--- | :--- | :--- | :--- |
| **C2: Board Dimension** | B1 | Standard board | 9x9 board |
| | B2 | Alternative board | 6x6 board |

#### 5. Base Choice

Two base choices ($M = 2$) are selected:

* **Base Choice 1:** $[A1, B1]$ $\rightarrow$ Completely Full 9x9 board
* **Base Choice 2:** $[A2, B1]$ $\rightarrow$ Almost Full 9x9 board (Boundary condition: cell `[8][8]` empty)

#### 6. MBCC Test Cases

| Test | Base Origin | Board Completeness | Board Dimension | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **BF01** | Base 1 | A1: Completely Full (81/81) | B1: 9x9 | `true` |
| **BF02** | Base 1 | A1: Completely Full (36/36) | B2: 6x6 | `true` |
| **BF03** | Base 2 | A2: Almost Full (80/81) | B1: 9x9 | `false` |
| **BF04** | Base 2 | A2: Almost Full (35/36) | B2: 6x6 | `false` |
| **BF05** | Base 2 | A3: Partially Filled | B1: 9x9 | `false` |
| **BF06** | Base 2 | A4: Completely Empty | B1: 9x9 | `false` |

#### 7. Test Values

* **BF01:** Fixture constructs a fully populated 9x9 board. Returns `true`.
* **BF02:** Fixture constructs a fully populated 6x6 board. Returns `true`.
* **BF03:** Fixture constructs a full 9x9 board, then sets cell `[8][8] = ""`. Returns `false`.
* **BF04:** Fixture constructs a full 6x6 board, then sets cell `[5][5] = ""`. Returns `false`.
* **BF05:** Fixture constructs a standard 9x9 board with multiple empty cells. Returns `false`.
* **BF06:** Fixture constructs a default initialized 9x9 board where all cells are `""`. Returns `false`.


#### 8. Test Execution Results

<img width="974" height="716" alt="image" src="https://github.com/user-attachments/assets/7d0965c5-1e8f-4731-a10b-eddc9f242c41" />
<img width="974" height="716" alt="image" src="https://github.com/user-attachments/assets/1251db71-3b3c-48ce-b2c0-e3108d8665d0" />


#### 9. Test Count Calculation

#### Calculation for MBCC-1: `makeMove()`

* **Base Tests ($M$):** 2 (Base A: editable target, Base B: locked target)
* **Characteristics ($Q$):** 7 ($C_1$ to $C_7$)
* **Partition Counts & Non-Base Blocks ($B_i - m_i$):**
  * $C_1$ (Row Position): $B_1 = 3$, $m_1 = 1 \rightarrow B_1 - m_1 = 3 - 1 = 2$
  * $C_2$ (Column Position): $B_2 = 3$, $m_2 = 1 \rightarrow B_2 - m_2 = 3 - 1 = 2$
  * $C_3$ (Value Category): $B_3 = 4$, $m_3 = 1 \rightarrow B_3 - m_3 = 4 - 1 = 3$
  * $C_4$ (Move Conflict): $B_4 = 5$, $m_4 = 1 \rightarrow B_4 - m_4 = 5 - 1 = 4$
  * $C_5$ (Current Mutability): $B_5 = 2$, $m_5 = 1 \rightarrow B_5 - m_5 = 2 - 1 = 1$
  * $C_6$ (Existing Content): $B_6 = 2$, $m_6 = 1 \rightarrow B_6 - m_6 = 2 - 1 = 1$
  * $C_7$ (Requested Mutability): $B_7 = 2$, $m_7 = 2 \rightarrow B_7 - m_7 = 2 - 2 = 0$ *(Both blocks covered by Base A and Base B)*

Applying the MBCC calculation formula:

$$\sum_{i=1}^{7} (B_i - m_i) = 2 + 2 + 3 + 4 + 1 + 1 + 0 = 13 \text{ variations per base}$$

$$T_{makeMove} = 2 \times \left[ 1 + 13 \right] = 2 \times 14 = 28 \text{ test cases}$$


#### Calculation for MBCC-2: `boardFull()`

* **Base Tests ($M$):** 2 (Base Choice 1: Full 9x9, Base Choice 2: Almost Full 9x9)
* **Characteristics ($Q$):** 2 ($C_1, C_2$)
* **Partition Counts & Non-Base Blocks ($B_i - m_i$):**
  * $C_1$ (Completeness): $B_1 = 4$, $m_1 = 2$ ($A1, A2$) $\rightarrow B_1 - m_1 = 4 - 2 = 2$
  * $C_2$ (Dimension): $B_2 = 2$, $m_2 = 1$ ($B1$) $\rightarrow B_2 - m_2 = 2 - 1 = 1$

Applying the raw formula:

$$T_{raw} = M + M \sum_{i=1}^{2} (B_i - m_i) = 2 + 2(2 + 1) = 2 + 6 = 8 \text{ combinations}$$

**Duplicate Elimination:**
* Varying $C_1 \rightarrow A3$ from Base Choice 1 yields $[A3, B1]$
* Varying $C_1 \rightarrow A3$ from Base Choice 2 yields $[A3, B1]$ *(Duplicate)*
* Varying $C_1 \rightarrow A4$ from Base Choice 1 yields $[A4, B1]$
* Varying $C_1 \rightarrow A4$ from Base Choice 2 yields $[A4, B1]$ *(Duplicate)*

Consolidating the 2 duplicate combinations:

$$T_{boardFull} = 8 - 2 = 6 \text{ unique test cases}$$


#### Total Suite Test Count

$$\text{Total MBCC Test Cases} = T_{makeMove} + T_{boardFull} = 28 + 6 = 34 \text{ test cases}$$
