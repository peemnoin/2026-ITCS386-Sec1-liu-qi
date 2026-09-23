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
| Wirunya Kaewthong | 6688172 | MBCC | `makeMove()` | `boardFull()` |
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
| IR06 | B2 | B3 | NO_CELL | `false` |
| IR07 | B3 | B1 | NO_CELL | `false` |
| IR08 | B3 | B2 | NO_CELL | `false` |
| IR09 | B3 | B3 | NO_CELL | `false` |

#### 7. Test Values

| Test | `row` | `col` | Expected Result |
|---|---:|---:|---|
| IR01 | -1 | -1 | `false` |
| IR02 | -1 | 4 | `false` |
| IR03 | -1 | 9 | `false` |
| IR04 | 4 | -1 | `false` |
| IR05 | 4 | 4 | `true` |
| IR06 | 4 | 9 | `false` |
| IR07 | 9 | -1 | `false` |
| IR08 | 9 | 4 | `false` |
| IR09 | 9 | 9 | `false` |

IR06, IR08, and IR09 show `true` to which is known defect. The correct array-bounds result would be `false`.

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

#### 8. Defect report — D01: inclusive upper bounds

**Location:** SudokuPuzzle.inRange(int row, int col)  
**Type:** Off-by-one boundary defect  
**Status:** Observed and documented; production code intentionally unchanged.

The original condition is:

```java
return row <= this.ROWS && col <= this.COLUMNS
        && row >= 0 && col >= 0;
```

For a dimension of 9, array indices run from 0 to 8. The condition accepts 9 because 9 <= 9 is true.

| Reproduction | Correct expected behavior | Observed original behavior |
|---|---|---|
| inRange(4,9) | false | true |
| inRange(9,4) | false | true |
| inRange(9,9) | false | true |
| getValue(4,9) | empty String | ArrayIndexOutOfBoundsException |
| getValue(9,4) | empty String | ArrayIndexOutOfBoundsException |
| getValue(9,9) | empty String | ArrayIndexOutOfBoundsException |

getValue() relies on inRange(). When the faulty guard accepts a nonexistent cell, getValue() accesses board[row][col] and throws. The six failing correctness tests reveal multiple manifestations of the same root defect; they should not be reported as six independent bugs.

The characterization tests retain these inputs and explicitly record the observed outcomes. If the defect is fixed later, these six characterization expectations must be reviewed.
#### 9. Test Execution Results
<img width="729" height="943" alt="image" src="https://github.com/user-attachments/assets/4f3a24c8-6bfe-4434-8bc1-884dafe6459e" />

## 5. ECC — Tinakome Rasripenngam

**Owner:** Tinakome Rasripenngam (Dome)  
**Numbering:** Subsection numbers below are local to this contribution.

### ECC-1: isSlotMutable()

#### 1. Testable Function
Function: isSlotMutable(int row, int col)
<br> This method returns whether the slot at the given position is currently editable, based only on the internal `mutable` flag of that cell.

#### 2. Parameters
| Parameter | Description |
|---|---|
| `row` | The row index of the Sudoku board |
| `col` | The column index of the Sudoku board |

#### 3. Return Value and Exceptional Behaviour
The method returns a boolean value:
- `true` if the slot at `(row, col)` is mutable
- `false` if the slot at `(row, col)` is locked

Exceptional behaviour: Unlike `isSlotAvailable()`, this method does not call `inRange()` before accessing the array. It reads `this.mutable[row][col]` directly, so a `row` or `col` outside the board throws an uncaught `ArrayIndexOutOfBoundsException` instead of returning a boolean. Out-of-range input is outside the scope of this suite, which tests the method's normal in-range contract.

#### 4. Input Domain Modeling
##### Interface-based characteristic
C1: Column Position
| Partition | Description |
|---|---|
| A1: Boundary column | `col` is the first column of the board (`col = 0`) |
| A2: Non-boundary column | `col` is not a board edge (`col = 1`) |

