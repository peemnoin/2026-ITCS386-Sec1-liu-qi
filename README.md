# ITCS386 Project 1 — Unit Testing for Sudoku

**Team:** liu-qi  
**Repository:** 2026-ITCS386-Sec1-liu-qi  
**Submission folder:** `liu-qi_project1/`  
**Submission deadline:** 23 September 2026, before 23:55  
**Presentation and Q&A:** 24 September 2026

This README documents the team's Input Space Partitioning (ISP) unit tests for the selected open-source project. Each of the five members applies one combination criterion to two logical test suites. The original production code is kept unchanged.

## Contents

- [1. Project overview](#1-project-overview)
- [2. Team responsibilities and suite inventory](#2-team-responsibilities-and-suite-inventory)
- [3. Build and execution](#3-build-and-execution)
- [4. ACoC — Veerakron No-in](#4-acoc--veerakron-no-in)
- [5. ECC — Tinakome Rasripenngam](#5-ecc--tinakome-rasripenngam)
- [6. PWC — Sunattha Boonla-or](#6-pwc--sunattha-boonla-or)
- [7. MBCC — Wirunya Kaewthong](#7-mbcc--wirunya-kaewthong)
- [8. BCC — Piyada Chalermnontakarn](#8-bcc--piyada-chalermnontakarn)
- [9. Known defect in the production code](#9-known-defect-in-the-production-code)

## 1. Project overview

The selected project is [mattnenterprise/Sudoku](https://github.com/mattnenterprise/Sudoku), a Java Sudoku game with a Swing GUI. At the time of selection the repository had 58 stars (well above the required minimum of 20), is written in Java, is an actual software project rather than a tutorial, and was not chosen by any other group.

The project already ships a small test class (`SudokuPuzzleTest.java`) that tests `numInRow()`, `numInCol()`, and `numInBox()`. The team's new tests target other board-logic methods in `sudoku.SudokuPuzzle` and do not duplicate those existing tests. GUI classes (`SudokuFrame`, `SudokuPanel`) are not tested.

The team applies the five ISP combination criteria taught in class: All Combinations Coverage (ACoC), Each Choice Coverage (ECC), Pair-Wise Coverage (PWC), Base Choice Coverage (BCC), and Multiple Base Choice Coverage (MBCC). Each criterion is used in exactly two test suites, giving 10 additional unit test suites in total. Each suite documents the tested function, its parameters and return behaviour, interface-based and functionality-based characteristics, the combination step, and concrete test values with expected results.

## 2. Team responsibilities and suite inventory

| Member | Student ID | Criterion | Suite 1 (method) | Suite 2 (method) |
|---|---|---|---|---|
| Veerakron No-in | 6688164 | ACoC | `inRange()` | `getValue()` |
| Tinakome Rasripenngam | 6688095 | ECC | `isSlotMutable()` | `makeSlotEmpty()` |
| Sunattha Boonla-or | 6688009 | PWC | `isSlotAvailable()` | `makeMove()` |
| Wirunya Kaewthong | 6688172 | MBCC | `makeMove()` | `numInBox()` (being revised) |
| Piyada Chalermnontakarn | 6688239 | BCC | `isValidMove()` | `isSlotAvailable()` |

Each criterion is applied to two suites, so the five members cover all five combination approaches (each approach used in two suites), as required.

A method may be tested by more than one member as long as the characteristics differ. `makeMove()` is tested by both PWC and MBCC, and `isSlotAvailable()` by both PWC and BCC, but each uses a different set of characteristics and a different combination criterion, so the resulting test cases are distinct.

Each new test class is placed under `src/test/java/sudoku/`, separate from the existing `SudokuPuzzleTest.java`, and carries the required MIT copyright header with its author and the year 2026. The original `LICENSE` file is kept.

## 3. Build and execution

The project uses **Gradle** as its build system, with **JUnit 4.12** as the test framework. Run the tests through the existing Gradle build from the project directory that contains `build.gradle` and the Gradle wrapper (`liu-qi_project1/Sudoku-master/`):

```bash
# macOS / Linux
./gradlew test
```

```powershell
# Windows
.\gradlew.bat test
```

The HTML test report is generated at `build/reports/tests/test/index.html`. The presentation demonstrates the full test suite running through this Gradle build.

## 4. ACoC — Veerakron No-in

**Owner:** Veerakron No-in  
**Numbering:** Subsection numbers below are local to this contribution.  
**Scope:** Two logical test suites: `inRange()` (9 tests) and `getValue()` (11 tests), giving **20 tests** in total.

Each test uses a fresh 9×9 board with 3×3 boxes and values `"1"`–`"9"`. Cells start empty (`""`) and mutable. Valid array indices are 0–8.

The expected results below follow the characterization version described in this report: they record the original program's behaviour, including its index-9 defect. They are not a claim that the defect is correct or that the Java tests have been run successfully. See Section 9 for the defect details.

### ACoC-1: inRange()

#### 1. Testable Function

```java
public boolean inRange(int row, int col)
```

This method checks whether the given row and column are accepted as within the board range.

#### 2. Parameters

| Parameter | Description |
|---|---|
| `row` | Requested row index (`int`) |
| `col` | Requested column index (`int`) |

#### 3. Return Value and Exceptional Behaviour

The method returns `true` for accepted coordinates and `false` for rejected coordinates. No exception is expected because it only compares integers.

The original implementation also accepts index `9` when the other coordinate is between `0` and `9`. This is a known boundary defect.

#### 4. Input Domain Modeling

##### Interface-based characteristics

| ID | Characteristic | B1: Below range | B2: Valid | B3: At or above size |
|---|---|---|---|---|
| C1 | Row position | `row < 0`; use `-1` | `0 ≤ row < 9`; use `4` | `row ≥ 9`; use `9` |
| C2 | Column position | `col < 0`; use `-1` | `0 ≤ col < 9`; use `4` | `col ≥ 9`; use `9` |

##### Functionality-based characteristic

| ID | Characteristic | Blocks |
|---|---|---|
| C3 | Coordinate identifies an existing board cell | EXISTS / NO_CELL |

**Constraint:** C3 is EXISTS only when C1 and C2 are both B2; otherwise it is NO_CELL. C3 is derived from C1 and C2, so it adds no independent combinations.

#### 5. Combination Strategy (All Combinations Coverage)

ACoC covers every feasible combination of the modeled blocks.

- Before constraints: `3 × 3 × 2 = 18` combinations.
- Each of the nine row/column pairs permits only one C3 value, excluding nine combinations.
- Required tests: **18 − 9 = 9**.

#### 6. ACoC Test Requirements

| Test | Row block (C1) | Column block (C2) | Cell existence (C3) | Expected Result |
|---|---|---|---|---|
| IR01 | B1 | B1 | NO_CELL | `false` |
| IR02 | B1 | B2 | NO_CELL | `false` |
| IR03 | B1 | B3 | NO_CELL | `false` |
| IR04 | B2 | B1 | NO_CELL | `false` |
| IR05 | B2 | B2 | EXISTS | `true` |
| IR06 | B2 | B3 | NO_CELL | `true` |
| IR07 | B3 | B1 | NO_CELL | `false` |
| IR08 | B3 | B2 | NO_CELL | `true` |
| IR09 | B3 | B3 | NO_CELL | `true` |

#### 7. Test Values

| Test | `row` | `col` | Expected Result |
|---|---:|---:|---|
| IR01 | -1 | -1 | `false` |
| IR02 | -1 | 4 | `false` |
| IR03 | -1 | 9 | `false` |
| IR04 | 4 | -1 | `false` |
| IR05 | 4 | 4 | `true` |
| IR06 | 4 | 9 | `true` |
| IR07 | 9 | -1 | `false` |
| IR08 | 9 | 4 | `true` |
| IR09 | 9 | 9 | `true` |

IR06, IR08, and IR09 expect `true` to record the known defect. The correct array-bounds result would be `false`.

### ACoC-2: getValue()

#### 1. Testable Function

```java
public String getValue(int row, int col)
```

This method reads the value stored at the given board position.

#### 2. Parameters

| Parameter | Description |
|---|---|
| `row` | Requested row index (`int`) |
| `col` | Requested column index (`int`) |

The fixture also supplies the cell content and mutability state for existing cells.

#### 3. Return Value and Exceptional Behaviour

The method returns the stored `String` for an existing cell, or `""` when `inRange()` rejects the coordinates.

For `(4,9)`, `(9,4)`, and `(9,9)`, the original implementation throws `ArrayIndexOutOfBoundsException` because its range check incorrectly accepts index `9`. These cases record that exception as their expected outcome.

#### 4. Input Domain Modeling

##### Interface-based characteristics

| ID | Characteristic | B1: Below range | B2: Valid | B3: At or above size |
|---|---|---|---|---|
| C1 | Row position | `row < 0`; use `-1` | `0 ≤ row < 9`; use `4` | `row ≥ 9`; use `9` |
| C2 | Column position | `col < 0`; use `-1` | `0 ≤ col < 9`; use `4` | `col ≥ 9`; use `9` |

##### Functionality-based characteristic

C3: State of the addressed cell

| Block | Description | Fixture |
|---|---|---|
| EMPTY | Empty mutable cell | Value `""`, mutable `true` |
| PLAYER | Filled mutable cell | Value `"5"`, mutable `true` |
| GIVEN | Filled immutable cell | Value `"7"`, mutable `false` |
| NO_CELL | Coordinate does not identify a cell | No array access during setup |

PLAYER and GIVEN label fixture scenarios. This model covers non-null cell contents and excludes empty immutable cells.

**Constraints:** When C1 and C2 are both B2, C3 is EMPTY, PLAYER, or GIVEN. For all other coordinate pairs, C3 must be NO_CELL.

#### 5. Combination Strategy (All Combinations Coverage)

ACoC covers all feasible combinations within this model.

- Before constraints: `3 × 3 × 4 = 36` combinations.
- Both coordinates valid: `1 × 3 = 3` feasible combinations.
- At least one coordinate invalid: `8 × 1 = 8` feasible combinations.
- Required tests: **3 + 8 = 11**, equivalently **36 − 25 = 11**.

#### 6. ACoC Test Requirements

| Test | Row block (C1) | Column block (C2) | Cell state (C3) | Expected Result |
|---|---|---|---|---|
| GV01 | B1 | B1 | NO_CELL | `""` |
| GV02 | B1 | B2 | NO_CELL | `""` |
| GV03 | B1 | B3 | NO_CELL | `""` |
| GV04 | B2 | B1 | NO_CELL | `""` |
| GV05 | B2 | B2 | EMPTY | `""` |
| GV06 | B2 | B2 | PLAYER | `"5"` |
| GV07 | B2 | B2 | GIVEN | `"7"` |
| GV08 | B2 | B3 | NO_CELL | `ArrayIndexOutOfBoundsException` |
| GV09 | B3 | B1 | NO_CELL | `""` |
| GV10 | B3 | B2 | NO_CELL | `ArrayIndexOutOfBoundsException` |
| GV11 | B3 | B3 | NO_CELL | `ArrayIndexOutOfBoundsException` |

#### 7. Test Values

Each test starts with a fresh board. Existing-cell fixtures set `board` and `mutable` directly in package `sudoku`, without calling `makeMove()`. NO_CELL cases do not access invalid indices during setup.

| Test | `row` | `col` | Cell State | Expected Result |
|---|---:|---:|---|---|
| GV01 | -1 | -1 | NO_CELL | `""` |
| GV02 | -1 | 4 | NO_CELL | `""` |
| GV03 | -1 | 9 | NO_CELL | `""` |
| GV04 | 4 | -1 | NO_CELL | `""` |
| GV05 | 4 | 4 | EMPTY | `""` |
| GV06 | 4 | 4 | PLAYER | `"5"` |
| GV07 | 4 | 4 | GIVEN | `"7"` |
| GV08 | 4 | 9 | NO_CELL | `ArrayIndexOutOfBoundsException` |
| GV09 | 9 | -1 | NO_CELL | `""` |
| GV10 | 9 | 4 | NO_CELL | `ArrayIndexOutOfBoundsException` |
| GV11 | 9 | 9 | NO_CELL | `ArrayIndexOutOfBoundsException` |

GV08, GV10, and GV11 expect `ArrayIndexOutOfBoundsException` in the characterization version. This records the boundary defect; it does not fix it.
#### 8. Test Execution Results
<img width="729" height="943" alt="image" src="https://github.com/user-attachments/assets/4f3a24c8-6bfe-4434-8bc1-884dafe6459e" />

## 5. ECC — Tinakome Rasripenngam

**Owner:** Tinakome Rasripenngam (Dome)  
**Numbering:** Subsection numbers below are local to this contribution.

### ECC-1: isSlotMutable()

#### 1. Testable Function
```java
isSlotMutable(int row, int col)
```
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
```java
makeSlotEmpty(int row, int col)
```
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

#### 8. Test Execution Results
<img width="751" height="444" alt="image" src="https://github.com/user-attachments/assets/27179eef-36ac-44d4-afa1-d3dfe34bbf18" />

## 6. PWC — Sunattha Boonla-or

**Owner:** Sunattha Boonl-or (Grace)  
**Numbering:** Subsection numbers below are local to this contribution.

> **Model review:** Preserve the proposed cases, but do not claim completed PWC validation yet. An out-of-range coordinate has no target cell whose content or mutability can be set. In PWC-2/T5, a stored `"5"` also does not demonstrate a conflict with input `"X"`. See Section 10 for the required reconciliation with the Java tests.

### PWC-1: isSlotAvailable()

#### 1. Testable Function
```java
isSlotAvailable(int row, int col)
```
<br> This method checks whether a slot can be used, by verifying that the position is within the board range, the slot is empty, and the slot is mutable.
The test suite applies Pair-Wise Coverage (PWC) to ensure that every pair of blocks from two different characteristics appears in at least one test case.
#### 2. Parameters
| Parameter | Description |
|---|---|
| `row` | The row index of the Sudoku board |
| `col` | The column index of the Sudoku board |

#### 3. Return Value and Exceptional Behaviour
The method returns a boolean value:
if the position is valid, the slot is empty, and the slot is mutable
- false otherwise

Exceptional behaviour: No exception is expected for the selected concrete test cases.

The test cases use only valid board positions. This is intentional because cell-content and mutability states can only be defined for an existing board cell. Therefore, no out-of-range position is combined with cell-content or mutability blocks in this PWC model.
#### 4. Input Domain Modeling
##### Interface-based characteristic
C1: Position
| Partition | Description |
|---|---|
| A1: Boundary Position | The selected cell is located at a boundary of the 9×9 board. Representative: (0,0) |
| A2: Interior Position | The selected cell is located away from the board boundary. Representative: (4,4) |

##### Functionality-based characteristics
C2: Cell Content
 Partition | Description |
|---|---|
| B1: Empty | The selected slot contains `""` |
| B2: Occupied | The selected slot contains a Sudoku value, represented by "5" |

C3: Mutability
 Partition | Description |
|---|---|
| C1: Mutable | The selected slot can be modified (`mutable = true`) |
| C2: Immutable | The selected slot cannot be modified (`mutable = false`) |

All three characteristics are independently realizable because both position categories refer to existing cells on the 9×9 board.

#### 5. Combination Strategy (Pair-Wise Coverage)
Pair-Wise Coverage requires every pair of blocks from two different characteristics to appear together in at least one test. This method has three characteristics of two blocks each, so All Combinations (ACoC) would need 2 x 2 x 2 = 8 tests. The product of the two largest block counts, 2 x 2 = 4, is a lower bound for an unconstrained pairwise design. These four abstract rows cover its pairs; their concrete feasibility is reviewed below.

#### 6. PWC Test Requirements
| Test | Position Type | Cell Content | Mutability | Expected Result |
|---|---|---|---|---|
| T1 | A1: Boundary Position | B1: Empty | C1: Mutable | true |
| T2 | A1: Boundary Position | B2: Occupied | C2: Immutable | false |
| T3 | A2: Interior Position | B1: Empty | C2: Immutable | false |
| T4 | A2: Interior Position | B2: Occupied | C1: Mutable | false |

##### Pair Coverage Check

**Position Type × Cell Content**

- Boundary + Empty → T1
- Boundary + Occupied → T2
- Interior + Empty → T3
- Interior + Occupied → T4

All four pairs are covered.

**Position Type × Mutability**

- Boundary + Mutable → T1
- Boundary + Immutable → T2
- Interior + Immutable → T3
- Interior + Mutable → T4

All four pairs are covered.

**Cell Content × Mutability**

- Empty + Mutable → T1
- Occupied + Immutable → T2
- Empty + Immutable → T3
- Occupied + Mutable → T4

All four pairs are covered.

Therefore, every pair of blocks from two different characteristics appears at least once.

#### 7. Test Values
The test fixture uses a 9×9 Sudoku board.

The constructor initializes all cells as empty strings (`""`) and all cells as mutable (`true`). The test fixture directly modifies selected cells and their mutability states so that each required combination can be created.

| Test | row | col | Position Type | Cell Content | Mutability | Expected Result |
|---|---:|---:|---|---|---|---|
| T1 | 0 | 0 | Boundary Position | Empty | Mutable | true |
| T2 | 0 | 0 | Boundary Position | Occupied (`"5"`) | Immutable | false |
| T3 | 4 | 4 | Interior Position | Empty | Immutable | false |
| T4 | 4 | 4 | Interior Position | Occupied (`"5"`) | Mutable | false |

### PWC-2: makeMove()

#### 1. Testable Function
```java
 makeMove(int row, int col, String value, boolean isMutable)
```
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
Pair-Wise Coverage requires every pair of blocks from two different characteristics to appear together in at least one test. This method has four characteristics of two blocks each, so All Combinations (ACoC) would need 2 x 2 x 2 x 2 = 16 tests. The product 2 x 2 = 4 is a lower bound, not a general formula for the final count. Four rows are insufficient for four independent binary characteristics; the five abstract rows below cover all pairs. Concrete feasibility still needs checking.

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

All 24 label pairs appear in the abstract table, compared with 16 rows for the unconstrained Cartesian product. The concrete fixtures do not yet substantiate every assigned block, so complete PWC coverage is not claimed. For out-of-range or invalid-value cases, the conflict and mutability blocks do not affect the result; these assignments still require feasible fixtures; short-circuiting alone does not validate them.

#### 7. Test Values
The fixture uses a 9x9 board that starts empty and mutable. Specific cells are adjusted per test to create the required conflict or locked state. Each test uses a fresh puzzle so an applied move in one test does not affect another. The witness cell `(0,0)` is checked to confirm no unintended change for the rejected cases.
| Test | `row` | `col` | `value` | Setup | Expected `getValue(0,0)` |
|---|---:|---:|---|---|---|
| T1 | `0` | `0` | `"5"` | empty, mutable | `"5"` |
| T2 | `0` | `0` | `"5"` | `(0,4)="5"` conflict, `(0,0)` locked | `""` |
| T3 | `-1` | `0` | `"5"` | `(0,0)` locked | `""` |
| T4 | `0` | `0` | `"X"` | `(0,0)` locked | `""` |
| T5 | `-1` | `-1` | `"X"` | `(0,4)="5"` conflict, mutable | `""` |

#### 8. Test Execution Results
<img width="707" height="409" alt="Screenshot 2569-09-23 at 21 54 46" src="https://github.com/user-attachments/assets/ed79df7b-077f-46f0-83b0-71a8ff13dc9a" />

## 7. MBCC — Wirunya Kaewthong

**Owner:** Wirunya Kaewthong (Ingeye)  
**Numbering:** Subsection numbers below are local to this contribution.

> The MBCC contribution originally covered two methods: `makeMove()` (MM01-MM28) and `numInBox()` (NB01-NB12). The `numInBox()` suite is being revised because the existing project test class `SudokuPuzzleTest.java` already tests `numInBox()`, and the assignment does not allow duplicating an existing test. It will be added back here once it targets a method that is not already covered.

### MBCC-1: makeMove()

#### 1. Testable Function
Function: makeMove(int row, int col, String value, boolean isMutable)
<br> This method places a value into the target slot only when the value is an allowed digit, the move does not conflict with the same row, column, or box, and the slot is currently mutable. On an accepted move the target is assigned the proposed value and the requested mutability. Otherwise the board and the mutability flags are left unchanged.

#### 2. Parameters
| Parameter | Description |
|---|---|
| `row` | The row index of the target cell |
| `col` | The column index of the target cell |
| `value` | The proposed value to store in the target cell |
| `isMutable` | The mutability flag to set on the target if the move is accepted |

#### 3. Return Value and Exceptional Behaviour
This method returns `void`. Its effect is observed through the board state after the call, using `getValue(row, col)` and the mutability flag. An accepted move changes only the target value and its requested mutability; a rejected move leaves the entire state unchanged.

Exceptional behaviour: No exception is expected for the selected cases, including a `null` value. The guard uses short-circuit evaluation (`isValidValue(value) && isValidMove(row,col,value) && isSlotMutable(row,col)`), so an unsupported, empty, or `null` value is rejected by value validation before any array access. All selected coordinates are inside the modeled range 0-8.

#### 4. Input Domain Modeling
##### Interface-based characteristics
C1: Row Position
| Partition | Description |
|---|---|
| First | `row = 0` |
| Interior | `1 <= row <= 7`, represented by `row = 4` |
| Last | `row = 8` |

C2: Column Position
| Partition | Description |
|---|---|
| First | `col = 0` |
| Interior | `1 <= col <= 7`, represented by `col = 4` |
| Last | `col = 8` |

C3: Input Value Category
| Partition | Description |
|---|---|
| Allowed digit | An allowed value, represented by `"5"` |
| Unsupported string | A non-empty value that is not allowed, represented by `"X"` |
| Empty string | `""` |
| Null | `null` |

C7: Requested Final Mutability
| Partition | Description |
|---|---|
| True | `isMutable = true` |
| False | `isMutable = false` |

##### Functionality-based characteristics
C4: Other-cell Conflict (for an allowed proposed digit)
| Partition | Description |
|---|---|
| NONE | No conflicting occurrence of the value in the row, column, or box |
| ROW | The value already exists in the same row (different box) |
| COLUMN | The value already exists in the same column (different box) |
| BOX | The value already exists in the same box (different row and column) |
| MULTIPLE | The value exists in the row, column, and box simultaneously |

C5: Target Currently Editable
| Partition | Description |
|---|---|
| True | The target's `mutable` flag is `true` before the call |
| False | The target's `mutable` flag is `false` before the call |

C6: Existing Target Content
| Partition | Description |
|---|---|
| Empty | The target already holds `""` before the call |
| Different digit | The target already holds a different allowed digit, represented by `"2"` |

**Constraints:**
- C1 and C2 partition the valid coordinate range 0-8. Coordinates outside this range are out of this model's scope.
- C4 excludes the target itself; its blocks are mutually exclusive for an allowed candidate digit.
- For unsupported, empty, or `null` values, C4 uses NONE as a neutral fixture, since value validation rejects the input before any conflict check is relevant. Invalid values are not combined with ROW, COLUMN, BOX, or MULTIPLE fixtures.
- C6 excludes a target already containing the same allowed digit as the proposed value.

#### 5. Combination Strategy (Multiple Base Choice Coverage)
Multiple Base Choice Coverage selects one or more complete base tests, then, from each base, changes exactly one characteristic at a time to each of its non-base blocks while keeping the other base choices fixed.

Two base tests are chosen. They share a valid interior position, an allowed value, no conflict, and an editable empty target, and differ only in the requested final mutability (C7), so both boolean outcomes are observed under conditions where the move should succeed:
- Base A: `(row=4, col=4, value="5", conflict=NONE, currentMutable=true, oldValue="", requestedMutable=true)` — accepted, target stays editable.
- Base B: `(row=4, col=4, value="5", conflict=NONE, currentMutable=true, oldValue="", requestedMutable=false)` — accepted, target becomes locked.

The lecture's MBCC test count is `M + sum over i of M x (Bi - mi)`, where `M` is the number of base tests, `Bi` is the block count of characteristic `i`, and `mi` is its number of base blocks.

| Characteristic | Blocks Bi | Base blocks mi | Non-base variations per base |
|---|---:|---:|---:|
| C1: row | 3 | 1 | 2 |
| C2: column | 3 | 1 | 2 |
| C3: input value | 4 | 1 | 3 |
| C4: conflict | 5 | 1 | 4 |
| C5: current mutability | 2 | 1 | 1 |
| C6: existing content | 2 | 1 | 1 |
| C7: requested mutability | 2 | 2 | 0 |
| **Variations per base** | | | **13** |

With `M = 2`, the count is `2 x (1 + 13) = 28` tests. C7 adds no variation because both of its blocks are already base blocks. MM02-MM14 are the single-characteristic variations of Base A (MM01); MM16-MM28 are the corresponding variations of Base B (MM15).

#### 6. MBCC Test Requirements
Tuple order: `(row, col, value, conflict, currentMutable, oldValue, requestedMutable)`. ACCEPT changes only the target value and mutability; REJECT leaves the entire state unchanged.

| ID | Tuple | Expected Result |
|---|---|---|
| MM01 (Base A) | `(4, 4, "5", NONE, true, "", true)` | ACCEPT: target `"5"`, mutable `true` |
| MM02 | `(0, 4, "5", NONE, true, "", true)` | ACCEPT: target `"5"`, mutable `true` |
| MM03 | `(8, 4, "5", NONE, true, "", true)` | ACCEPT: target `"5"`, mutable `true` |
| MM04 | `(4, 0, "5", NONE, true, "", true)` | ACCEPT: target `"5"`, mutable `true` |
| MM05 | `(4, 8, "5", NONE, true, "", true)` | ACCEPT: target `"5"`, mutable `true` |
| MM06 | `(4, 4, "X", NONE, true, "", true)` | REJECT: state unchanged |
| MM07 | `(4, 4, "", NONE, true, "", true)` | REJECT: state unchanged |
| MM08 | `(4, 4, null, NONE, true, "", true)` | REJECT: state unchanged |
| MM09 | `(4, 4, "5", ROW, true, "", true)` | REJECT: state unchanged |
| MM10 | `(4, 4, "5", COLUMN, true, "", true)` | REJECT: state unchanged |
| MM11 | `(4, 4, "5", BOX, true, "", true)` | REJECT: state unchanged |
| MM12 | `(4, 4, "5", MULTIPLE, true, "", true)` | REJECT: state unchanged |
| MM13 | `(4, 4, "5", NONE, false, "", true)` | REJECT: state unchanged |
| MM14 | `(4, 4, "5", NONE, true, "2", true)` | ACCEPT: target `"5"`, mutable `true` |
| MM15 (Base B) | `(4, 4, "5", NONE, true, "", false)` | ACCEPT: target `"5"`, mutable `false` |
| MM16 | `(0, 4, "5", NONE, true, "", false)` | ACCEPT: target `"5"`, mutable `false` |
| MM17 | `(8, 4, "5", NONE, true, "", false)` | ACCEPT: target `"5"`, mutable `false` |
| MM18 | `(4, 0, "5", NONE, true, "", false)` | ACCEPT: target `"5"`, mutable `false` |
| MM19 | `(4, 8, "5", NONE, true, "", false)` | ACCEPT: target `"5"`, mutable `false` |
| MM20 | `(4, 4, "X", NONE, true, "", false)` | REJECT: state unchanged |
| MM21 | `(4, 4, "", NONE, true, "", false)` | REJECT: state unchanged |
| MM22 | `(4, 4, null, NONE, true, "", false)` | REJECT: state unchanged |
| MM23 | `(4, 4, "5", ROW, true, "", false)` | REJECT: state unchanged |
| MM24 | `(4, 4, "5", COLUMN, true, "", false)` | REJECT: state unchanged |
| MM25 | `(4, 4, "5", BOX, true, "", false)` | REJECT: state unchanged |
| MM26 | `(4, 4, "5", MULTIPLE, true, "", false)` | REJECT: state unchanged |
| MM27 | `(4, 4, "5", NONE, false, "", false)` | REJECT: state unchanged |
| MM28 | `(4, 4, "5", NONE, true, "2", false)` | ACCEPT: target `"5"`, mutable `false` |

Each Base A / Base B pair shares one test goal:

| Base A | Base B | Goal |
|---|---|---|
| MM01 | MM15 | Accept a normal entry and apply the requested final mutability |
| MM02 | MM16 | Accept an entry in the first valid row |
| MM03 | MM17 | Accept an entry in the last valid row |
| MM04 | MM18 | Accept an entry in the first valid column |
| MM05 | MM19 | Accept an entry in the last valid column |
| MM06 | MM20 | Reject an unsupported non-empty value |
| MM07 | MM21 | Reject an empty input value |
| MM08 | MM22 | Reject a null input value |
| MM09 | MM23 | Reject a value already present in the same row |
| MM10 | MM24 | Reject a value already present in the same column |
| MM11 | MM25 | Reject a value already present in the same box |
| MM12 | MM26 | Reject simultaneous row, column, and box conflicts |
| MM13 | MM27 | Reject a move into a currently locked target |
| MM14 | MM28 | Replace a different existing digit in an editable target |

#### 7. Test Values
Each test uses a fresh 9x9 puzzle created by `@Before` with all cells `""` and all flags `true`. The helper prepares the target's prior content and mutability, then places conflict digits when required: ROW at `(4,7)`, COLUMN at `(7,4)`, BOX at `(5,5)`, and MULTIPLE at all three. After one call to `makeMove(...)`, `assertArrayEquals()` compares every row of both the board and the mutable arrays against the expected state, which confirms the intended target change and detects any unintended change elsewhere. The JUnit method names follow the pattern `testMM01_Base_Editable`, `testMM15_Base_Locked`, and so on.

<img width="667" height="915" alt="image" src="https://github.com/user-attachments/assets/120c6c6f-77a8-4956-b775-16ec15d6caed" />

## 8. BCC — Piyada Chalermnontakarn

**Owner:** Piyada Chalermnontakarn (Nudee)  
**Numbering:** Subsection numbers below are local to this contribution.

> **Scope review:** The invalid-coordinate rows test rejection before a target cell is accessed. Their cell-state/conflict labels need a neutral-fixture or not-applicable interpretation. The supplied report also omits the exact conflict fixture for BCC-1/T4. See Section 10.

### BCC-1: isValidMove()
#### 1.Testable Function
```java
isValidMove(int row, int col, String value)
```
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
```java
isSlotAvailable(int row, int col)
```
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
- 
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
<img width="706" height="614" alt="image" src="https://github.com/user-attachments/assets/c6208fa8-f8f3-494e-8073-8b0e876963e2" />

#### 9. Test Count
For BCC-1, there are three characteristics, and each characteristic has two blocks:
\[
N_{BCC} = 1 + (2-1) + (2-1) + (2-1)
\]

\[
N_{BCC} = 4
\]
BCC-1 requires **4 test cases*

BCC-2, there are also three characteristics, and each characteristic has two blocks:
\[
N_{BCC} = 1 + (2-1) + (2-1) + (2-1)
\]

\[
N_{BCC} = 4
\]

Therefore, BCC-2 requires **4 test cases**.

## 9. Known defect in the production code

While designing the ISP tests, the team found an off-by-one boundary defect in the production code. It is documented here; the production code is **not** modified.

**Location:** `SudokuPuzzle.inRange(int row, int col)`

```java
return row <= this.ROWS && col <= this.COLUMNS
        && row >= 0 && col >= 0;
```

For a 9x9 board the valid indices are 0 through 8, but the condition uses `<=`, so it also accepts index 9 (`9 <= 9` is true). Methods that trust `inRange()` before accessing the array are then exposed to an out-of-bounds access.

| Call | Correct behaviour | Observed behaviour |
|---|---|---|
| `inRange(4,9)`, `inRange(9,4)`, `inRange(9,9)` | `false` | `true` |
| `getValue(4,9)`, `getValue(9,4)`, `getValue(9,9)` | `""` | `ArrayIndexOutOfBoundsException` |

These are manifestations of a single root defect, not several independent bugs. The ACoC suite documents this observed behaviour explicitly rather than hiding it, and other suites keep their coordinates inside the valid 0-8 range so the defect does not affect their results.