##### Functionality-based characteristic
C2: Mutability State
| Partition | Description |
|---|---|
| B1: Mutable | The slot's `mutable` flag is `true` |
| B2: Immutable | The slot's `mutable` flag is `false` |

#### 5. Combination Strategy (Each Choice Coverage)
Each Choice Coverage requires every block of every characteristic to appear in at least one test case. The minimum number of tests is the size of the largest characteristic. Both characteristics have two blocks, so 2 test cases are enough, compared with 2 x 2 = 4 for All Combinations.

#### 6. ECC Test Requirements
| Test | Column Position | Mutability State | Expected Result |
|---|---|---|---|
| T1 | A1: Boundary column | B1: Mutable | `true` |
| T2 | A2: Non-boundary column | B2: Immutable | `false` |

Each-choice check:
- C1 blocks covered: A1 (T1), A2 (T2).
- C2 blocks covered: B1 (T1), B2 (T2).

Every block appears at least once, so the two tests satisfy Each Choice Coverage.

#### 7. Test Values
The fixture `SudokuPuzzleForTesting` is a 9x9 board created fresh before each test by `@Before`. Slot `(0,0)` holds `"5"` and is mutable. Slot `(0,1)` holds `"3"` and is locked (`mutable = false`).
| Test | JUnit method | `row` | `col` | Column Position | Mutability State | Expected |
|---|---|---:|---:|---|---|---|
| T1 | `testIsSlotMutableBoundaryColumnMutable` | `0` | `0` | Boundary column | Mutable | `true` |
| T2 | `testIsSlotMutableNonBoundaryColumnImmutable` | `0` | `1` | Non-boundary column | Immutable | `false` |

### ECC-2: makeSlotEmpty()

#### 1. Testable Function
Function: makeSlotEmpty(int row, int col)
<br> This method clears the slot at the given position by setting it to an empty string, regardless of the value stored there before.

#### 2. Parameters
| Parameter | Description |
|---|---|
| `row` | The row index of the Sudoku board |
| `col` | The column index of the Sudoku board |

#### 3. Return Value and Exceptional Behaviour
This method returns `void`. Its effect is observed through `getValue(row, col)` after the call.

Exceptional behaviour: Like `isSlotMutable()`, this method does not call `inRange()` before writing. It assigns `this.board[row][col] = ""` directly, so an out-of-range position throws an uncaught `ArrayIndexOutOfBoundsException`. Out-of-range input is outside the scope of this suite.

#### 4. Input Domain Modeling
##### Interface-based characteristic
C1: Column Position
| Partition | Description |
|---|---|
| A1: Boundary column | `col` is the first column of the board (`col = 0`) |
| A2: Non-boundary column | `col` is not a board edge (`col = 2`) |

##### Functionality-based characteristic
C2: Prior Cell Content
| Partition | Description |
|---|---|
| B1: Has value | The slot contains a non-empty value before clearing |
| B2: Already empty | The slot is already `""` before clearing |

#### 5. Combination Strategy (Each Choice Coverage)
Both characteristics have two blocks, so 2 test cases cover every block, compared with 2 x 2 = 4 for All Combinations.

#### 6. ECC Test Requirements
| Test | Column Position | Prior Cell Content | Expected Result (after clearing) |
|---|---|---|---|
| T1 | A1: Boundary column | B1: Has value | `""` |
| T2 | A2: Non-boundary column | B2: Already empty | `""` |

Each-choice check:
- C1 blocks covered: A1 (T1), A2 (T2).
- C2 blocks covered: B1 (T1), B2 (T2).

Every block appears at least once, so the two tests satisfy Each Choice Coverage. T2 also shows that the method is idempotent: clearing an already empty slot leaves it empty.

#### 7. Test Values
The same fixture is used. Slot `(0,0)` holds `"5"` before clearing. Slot `(0,2)` keeps its default value `""`. Each test first asserts the precondition, so the test proves the slot really changed from its prior state. T1 also checks that the neighbouring slot `(0,1)` still holds `"3"`, confirming that only the target slot is cleared.
| Test | JUnit method | `row` | `col` | Precondition | Expected after call |
|---|---|---:|---:|---|---|
| T1 | `testMakeSlotEmptyBoundaryColumnHasValue` | `0` | `0` | `getValue(0,0) = "5"` | `getValue(0,0) = ""`, `getValue(0,1) = "3"` |
| T2 | `testMakeSlotEmptyNonBoundaryColumnAlreadyEmpty` | `0` | `2` | `getValue(0,2) = ""` | `getValue(0,2) = ""` |

#### 8. Test Execution Results
<img width="799" height="506" alt="Screenshot 2569-09-23 at 23 17 47" src="https://github.com/user-attachments/assets/2c988956-f53c-4169-b8ae-afaf4f1d52ba" />

#### 9. Test Count
#### Calculation for ECC-1: `isSlotMutable()`

- **Characteristics (Q):** 2 (C1, C2)
- **Partition Counts (Bᵢ):**
  - **C1 (Column Position):** B₁ = 2
  - **C2 (Mutability State):** B₂ = 2

Each Choice Coverage requires every block of every characteristic to appear in at least one test. One test can use only one block from each characteristic, so the minimum number of tests equals the largest block count.

Applying the ECC calculation formula:

$$
T_{ECC} = \max_{i=1}^{Q}(B_i)
$$

$$
T_{isSlotMutable}
= \max(2, 2)
= 2\text{ test cases}
$$

Therefore, ECC-1 requires 2 test cases.

#### Calculation for ECC-2: `makeSlotEmpty()`

- **Characteristics (Q):** 2 (C1, C2)
- **Partition Counts (Bᵢ):**
  - **C1 (Column Position):** B₁ = 2
  - **C2 (Prior Cell Content):** B₂ = 2

Applying the ECC calculation formula:

$$
T_{ECC} = \max_{i=1}^{Q}(B_i)
$$

$$
T_{makeSlotEmpty}
= \max(2, 2)
= 2\text{ test cases}
$$

Therefore, ECC-2 requires 2 test cases.

Total Suite Test Count

$$
T_{Total}
= T_{isSlotMutable} + T_{makeSlotEmpty}
$$

$$
T_{Total}
= 2 + 2
= 4\text{ test cases}
$$

Therefore, the total ECC test count is 4 test cases.

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
<img width="733" height="631" alt="Screenshot 2569-09-23 at 22 37 27" src="https://github.com/user-attachments/assets/9efb05ca-a8ab-4c7d-9792-8eb6ee9042d1" />

#### 9. Test Count
#### Calculation for PWC-1: `isSlotAvailable()`

- **Characteristics (Q):** 3 (C1, C2, C3)
- **Partition Counts (Bᵢ):**
  - **C1 (Position Type):** B₁ = 2
  - **C2 (Cell Content):** B₂ = 2
  - **C3 (Mutability):** B₃ = 2
- **Pairs to Cover:** 3 characteristic pairs × (2 × 2) = 12 pairs

Pair-Wise Coverage requires every pair of blocks from two different characteristics to appear together in at least one test. The number of tests is at least the product of the two largest characteristics.

Applying the PWC calculation formula:

$$
T_{PWC} \geq \left(\max_{i=1}^{Q} B_i\right) \times \left(\max_{j=1,\, j \neq i}^{Q} B_j\right)
$$

$$
T_{isSlotAvailable}
\geq 2 \times 2
= 4\text{ test cases}
$$

The four tests in section 6 cover all 12 pairs, so the lower bound is reached.

Therefore, PWC-1 requires 4 test cases (All Combinations would require 2 × 2 × 2 = 8).

#### Calculation for PWC-2: `makeMove()`

- **Characteristics (Q):** 4 (C1, C2, C3, C4)
- **Partition Counts (Bᵢ):**
  - **C1 (Value Validity):** B₁ = 2
  - **C2 (Position):** B₂ = 2
  - **C3 (Move Conflict):** B₃ = 2
  - **C4 (Mutability):** B₄ = 2
- **Pairs to Cover:** 6 characteristic pairs × (2 × 2) = 24 pairs

Applying the PWC calculation formula:

$$
T_{PWC} \geq \left(\max_{i=1}^{Q} B_i\right) \times \left(\max_{j=1,\, j \neq i}^{Q} B_j\right)
$$

$$
T_{makeMove}
\geq 2 \times 2
= 4\text{ test cases}
$$

The formula gives a lower bound only. With 4 tests, every pair of characteristics must show each of its 4 block combinations exactly once, so each characteristic uses each block exactly twice. If the first test uses the first block of every characteristic, each characteristic must place its second block in 2 of the remaining 3 tests. There are only 3 ways to choose 2 tests out of 3, so at most 3 characteristics can fit. Two characteristics sharing the same choice would never form a mixed pair. A fourth characteristic therefore needs one more test.

$$
T_{makeMove}
= 5\text{ test cases}
$$

Therefore, PWC-2 requires 5 test cases, which is the minimum possible (All Combinations would require 2 × 2 × 2 × 2 = 16).

Total Suite Test Count

$$
T_{Total}
= T_{isSlotAvailable} + T_{makeMove}
$$

$$
T_{Total}
= 4 + 5
= 9\text{ test cases}
$$

Therefore, the total PWC test count is 9 test cases.

## 7. MBCC — Wirunya Kaewthong

**Owner:** Wirunya Kaewthong (Ingeye)  
**Numbering:** Subsection numbers below are local to this contribution.

### MBCC-1: makeMove()

#### 1. Testable Function
```java
makeMove(int row, int col, String value, boolean isMutable)
```
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
```java
boardFull()
```
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
### C3: Row Conflict
| Block | Description | Base |
|---|---|---|
| C3.1 No Row Conflict | The value does not exist in the same row | ✓ |
| C3.2 Row Conflict | The value already exists in the same row | |


### C4: Column Conflict

| Block | Description | Base |
|---|---|---|
| C4.1 No Column Conflict | The value does not exist in the same column | ✓ |
| C4.2 Column Conflict | The value already exists in the same column | |


### C5: Box Conflict

| Block | Description | Base |
|---|---|---|
| C5.1 No Box Conflict | The value does not exist in the same 3×3 box | ✓ |
| C5.2 Box Conflict | The value already exists in the same 3×3 box | |

#### 5. Base Choice
The base choice consists of:

- C1: Valid Row
- C2: Valid Column
- C3: No Row Conflict
- C4: No Column Conflict
- C5: No Box Conflict

Therefore, the base test is:
(row, col, value) = (0, 0, "1")
Expected result: true

#### 6.  BCC Test Cases
| Test | Row Position | Column Position | Row Conflict | Column Conflict | Box Conflict | Expected Result |
|---|---|---|---|---|---|---|
| T1 (Base) | Valid | Valid | No | No | No | true |
| T2 | Invalid | Valid | No | No | No | false |
| T3 | Valid | Invalid | No | No | No | false |
| T4 | Valid | Valid | Yes | No | No | false |
| T5 | Valid | Valid | No | Yes | No | false |
| T6 | Valid | Valid | No | No | Yes | false |

- **T1** is the base test using all base choices.
- **T2** changes only the Row Position from valid to invalid.
- **T3** changes only the Column Position from valid to invalid.
- **T4** changes only Row Conflict from no conflict to conflict.
- **T5** changes only Column Conflict from no conflict to conflict.
- **T6** changes only Box Conflict from no conflict to conflict.

#### 7. Test Values
| Test | row | col | value | Conflict Type | Expected Result |
|---|---:|---:|---|---|---|
| T1 (Base) | 0 | 0 | "1" | No conflict | true |
| T2 | -1 | 0 | "1" | No conflict | false |
| T3 | 0 | -1 | "1" | No conflict | false |
| T4 | 0 | 0 | "8" | Row conflict | false |
| T5 | 0 | 0 | "8" | Column conflict | false |
| T6 | 0 | 0 | "8" | Box conflict | false |

T1: Position (0,0) is within the board range, and value "1" does not conflict with any existing value in the same row, column, or box.

T2: row = -1 represents an invalid row position, causing the method to return false.

T3: col = -1 represents an invalid column position, causing the method to return false.

T4: Value "8" already exists in the same row at position (0,3), while being outside the same column and box. Therefore, the method returns false due to a row conflict.

T5: Value "8" already exists in the same column at position (3,0), while being outside the same row and box. Therefore, the method returns false due to a column conflict.

T6: Value "8" already exists in the same 3×3 box at position (1,1), while being outside the same row and column. Therefore, the method returns false due to a box conflict.
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
<img width="843" height="792" alt="image" src="https://github.com/user-attachments/assets/e67a9416-e08b-4d56-9216-5e49c28eca47" />

#### 9. Test Count
#### Calculation for BCC-1: `isValidMove()`

- **Base Tests (M):** 1 (Base Choice: Valid row, Valid column, No conflict)
- **Characteristics (Q):** 5
- **Partition Counts & Non-Base Blocks (Bᵢ − mᵢ):**
  - **C1 (Row Position):** B₁ = 2, m₁ = 1 → 2 − 1 = 1
  - **C2 (Column Position):** B₂ = 2, m₂ = 1 → 2 − 1 = 1
  - **C3 (Row Conflict):** B₃ = 2, m₃ = 1 → 2 − 1 = 1
  - **C4 (Column Conflict):** B₄ = 2, m₄ = 1 → 2 − 1 = 1
  - **C5 (Box Conflict):** B₅ = 2, m₅ = 1 → 2 − 1 = 1

Applying the BCC calculation formula:

$$
T_{BCC} = M\left[1+\sum_{i=1}^{Q}(B_i-m_i)\right]
$$

$$
T_{isValidMove}
= 1\left[1+(1+1+1+1+1)\right]
= 1[6]
= 6\text{ test cases}
$$

Therefore, BCC-1 requires 6 test cases.

### Calculation for BCC-2: `isSlotAvailable()`

- **Base Tests (M):** 1 (Base Choice: Valid row, Valid column, Available slot)
- **Characteristics (Q):** 3 (C1, C2, C3)
- **Partition Counts & Non-Base Blocks (Bᵢ − mᵢ):**
  - **C₁ (Row Position):** B₁ = 2, m₁ = 1 → B₁ − m₁ = 2 − 1 = 1
  - **C₂ (Column Position):** B₂ = 2, m₂ = 1 → B₂ − m₂ = 2 − 1 = 1
  - **C₃ (Slot State):** B₃ = 2, m₃ = 1 → B₃ − m₃ = 2 − 1 = 1

Applying the BCC calculation formula:

$$
T_{BCC} = M\left[1+\sum_{i=1}^{Q}(B_i-m_i)\right]
$$

$$
T_{isSlotAvailable}
= 1\left[1+(1+1+1)\right]
= 1[4]
= 4\text{ test cases}
$$

Therefore, BCC-2 requires 4 test cases.

Total Suite Test Count

$$
T_{Total}
= T_{isValidMove} + T_{isSlotAvailable}
$$

$$
T_{Total}
= 6 + 4
= 10\text{ test cases}
$$

Therefore, the total BCC test count is 10 test cases.

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
## 10. Overall Test Results
<img width="1376" height="627" alt="image" src="https://github.com/user-attachments/assets/71ec734a-051e-4d3a-a4fe-aca2f9494d0a" />

