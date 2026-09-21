# ITCS386 Project 1 — Unit Testing for Sudoku

**Team:** liu-qi  
**Repository:** 2026-ITCS386-Sec1-liu-qi  
**Submission folder:** `liu-qi_project1/`  
**Submission deadline:** 23 September 2026, before 23:55  
**Presentation and Q&A:** 24 September 2026

This README combines the five members' input space partitioning (ISP) reports. It documents **10 logical suites and 81 designed scenarios**. These are design counts from the supplied reports, not a verified combined Gradle execution count. The original production code is kept unchanged.

## Contents

- [1. Project overview](#1-project-overview)
- [2. Team responsibilities and suite inventory](#2-team-responsibilities-and-suite-inventory)
- [3. Build, execution, and documentation conventions](#3-build-execution-and-documentation-conventions)
- [4. ACoC — Veerakron No-in](#4-acoc--veerakron-no-in)
- [5. ECC — Tinakome Rasripenngam](#5-ecc--tinakome-rasripenngam)
- [6. PWC — Sunattha Boonl-or](#6-pwc--sunattha-boonl-or)
- [7. MBCC — Wirunya Kaewthong](#7-mbcc--wirunya-kaewthong)
- [8. BCC — Piyada Chalermnontakarn](#8-bcc--piyada-chalermnontakarn)
- [9. Consolidated results and known defect](#9-consolidated-results-and-known-defect)
- [10. Integration review and submission checklist](#10-integration-review-and-submission-checklist)

## 1. Project overview

The selected project is [mattnenterprise/Sudoku](https://github.com/mattnenterprise/Sudoku), a Java Sudoku application with a Swing interface. The team's tests in these reports target the board logic in `sudoku.SudokuPuzzle` rather than GUI interaction.

The work applies five ISP combination criteria: All Combinations Coverage (ACoC), Each Choice Coverage (ECC), Pair-Wise Coverage (PWC), Base Choice Coverage (BCC), and Multiple Base Choice Coverage (MBCC). Each criterion is assigned to two logical suites. The purpose is to explain how concrete tests follow from characteristics, partitions, constraints, and expected outcomes.

**Evidence scope:** This combined report was assembled from five member READMEs. Test source files and a final full-team Gradle report were not supplied with them. Historical execution statements below are attributed to their source reports; no new test execution is claimed. Project-selection evidence such as the star count at selection and confirmation that no other group chose the project should be retained with the submission.

## 2. Team responsibilities and suite inventory

| Member | StudentID | Criterion | Logical suites | Designed scenarios |
|---|---|---|---:|---:|
| Veerakron No-in | 6688164 | ACoC | 2 | 20 |
| Tinakome Rasripenngam | 6688 | ECC | 2 | 4 |
| Sunattha Boonl-o | 6688 | PWC | 2 | 9 |
| Wirunya Kaewthong | 6688172 | MBCC | 2 | 40 |
| Piyada Chalermnontakarn | 6688239 | BCC | 2 | 8 |
| **Total** | | **5 criteria** | **10** | **81** |

| Suite | Local identifier | Tested method | Criterion | Cases | Reason for count |
|---:|---|---|---|---:|---|
| 1 | ACoC-1 / IR01–IR09 | `inRange(row, col)` | ACoC | 9 | 18 raw combinations minus 9 infeasible combinations |
| 2 | ACoC-2 / GV01–GV11 | `getValue(row, col)` | ACoC | 11 | 36 raw combinations minus 25 infeasible combinations |
| 3 | ECC-1 / T1–T2 | `isSlotMutable(row, col)` | ECC | 2 | Cover both blocks of each of two characteristics |
| 4 | ECC-2 / T1–T2 | `makeSlotEmpty(row, col)` | ECC | 2 | Cover both blocks of each of two characteristics |
| 5 | PWC-1 / T1–T4 | `isSlotAvailable(row, col)` | PWC | 4 | Four proposed rows for three binary characteristics; feasibility review required |
| 6 | PWC-2 / T1–T5 | `makeMove(row, col, value, isMutable)` | PWC | 5 | Five proposed rows for four binary characteristics; fixture review required |
| 7 | MBCC-1 / MM01–MM28 | `makeMove(row, col, value, isMutable)` | MBCC | 28 | Two bases, each with 13 non-base variations |
| 8 | MBCC-2 / NB01–NB12 | `numInBox(row, col, value)` | MBCC | 12 | Two bases, each with five non-base variations |
| 9 | BCC-1 / T1–T4 | `isValidMove(row, col, value)` | BCC | 4 | One base plus three single-characteristic variations |
| 10 | BCC-2 / T1–T4 | `isSlotAvailable(row, col)` | BCC | 4 | One base plus three single-characteristic variations |

A **suite** here is a logical group for a tested method and criterion. A JUnit **test case** is an implemented test method; several assertions may belong to one case. Two logical suites can share one Java test class. Prefix local IDs with their suite, for example `ECC-1/T1`, to avoid confusing repeated T1 labels.

The 10 suites target **eight distinct methods**: `makeMove()` and `isSlotAvailable()` each appear in two contributions. Testing the same method does not automatically mean every scenario is duplicated, but the fixtures and assertions must be compared. The existing project's `numInBox()` tests also require comparison with MBCC-2. These checks are recorded in Section 10.

## 3. Build, execution, and documentation conventions

Run commands from the Sudoku project directory containing `build.gradle`, `gradlew`, and `gradlew.bat`, inside `liu-qi_project1/`. Do not assume the team repository root is the Gradle project root.

The supplied reports identify the original configuration as **Gradle 5.2.1 and JUnit 4.12**. Use the team's established compatible JDK configuration and record it with the final run. The earlier project setup uses JDK 11; the MBCC report's separate Java 17 verification does not establish wrapper compatibility.

Windows PowerShell:

```powershell
java -version
.\gradlew.bat --version
.\gradlew.bat clean test
```

macOS/Linux:

```bash
java -version
bash gradlew --version
bash gradlew clean test
```

Open `build/reports/tests/test/index.html` after execution. Preserve the final full-run report before running filtered tests, which may overwrite the report. The presentation must demonstrate execution through the existing Gradle build system.

New tests belong under `src/test/java/sudoku/`, separately from existing test classes. Confirmed names from the reports are `SudokuACoCTest.java` and `SudokuMBCCTest.java`; the ECC, PWC, and BCC reports do not supply their enclosing test-class names. Each new Java file needs the required copyright header with its actual author(s), year 2026, and the project's MIT license. Retain the original `LICENSE`.

Each contribution documents the tested function, inputs and outputs, interface-based and functionality-based characteristics, combinations, and concrete expected outcomes. `@Before` creates a fresh fixture for each test where stated. `@After` is needed only when cleanup is required; these in-memory fixtures do not open external resources.

**Expected and actual results are separate:** an expected result is the test oracle; an actual result requires execution evidence. ACoC deliberately characterizes an existing defect. Its passing boundary tests do not mean that the boundary behavior is correct.


## 4. ACoC — Veerakron No-in

**Owner:** Veerakron No-in  
**Numbering:** Subsection numbers below are local to this contribution.

**Contributor:** Veerakron No-in  
**Team:** liu-qi  
**Production class:** `sudoku.SudokuPuzzle`  
**Test class:** `sudoku.SudokuACoCTest`  
**Scope:** Two logical test suites: `inRange()` and `getValue()`.

> This section covers the contributor's two suites. The original production code is not modified.

### 1. Purpose and test strategy

The tests apply Input Space Partitioning (ISP) and All Combinations Coverage (ACoC) to select concrete input combinations.

The first test version used correctness expectations: coordinates outside a 9×9 board should be rejected, and getValue() should return an empty string for coordinates rejected as out of range. Its execution exposed six failures.

The current version is a **characterization test suite**: it checks the observed behavior of the original implementation, including its known boundary defect. Six expected outcomes were changed; the inputs and number of test cases were not changed. A passing characterization test is not evidence that the boundary behavior is correct.

### 2. Test environment and execution

The original project configuration uses Gradle 5.2.1 and JUnit 4.12. Record the actual environment used for the submitted run with:

```powershell
java -version
.\gradlew.bat --version
```

Place the new class at:

```text
src/test/java/sudoku/SudokuACoCTest.java
```

Keep a copy of each relevant report before rerunning, because generated reports may be overwritten. The assignment demonstration uses the existing Gradle build system.

### 3. Shared fixture and test isolation

Before each test method, JUnit executes the method annotated with `@Before`:

```java
@Before
public void setUp() {
    puzzle = new SudokuPuzzle(
        9, 9, 3, 3,
        new String[]{"1","2","3","4","5","6","7","8","9"}
    );
}
```

This creates a new 9-row, 9-column board with 3×3 boxes. The constructor initializes all cells to `""` and all mutability flags to `true`.

- Valid array indices are 0 through 8; 9 is the number of rows/columns, not the last index.
- Each test receives a fresh board and does not depend on test execution order.
- The getValue() tests prepare board and mutable fields directly in package sudoku. This avoids depending on makeMove() for fixture construction.
- No external resource needs cleanup, so `@After` is unnecessary.
- JUnit discovers one test class containing 20 test methods. The two suites below are logical groups documented in comments and this report.

### 4. Suite 1 — inRange(row, col)

#### 4.1 Testable function and objective

```java
public boolean inRange(int row, int col)
```

Check the return value for all combinations of the modeled row and column categories. The current version explicitly records the original implementation's acceptance of coordinates equal to the board size.

#### 4.2 Parameters, returns, and exceptional behavior

| Item | Description |
|---|---|
| row | int: requested row index |
| col | int: requested column index |
| Implicit input | Initialized board with ROWS=9 and COLUMNS=9 |
| Return type | boolean |
| Correct bounds behavior | true iff 0 ≤ row < 9 and 0 ≤ col < 9 |
| Current implementation | true iff 0 ≤ row ≤ 9 and 0 ≤ col ≤ 9 |
| Exception for modeled cases | None expected; this method only compares integers |

#### 4.3 Input domain model

| ID | Characteristic | Type | Blocks and representatives |
|---|---|---|---|
| C1 | Row relative to array bounds | Interface-based | B1: row < 0 → -1; B2: 0 ≤ row < 9 → 4; B3: row ≥ 9 → 9 |
| C2 | Column relative to array bounds | Interface-based | B1: col < 0 → -1; B2: 0 ≤ col < 9 → 4; B3: col ≥ 9 → 9 |
| C3 | Coordinate identifies an existing board cell | Functionality-based, derived | EXISTS / NO_CELL |

C1 and C2 are disjoint and collectively cover integer coordinates. The representatives -1 and 9 lie immediately outside the valid range, making them useful boundary probes. The value 4 represents an interior coordinate.

**Constraint:** C3=EXISTS iff C1=B2 and C2=B2. Otherwise C3=NO_CELL. This property describes actual array-cell existence; it is not taken from the possibly incorrect return value of inRange().

**Model limitation:** C3 is fully determined by C1/C2 and adds no independent test dimension. Its classification should be explained transparently; it should not be presented as additional independent coverage.

#### 4.4 Why there are nine tests

The unconstrained product is 3×3×2=18 combinations. For each of the nine row/column block pairs, exactly one C3 value is feasible. Therefore nine combinations are excluded by the cell-existence constraint, leaving:

**18 − 9 = 9 feasible test requirements.**

All nine row/column block pairs appear exactly once in the table below. ACoC requires all feasible block combinations, not every possible integer input.

#### 4.5 Concrete values, goals, and current expected outcomes

Expected values below belong to the **current characterization version**.

| ID | Blocks (C1, C2, C3) | row | col | Goal | Current expected |
|---|---|---:|---:|---|---|
| IR01 | B1, B1, NO_CELL | -1 | -1 | Check coordinate classification for this block pair | `false` |
| IR02 | B1, B2, NO_CELL | -1 | 4 | Check coordinate classification for this block pair | `false` |
| IR03 | B1, B3, NO_CELL | -1 | 9 | Check coordinate classification for this block pair | `false` |
| IR04 | B2, B1, NO_CELL | 4 | -1 | Check coordinate classification for this block pair | `false` |
| IR05 | B2, B2, EXISTS | 4 | 4 | Check coordinate classification for this block pair | `true` |
| IR06 | B2, B3, NO_CELL | 4 | 9 | Record erroneous acceptance of a coordinate equal to size | `true` |
| IR07 | B3, B1, NO_CELL | 9 | -1 | Check coordinate classification for this block pair | `false` |
| IR08 | B3, B2, NO_CELL | 9 | 4 | Record erroneous acceptance of a coordinate equal to size | `true` |
| IR09 | B3, B3, NO_CELL | 9 | 9 | Record erroneous acceptance of a coordinate equal to size | `true` |

#### 4.6 Test method mapping

| ID | JUnit test method |
|---|---|
| IR01 | `testIR01_NegativeRowNegativeColumn` |
| IR02 | `testIR02_NegativeRowValidColumn` |
| IR03 | `testIR03_NegativeRowAboveRangeColumn` |
| IR04 | `testIR04_ValidRowNegativeColumn` |
| IR05 | `testIR05_ValidRowValidColumn` |
| IR06 | `testIR06_CurrentBehaviorAcceptsColumnEqualToSize` |
| IR07 | `testIR07_AboveRangeRowNegativeColumn` |
| IR08 | `testIR08_CurrentBehaviorAcceptsRowEqualToSize` |
| IR09 | `testIR09_CurrentBehaviorAcceptsBothEqualToSize` |

IR06, IR08, and IR09 use assertTrue() only to characterize the known defect. Under the correct array-bounds contract, their expected return value remains false.

### 5. Suite 2 — getValue(row, col)

#### 5.1 Testable function and objective

```java
public String getValue(int row, int col)
```

Verify the returned content of modeled existing cells and characterize the behavior for nonexistent coordinates. Reading filled mutable and immutable cells demonstrates that both can be read; it does not test whether writes to immutable cells are prevented.

#### 5.2 Parameters, returns, and exceptional behavior

| Item | Description |
|---|---|
| row / col | int coordinates |
| Implicit inputs | Board dimensions, cell contents, and mutability state |
| Return type | String |
| Existing cell | Returns its stored value |
| Rejected coordinate | Returns `""` when inRange() returns false |
| Current boundary behavior | Throws ArrayIndexOutOfBoundsException for (4,9), (9,4), and (9,9) |
| Correctness expectation for those boundary cases | The coordinate should be rejected and `""` returned through the existing fallback |

The out-of-range fallback expectation is inferred from the method's guard and final return statement, together with the actual array bounds. The exceptions above are observed implementation defects, not a documented promise that the method should throw.

#### 5.3 Input domain model

| ID | Characteristic | Type | Blocks |
|---|---|---|---|
| C1 | Row relative to bounds | Interface-based | B1: negative (-1); B2: valid (4); B3: above range (9) |
| C2 | Column relative to bounds | Interface-based | B1: negative (-1); B2: valid (4); B3: above range (9) |
| C3 | State of the addressed cell | Functionality-based | EMPTY / PLAYER / GIVEN / NO_CELL |

| C3 block | Fixture |
|---|---|
| EMPTY | board[row][col]=`""`, mutable[row][col]=true |
| PLAYER | board[row][col]=`"5"`, mutable[row][col]=true |
| GIVEN | board[row][col]=`"7"`, mutable[row][col]=false |
| NO_CELL | Requested coordinate does not exist; do not access it during setup |

PLAYER and GIVEN are scenario labels, not stored provenance information. The fixture distinguishes filled mutable and filled immutable cells.

**Declared scope:** Initialized 9×9 boards with non-null String cell contents. Empty immutable cells are excluded from this model even though the implementation can produce them. Therefore this model is exhaustive only within its declared scope.

#### 5.4 Constraints and why there are eleven tests

- If C1=B2 and C2=B2, C3 must be EMPTY, PLAYER, or GIVEN.
- For every other coordinate pair, C3 must be NO_CELL.
- A valid coordinate cannot have NO_CELL.
- An invalid coordinate cannot have a stored EMPTY, PLAYER, or GIVEN cell.

The unconstrained product contains 3×3×4=36 combinations.

| Coordinate category | Number of coordinate block pairs | Feasible states per pair | Feasible combinations |
|---|---:|---:|---:|
| Both coordinates valid | 1 | 3 | 3 |
| At least one coordinate invalid | 8 | 1 | 8 |
| Total | 9 | — | 11 |

There are 25 infeasible combinations: one valid-coordinate/NO_CELL combination and 8×3 invalid-coordinate/stored-state combinations.

**36 − 25 = 11 feasible test requirements.**

The table below covers all eleven. The count comes from the model and constraints; it is not an arbitrary target number.

#### 5.5 Concrete values, goals, and current expected outcomes

| ID | Blocks (C1, C2) | row | col | State | Goal | Current expected |
|---|---|---:|---:|---|---|---|
| GV01 | B1, B1 | -1 | -1 | NO_CELL | Check empty-string fallback | `""` |
| GV02 | B1, B2 | -1 | 4 | NO_CELL | Check empty-string fallback | `""` |
| GV03 | B1, B3 | -1 | 9 | NO_CELL | Check empty-string fallback | `""` |
| GV04 | B2, B1 | 4 | -1 | NO_CELL | Check empty-string fallback | `""` |
| GV05 | B2, B2 | 4 | 4 | EMPTY | Read an empty mutable cell | `""` |
| GV06 | B2, B2 | 4 | 4 | PLAYER | Read a filled mutable cell | `"5"` |
| GV07 | B2, B2 | 4 | 4 | GIVEN | Read a filled immutable cell | `"7"` |
| GV08 | B2, B3 | 4 | 9 | NO_CELL | Record boundary-access exception | `ArrayIndexOutOfBoundsException` |
| GV09 | B3, B1 | 9 | -1 | NO_CELL | Check empty-string fallback | `""` |
| GV10 | B3, B2 | 9 | 4 | NO_CELL | Record boundary-access exception | `ArrayIndexOutOfBoundsException` |
| GV11 | B3, B3 | 9 | 9 | NO_CELL | Record boundary-access exception | `ArrayIndexOutOfBoundsException` |

#### 5.6 Test method mapping

| ID | JUnit test method |
|---|---|
| GV01 | `testGV01_NegativeRowNegativeColumn` |
| GV02 | `testGV02_NegativeRowValidColumn` |
| GV03 | `testGV03_NegativeRowAboveRangeColumn` |
| GV04 | `testGV04_ValidRowNegativeColumn` |
| GV05 | `testGV05_ValidPositionEmptyCell` |
| GV06 | `testGV06_ValidPositionPlayerFilledCell` |
| GV07 | `testGV07_ValidPositionGivenCell` |
| GV08 | `testGV08_CurrentBehaviorThrowsForColumnEqualToSize` |
| GV09 | `testGV09_AboveRangeRowNegativeColumn` |
| GV10 | `testGV10_CurrentBehaviorThrowsForRowEqualToSize` |
| GV11 | `testGV11_CurrentBehaviorThrowsForBothEqualToSize` |

GV08, GV10, and GV11 use:

```java
@Test(expected = ArrayIndexOutOfBoundsException.class)
```

JUnit marks these cases as passing when the call throws that exception type (or a subclass). Returning normally or throwing an unrelated exception fails the test. Each of these test bodies contains only the target call, making the expected exception's source clear.

### 6. Execution results and evidence

#### 6.1 Original correctness-oriented test version — observed log

The supplied Gradle execution log states:

```text
23 tests completed, 6 failed
BUILD FAILED
```

The six reported failing methods all belonged to SudokuACoCTest.

| Group | Executed | Passed | Failed |
|---|---:|---:|---:|
| New inRange() tests | 9 | 6 | 3 |
| New getValue() tests | 11 | 8 | 3 |
| Existing project tests | 3 | 3 | 0 |
| Total | 23 | 17 | 6 |

The new tests therefore had 14 passes and six failures. Three failures were assertion mismatches; three were unexpected ArrayIndexOutOfBoundsExceptions. Compilation and test discovery succeeded: the Gradle test task failed because tests failed.

#### 6.2 Current characterization version — confirmation status

The contributor reported that the revised version worked successfully. A detailed post-revision Gradle summary or HTML report was not supplied when this README was prepared.

The following numbers are **expected from the current code, not independently verified execution counts**:

| Run scope | Expected executed | Expected passed | Expected failed |
|---|---:|---:|---:|
| SudokuACoCTest only | 20 | 20 | 0 |
| Entire project, if it still contains only these 20 and the original 3 tests | 23 | 23 | 0 |

Before submission, attach or link the latest generated report and record the actual executed/passed/failed counts, run date, revision, and environment. If teammates have added tests, the full-project count will differ.

#### 6.3 What changed between versions

| Cases | Original expected | Current characterization expected |
|---|---|---|
| IR06, IR08, IR09 | false | true |
| GV08, GV10, GV11 | empty String | ArrayIndexOutOfBoundsException |

The production code, tested coordinates, and total number of new test methods remain unchanged. The six changes alter the test oracle, meaning the rule used to judge an outcome. They do not repair the program.

### 7. Defect report — D01: inclusive upper bounds

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



<img width="729" height="943" alt="image" src="https://github.com/user-attachments/assets/4f3a24c8-6bfe-4434-8bc1-884dafe6459e" />

## 5. ECC — Tinakome Rasripenngam

**Owner:** Tinakome Rasripenngam (Dome)  
**Numbering:** Subsection numbers below are local to this contribution.

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

Exceptional behaviour: Unlike `isSlotAvailable()`, this method does **not** call `inRange()` before accessing the array — it directly evaluates `this.mutable[row][col]`. Passing a `row` or `col` outside the board's bounds will therefore throw an uncaught `ArrayIndexOutOfBoundsException` instead of returning a boolean. This test suite focuses on the method's normal (in-range) contract; other contributions discuss invalid-coordinate behavior in other methods; they do not establish coverage of invalid inputs to this method.

#### 4. Input Domain Modeling
##### Interface-based characteristic
C1: Column Position
| Partition | Description |
|---|---|
| A1: First column | `col` is the first column of the board (`col = 0`) |
| A2: Later column | `1 ≤ col ≤ 8`, represented by `col = 1` |

##### Functionality-based characteristic
C2: Slot Mutability State
| Partition | Description |
|---|---|
| B1: Mutable | The slot's `mutable` flag is `true` |
| B2: Immutable | The slot's `mutable` flag is `false` |

#### 5. Combination Strategy (Each Choice Coverage)
Each Choice Coverage requires that every block of every characteristic be exercised by at least one test case, ; minimizing the number of tests is a design choice, not an additional coverage requirement. Since both characteristics have exactly two blocks, the two blocks of C1 and the two blocks of C2 can each be paired once, so only **2 test cases** are needed to cover all four blocks — unlike All Combinations, which would require 2×2 = 4 test cases.

#### 6. ECC Test Requirements
| Test | Column Position | Mutability State | Expected Result |
|---|---|---|---|
| T1 | A1: First column | B1: Mutable | `true` |
| T2 | A2: Later column | B2: Immutable | `false` |

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
| A1: First column | `col` is the first column of the board (`col = 0`) |
| A2: Later column | `1 ≤ col ≤ 8`, represented by `col = 2` |

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
| T1 | A1: First column | B1: Has value | `""` |
| T2 | A2: Later column | B2: Already empty | `""` |

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
<img width="751" height="444" alt="image" src="https://github.com/user-attachments/assets/27179eef-36ac-44d4-afa1-d3dfe34bbf18" />


## 6. PWC — Sunattha Boonl-or

**Owner:** Sunattha Boonl-or (Grace)  
**Numbering:** Subsection numbers below are local to this contribution.

> **Model review:** Preserve the proposed cases, but do not claim completed PWC validation yet. An out-of-range coordinate has no target cell whose content or mutability can be set. In PWC-2/T5, a stored `"5"` also does not demonstrate a conflict with input `"X"`. See Section 10 for the required reconciliation with the Java tests.

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

Exceptional behaviour: No exception is expected for the selected concrete cases. Index 9 is incorrectly accepted by the current guard and can still cause `ArrayIndexOutOfBoundsException`. The condition uses short-circuit evaluation (`inRange(row,col) && board[row][col].equals("") && isSlotMutable(row,col)`). When the position is out of range, the first condition is `false` and the board array is never accessed, so no `ArrayIndexOutOfBoundsException` occurs for positions such as `(-1, 0)`.

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
Pair-Wise Coverage requires every pair of blocks from two different characteristics to appear together in at least one test. This method has three characteristics of two blocks each, so All Combinations (ACoC) would need 2 x 2 x 2 = 8 tests. The product of the two largest block counts, 2 x 2 = 4, is a lower bound for an unconstrained pairwise design. These four abstract rows cover its pairs; their concrete feasibility is reviewed below.

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

All required label pairs appear at least once in the abstract table. This alone does not establish feasible input-model PWC coverage. In T3 and T4 the Cell Content and Mutability blocks do not affect the result because the out-of-range position short-circuits the evaluation. Those label assignments are retained from the member report but do not establish a real cell state at an invalid coordinate.

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
<img width="699" height="425" alt="image" src="https://github.com/user-attachments/assets/572d3a41-e53b-4b41-8652-4da20109fa25" />


## 7. MBCC — Wirunya Kaewthong

**Owner:** Wirunya Kaewthong (Ingeye)  
**Numbering:** Subsection numbers below are local to this contribution.

**Course:** ITCS386 Software Verification and Validation  
**Assignment:** Project 1 - Unit Testing for Open-Source Software  
**Test file:** `src/test/java/sudoku/SudokuMBCCTest.java`  
**Framework:** JUnit 4.12; the project uses Gradle

### 1. Objective and scope

This report documents the Multiple Base Choice Coverage (MBCC) tests implemented in `SudokuMBCCTest.java`. The objective is to check whether `SudokuPuzzle` correctly performs a move and searches the selected Sudoku box under systematically chosen input conditions.

The single Java file contains two method-based test groups:

| Method under test | Test identifiers | JUnit test methods |
|---|---|---:|
| `makeMove(int row, int col, String value, boolean isMutable)` | MM01-MM28 | 28 |
| `numInBox(int row, int col, String value)` | NB01-NB12 | 12 |
| **Total for this MBCC file** | | **40** |

Each `@Test` method implements one concrete scenario. Multiple assertions within a method verify different parts of that scenario; they are not counted as additional test cases. These tests form the MBCC contribution to the project. The report covers only this test file.

The production code is tested without modification. The models use a fixed 9 x 9 board with 3 x 3 boxes, valid coordinates from 0 to 8, and non-null strings stored in board cells. Additional restrictions are stated for each method. Coverage claims apply to these documented input models.

### 2. MBCC design procedure

The test design follows the input domain modelling steps in the project description:

1. Identify the testable method and its behaviour.
2. Identify its parameters, outputs, relevant state, and exceptional behaviour.
3. Define interface-based and functionality-based characteristics, their blocks, and constraints.
4. Select and justify multiple base tests.
5. For each base, change one characteristic to each of its non-base blocks while retaining the other base choices.
6. Select concrete values, define expected results, and implement the corresponding JUnit methods.

A **characteristic** is a property of the input or relevant pre-state. A **block** is a category within that characteristic. Interface-based characteristics describe parameter values, while functionality-based characteristics describe conditions relevant to the method's behaviour.

The lecture's MBCC formula counts the base tests and their one-characteristic variations:

$$
T_{\mathrm{MBCC}} = M + \sum_{i=1}^{Q} M(B_i-m_i)
                  = M\left[1+\sum_{i=1}^{Q}(B_i-m_i)\right]
$$

| Symbol | Meaning |
|---|---|
| $T_{\mathrm{MBCC}}$ | Number of generated test combinations; the final distinct-case count when they are all feasible and unique |
| $M$ | Number of complete base tests selected |
| $Q$ | Number of input characteristics in the model |
| $B_i$ | Total number of blocks for characteristic $i$ |
| $m_i$ | Number of selected base blocks for characteristic $i$ |
| $B_i-m_i$ | Number of non-base blocks to try for characteristic $i$, starting from each base test |

The first term, $M$, counts the base tests themselves. The summation counts the derived tests: each of the $M$ bases is varied through the non-base blocks of one characteristic at a time. Notice that $M$ counts **complete base scenarios**, whereas $m_i$ counts **base blocks for one characteristic**; they need not be equal.

This count must be checked for infeasible or duplicate combinations. In the two models below, all selected combinations are feasible and distinct. Every selected base block occurs in at least one base test. MBCC does not require the Cartesian product of all selected base blocks.

### 3. Common test setup

Before every test, JUnit executes `setUp()` using `@Before`:

```java
@Before
public void setUp() {
    puzzle = new SudokuPuzzle(BOARD_SIZE, BOARD_SIZE, BOX_SIZE, BOX_SIZE,
            new String[]{"1", "2", "3", "4", "5", "6", "7", "8", "9"});
}
```

`BOARD_SIZE` is 9 and `BOX_SIZE` is 3. The constructor initializes every board cell to `""` and every mutability flag to `true`. A fresh puzzle prevents state from one case affecting another; the tests do not depend on execution order.

The fixture helpers directly set `board` and `mutable` from the same `sudoku` package. This allows a test to prepare a specific pre-state without using the method being tested to construct that state. No files, connections, or other external resources are opened, so `@After` cleanup is unnecessary.

The implementation uses typed `Conflict`, `Match`, and `MoveOutcome` categories. Each test follows **Arrange - Act - Assert**: prepare the fixture, call the production method once, and compare the actual result with the expected result.

### 4. Test group 1: makeMove()

#### 4.1 Function, parameters, and expected behaviour

```java
void makeMove(int row, int col, String value, boolean isMutable)
```

| Parameter or state | Meaning |
|---|---|
| `row`, `col` | Zero-based coordinates of the target cell |
| `value` | Proposed string to store in the target cell |
| `isMutable` | Requested mutability after an accepted move |
| `board[row][col]` before the call | Existing target content |
| `mutable[row][col]` before the call | Whether the target currently permits editing |
| Other board cells | Potential conflicts in the target's row, column, or box |
| Return type | `void`; the result is observed through state changes |

An accepted move requires an allowed digit, no conflicting occurrence in the relevant row/column/box, and a currently editable target. The target is then assigned the proposed value and requested mutability. A rejected move must leave both arrays unchanged.

Current mutability and requested mutability are different properties. For example, a cell may be editable before the call but become locked after a successful call with `isMutable = false`. An editable cell containing a different digit can also be replaced; this method does not require the target to be empty.

No exception is expected for the selected cases, including a null input value. With the configured non-null valid symbols, null is rejected by value validation. Behaviour outside the selected coordinate scope is discussed in Section 8.

#### 4.2 Characteristics and blocks

| ID | Characteristic | Type | Blocks and concrete representatives | Selected base blocks |
|---|---|---|---|---|
| C1 | Row position | Interface | First: 0; interior: 1-7, represented by 4; last: 8 | Interior |
| C2 | Column position | Interface | First: 0; interior: 1-7, represented by 4; last: 8 | Interior |
| C3 | Input value category | Interface | Allowed digit: `"5"`; unsupported nonempty string: `"X"`; empty string: `""`; null: `null` | Allowed digit |
| C4 | Other-cell conflict for an allowed proposed digit | Functionality | NONE; ROW only; COLUMN only; BOX only; MULTIPLE regions | NONE |
| C5 | Target currently editable | Functionality | `true`; `false` | `true` |
| C6 | Existing target content | Functionality | Empty: `""`; different allowed digit: `"2"` | Empty |
| C7 | Requested final mutability | Interface | `true`; `false` | Both |

**Constraints and interpretation:**

- C1 and C2 partition the selected valid-coordinate domain, 0-8. Negative indices and indices 9 or greater are outside this model.
- C4 excludes the target itself. Its NONE, single-region, and multiple-region categories are mutually exclusive for an allowed candidate digit.
- For unsupported, empty, or null input values, C4 uses NONE as a neutral fixture category. Value validation is expected to reject the input before a Sudoku digit-conflict check is relevant. This does not claim that a low-level string search for `""` would find no empty cell.
- Invalid input values are not combined with ROW, COLUMN, BOX, or MULTIPLE fixtures. The generated invalid-value cases leave other cells empty.
- C6 excludes a target already containing the same allowed digit as the proposed value. An empty target remains in the Empty block even when the rejected input value is also `""`.
- The valid-digit representative is `"5"`; testing it does not independently prove correct handling of every allowed digit.

#### 4.3 Base choices and rationale

Tuple order throughout this group is:

```text
(row, col, value, conflict, currentMutable, oldValue, requestedMutable)
```

| Base | Test | Concrete tuple | Rationale |
|---|---|---|---|
| A | MM01 | `(4, 4, "5", NONE, true, "", true)` | An accepted entry that remains editable |
| B | MM15 | `(4, 4, "5", NONE, true, "", false)` | An accepted entry that becomes locked |

Both bases use a valid interior location, an allowed value, no conflict, and an editable empty target. They differ in the requested final mutability, so both boolean choices can be observed under conditions where a move should succeed.

#### 4.4 Derivation of 28 tests

| Characteristic | Total blocks `B_i` | Base blocks `m_i` | Non-base variations per base |
|---|---:|---:|---:|
| C1: row | 3 | 1 | 2 |
| C2: column | 3 | 1 | 2 |
| C3: input value | 4 | 1 | 3 |
| C4: conflict | 5 | 1 | 4 |
| C5: current mutability | 2 | 1 | 1 |
| C6: existing content | 2 | 1 | 1 |
| C7: requested mutability | 2 | 2 | 0 |
| **Total variations per base** | | | **13** |

For this model, $M=2$ and $Q=7$. Substituting the block counts from the table:

$$
\begin{aligned}
T_{\mathrm{makeMove}}
&= 2 + 2\big[(3-1)+(3-1)+(4-1)+(5-1)+(2-1)+(2-1)+(2-2)\big] \\
&= 2 + 2\big[2+2+3+4+1+1+0\big] \\
&= 2 + 2(13) \\
&= \boxed{28}
\end{aligned}
$$

Each base contributes its own base case plus 13 variations: $2\times(1+13)=28$ tests.

For example, C3 has four input-value blocks and one base block (the allowed digit). Its three non-base blocks are `"X"`, `""`, and `null`. Applying those three alternatives to both base scenarios gives $2\times(4-1)=6$ tests: MM06-MM08 and MM20-MM22.

MM02-MM14 are one-characteristic variations of MM01. MM16-MM28 are the corresponding variations of MM15. No additional C7 variation is generated because both of its blocks are already selected as base blocks. The count is a consequence of these characteristic and base choices, not an arbitrary test-count target.

#### 4.5 Fixture construction and assertions

The helper `checkMove()` prepares target content, current mutability, and any required conflict. Conflict placements isolate the intended restriction:

| Conflict fixture | Placement rule | Concrete placement for target `(4,4)` |
|---|---|---|
| NONE | No conflicting digit is inserted | No extra `"5"` |
| ROW | Same row, different box | `(4,7)` |
| COLUMN | Same column, different box | `(7,4)` |
| BOX | Same box, different row and column | `(5,5)` |
| MULTIPLE | All three placements above | `(4,7)`, `(7,4)`, and `(5,5)` |

The helper clones every row of both arrays to construct the expected state. Each test explicitly supplies `MoveOutcome.ACCEPT` or `MoveOutcome.REJECT`; the expected outcome is not obtained by calling production validation methods.

For ACCEPT, only the target value and requested target mutability are changed in the expected state. For REJECT, the expected state is identical to the pre-state. After one call to `puzzle.makeMove(...)`, `assertArrayEquals()` compares every row of both arrays. This checks the intended target change and detects unintended changes elsewhere.

`MoveOutcome` is an expected output specification; it is not an eighth input characteristic.

#### 4.6 Concrete test cases and expected results

The full tuples below specify all seven model characteristics. ACCEPT always requires every non-target cell and flag to remain unchanged. REJECT requires all cells and flags, including the target, to remain unchanged.

| ID | JUnit test method | Concrete input/pre-state tuple | Expected result |
|---|---|---|---|
| MM01 | `testMM01_Base_Editable` | `(4, 4, "5", NONE, true, "", true)` | ACCEPT: target = `"5"`; mutable = `true` |
| MM02 | `testMM02_Row_0_Editable` | `(0, 4, "5", NONE, true, "", true)` | ACCEPT: target = `"5"`; mutable = `true` |
| MM03 | `testMM03_Row_8_Editable` | `(8, 4, "5", NONE, true, "", true)` | ACCEPT: target = `"5"`; mutable = `true` |
| MM04 | `testMM04_Column_0_Editable` | `(4, 0, "5", NONE, true, "", true)` | ACCEPT: target = `"5"`; mutable = `true` |
| MM05 | `testMM05_Column_8_Editable` | `(4, 8, "5", NONE, true, "", true)` | ACCEPT: target = `"5"`; mutable = `true` |
| MM06 | `testMM06_Value_X_Editable` | `(4, 4, "X", NONE, true, "", true)` | REJECT: entire state unchanged |
| MM07 | `testMM07_Value_Empty_Editable` | `(4, 4, "", NONE, true, "", true)` | REJECT: entire state unchanged |
| MM08 | `testMM08_Value_Null_Editable` | `(4, 4, null, NONE, true, "", true)` | REJECT: entire state unchanged |
| MM09 | `testMM09_Conflict_ROW_Editable` | `(4, 4, "5", ROW, true, "", true)` | REJECT: entire state unchanged |
| MM10 | `testMM10_Conflict_COLUMN_Editable` | `(4, 4, "5", COLUMN, true, "", true)` | REJECT: entire state unchanged |
| MM11 | `testMM11_Conflict_BOX_Editable` | `(4, 4, "5", BOX, true, "", true)` | REJECT: entire state unchanged |
| MM12 | `testMM12_Conflict_MULTIPLE_Editable` | `(4, 4, "5", MULTIPLE, true, "", true)` | REJECT: entire state unchanged |
| MM13 | `testMM13_CurrentMutable_False_Editable` | `(4, 4, "5", NONE, false, "", true)` | REJECT: entire state unchanged |
| MM14 | `testMM14_ExistingValue_2_Editable` | `(4, 4, "5", NONE, true, "2", true)` | ACCEPT: target = `"5"`; mutable = `true` |
| MM15 | `testMM15_Base_Locked` | `(4, 4, "5", NONE, true, "", false)` | ACCEPT: target = `"5"`; mutable = `false` |
| MM16 | `testMM16_Row_0_Locked` | `(0, 4, "5", NONE, true, "", false)` | ACCEPT: target = `"5"`; mutable = `false` |
| MM17 | `testMM17_Row_8_Locked` | `(8, 4, "5", NONE, true, "", false)` | ACCEPT: target = `"5"`; mutable = `false` |
| MM18 | `testMM18_Column_0_Locked` | `(4, 0, "5", NONE, true, "", false)` | ACCEPT: target = `"5"`; mutable = `false` |
| MM19 | `testMM19_Column_8_Locked` | `(4, 8, "5", NONE, true, "", false)` | ACCEPT: target = `"5"`; mutable = `false` |
| MM20 | `testMM20_Value_X_Locked` | `(4, 4, "X", NONE, true, "", false)` | REJECT: entire state unchanged |
| MM21 | `testMM21_Value_Empty_Locked` | `(4, 4, "", NONE, true, "", false)` | REJECT: entire state unchanged |
| MM22 | `testMM22_Value_Null_Locked` | `(4, 4, null, NONE, true, "", false)` | REJECT: entire state unchanged |
| MM23 | `testMM23_Conflict_ROW_Locked` | `(4, 4, "5", ROW, true, "", false)` | REJECT: entire state unchanged |
| MM24 | `testMM24_Conflict_COLUMN_Locked` | `(4, 4, "5", COLUMN, true, "", false)` | REJECT: entire state unchanged |
| MM25 | `testMM25_Conflict_BOX_Locked` | `(4, 4, "5", BOX, true, "", false)` | REJECT: entire state unchanged |
| MM26 | `testMM26_Conflict_MULTIPLE_Locked` | `(4, 4, "5", MULTIPLE, true, "", false)` | REJECT: entire state unchanged |
| MM27 | `testMM27_CurrentMutable_False_Locked` | `(4, 4, "5", NONE, false, "", false)` | REJECT: entire state unchanged |
| MM28 | `testMM28_ExistingValue_2_Locked` | `(4, 4, "5", NONE, true, "2", false)` | ACCEPT: target = `"5"`; mutable = `false` |

The following mapping states the goal of every case. Each pair exercises the same input variation with the two different requested-mutability base choices.

| Base A case | Base B case | Test goal |
|---|---|---|
| MM01 | MM15 | Accept a normal entry and apply the requested final mutability. |
| MM02 | MM16 | Accept an entry in the first valid row. |
| MM03 | MM17 | Accept an entry in the last valid row. |
| MM04 | MM18 | Accept an entry in the first valid column. |
| MM05 | MM19 | Accept an entry in the last valid column. |
| MM06 | MM20 | Reject an unsupported nonempty value. |
| MM07 | MM21 | Reject an empty input value. |
| MM08 | MM22 | Reject a null input value without changing state. |
| MM09 | MM23 | Reject a value already present in the same row only. |
| MM10 | MM24 | Reject a value already present in the same column only. |
| MM11 | MM25 | Reject a value already present in the same box only. |
| MM12 | MM26 | Reject simultaneous row, column and box conflicts. |
| MM13 | MM27 | Reject a move into a currently locked target. |
| MM14 | MM28 | Replace a different existing digit in an editable target. |

### 5. Test group 2: numInBox()

#### 5.1 Function, parameters, and expected behaviour

```java
boolean numInBox(int row, int col, String value)
```

| Parameter or result | Meaning |
|---|---|
| `row`, `col` | Coordinates used to select the containing 3 x 3 box |
| `value` | String to search for; fixed to `"5"` in this model |
| `true` | At least one matching value exists in the selected box |
| `false` | No matching value exists in the selected box |
| State after the call | Board contents and mutable flags must remain unchanged |

The queried cell does not have to contain the searched digit. The method searches the entire containing box. It is a search operation, not a move validator: it does not itself check whether the value is an allowed move or whether a cell is mutable.

No exception is expected in the selected valid-coordinate cases.

#### 5.2 Characteristics, blocks, and scope

The model fixes the searched value to `"5"`, queries each selected box at its centre, and allows at most one occurrence of `"5"` on the board. All other cells are empty.

| ID | Characteristic | Type | Blocks and representatives | Selected base blocks |
|---|---|---|---|---|
| D1 | Row's box band | Interface | Top: rows 0-2, query row 1; middle: rows 3-5, query row 4; bottom: rows 6-8, query row 7 | Top, bottom |
| D2 | Column's box band | Interface | Left: columns 0-2, query column 1; centre: columns 3-5, query column 4; right: columns 6-8, query column 7 | Left, right |
| D3 | Match location relative to the selected box | Functionality | FIRST; MIDDLE; LAST; OUTSIDE; ABSENT | FIRST, LAST |

D3 is defined as follows:

| Block | Definition | Representative |
|---|---|---|
| FIRST | The match is at the first position in the box's row-major scan | Top-left cell |
| MIDDLE | The match is at one of the seven positions between the first and last scan positions | Centre cell |
| LAST | The match is at the last position in the scan | Bottom-right cell |
| OUTSIDE | The sole matching value is outside the selected box | A cell in the next box-column, wrapping around within the same three-row band |
| ABSENT | There is no matching value anywhere on the board | Entire board remains empty |

These blocks are disjoint and cover the declared model. Multiple occurrences of the searched digit, other search values, and non-centre query positions are outside this model.

#### 5.3 Base choices and rationale

| Base | Test | D1, D2, D3 | Query | Match location | Expected result |
|---|---|---|---|---|---|
| A | NB01 | Top, left, FIRST | `(1,1,"5")` | `(0,0)` | `true` |
| B | NB07 | Bottom, right, LAST | `(7,7,"5")` | `(8,8)` | `true` |

These bases exercise opposite board regions and both endpoints of the box scan. Every selected base block appears at least once. The two bases do not need to include every combination of top/bottom, left/right, and first/last.

#### 5.4 Derivation of 12 tests

| Characteristic | Total blocks `B_i` | Base blocks `m_i` | Non-base variations per base |
|---|---:|---:|---:|
| D1: row band | 3 | 2 | 1: middle |
| D2: column band | 3 | 2 | 1: centre |
| D3: match location | 5 | 2 | 3: MIDDLE, OUTSIDE, ABSENT |
| **Total variations per base** | | | **5** |

For this model, $M=2$ and $Q=3$. Substituting the block counts:

$$
\begin{aligned}
T_{\mathrm{numInBox}}
&= 2 + 2\big[(3-2)+(3-2)+(5-2)\big] \\
&= 2 + 2\big[1+1+3\big] \\
&= 2 + 2(5) \\
&= \boxed{12}
\end{aligned}
$$

Each base contributes its own base case plus five variations: $2\times(1+5)=12$ tests.

For example, D3 has five match-location blocks. FIRST and LAST are already base blocks, leaving MIDDLE, OUTSIDE, and ABSENT as its three non-base blocks. Applying those alternatives to both bases gives $2\times(5-2)=6$ tests: NB04-NB06 and NB10-NB12.

NB02-NB06 each change one characteristic of NB01. NB08-NB12 each change one characteristic of NB07. The expected boolean may also change, but it is an output and is not counted as a changed input characteristic.

A combination with both the row band and column band changed to middle/centre is not selected: it would change two characteristics from either base. MBCC therefore does not require all nine box locations in this design.

#### 5.5 Fixture construction and assertions

The helper `checkBox(rowBand, colBand, match, expected)` receives box-band indices 0, 1, or 2. These are not direct board-cell coordinates. It calculates:

```text
firstRow = rowBand x 3
firstCol = colBand x 3
query row = firstRow + 1
query column = firstCol + 1
```

It places `"5"` according to the selected match category and snapshots both arrays. It then calls `numInBox(queryRow, queryColumn, "5")` once. `assertEquals()` checks the expected boolean, and `assertArrayEquals()` checks that every row of the board and mutable arrays remains unchanged.

#### 5.6 Concrete test cases, goals, and expected results

For every case, all cells except the listed match location contain `""`, and all mutable flags start as `true`. The query value is always `"5"`. Every case also checks that no state changes occur.

| ID | JUnit test method | Query `(row,col,value)` | Match fixture | Expected result and goal |
|---|---|---|---|---|
| NB01 | `testNB01_Base_FIRST` | `(1,1,"5")` | FIRST: (0,0) | `true`; find the first scan position |
| NB02 | `testNB02_RowBand_FIRST` | `(4,1,"5")` | FIRST: (3,0) | `true`; find the first scan position |
| NB03 | `testNB03_ColumnBand_FIRST` | `(1,4,"5")` | FIRST: (0,3) | `true`; find the first scan position |
| NB04 | `testNB04_Match_MIDDLE` | `(1,1,"5")` | MIDDLE: (1,1) | `true`; find an interior scan position |
| NB05 | `testNB05_Match_OUTSIDE` | `(1,1,"5")` | OUTSIDE: (0,3) | `false`; ignore a match outside the selected box |
| NB06 | `testNB06_Match_ABSENT` | `(1,1,"5")` | ABSENT: none anywhere | `false`; report absence when no match exists |
| NB07 | `testNB07_Base_LAST` | `(7,7,"5")` | LAST: (8,8) | `true`; find the last scan position |
| NB08 | `testNB08_RowBand_LAST` | `(4,7,"5")` | LAST: (5,8) | `true`; find the last scan position |
| NB09 | `testNB09_ColumnBand_LAST` | `(7,4,"5")` | LAST: (8,5) | `true`; find the last scan position |
| NB10 | `testNB10_Match_MIDDLE` | `(7,7,"5")` | MIDDLE: (7,7) | `true`; find an interior scan position |
| NB11 | `testNB11_Match_OUTSIDE` | `(7,7,"5")` | OUTSIDE: (6,0) | `false`; ignore a match outside the selected box |
| NB12 | `testNB12_Match_ABSENT` | `(7,7,"5")` | ABSENT: none anywhere | `false`; report absence when no match exists |

Combining the two method groups gives the number of JUnit tests in the single MBCC file:

$$
T_{\mathrm{file}} = T_{\mathrm{makeMove}} + T_{\mathrm{numInBox}}
                 = 28 + 12 = \boxed{40}
$$

### 6. Automated execution and results

The class was compiled and executed using **JUnit 4.12**. All 40 MBCC test methods passed in the recorded verification run. The table reports only the tests belonging to `SudokuMBCCTest.java`.

| MBCC test group | Executed | Passed | Failed |
|---|---:|---:|---:|
| makeMove: MM01-MM28 | 28 | 28 | 0 |
| numInBox: NB01-NB12 | 12 | 12 | 0 |
| **Total** | **40** | **40** | **0** |

<img width="667" height="915" alt="image" src="https://github.com/user-attachments/assets/120c6c6f-77a8-4956-b775-16ec15d6caed" />


**Verification date:** 20 September 2026. Compilation used OpenJDK 17.0.20 with Java 8 target compatibility (`--release 8`) and produced no compiler diagnostics. The recorded verification used the JUnit runner directly; these results are not presented as a verified Gradle run. A successful Gradle report from the submission environment should accompany the required build-framework demonstration.

The tests passed for the selected inputs and expected outcomes. This does not establish correct behaviour for inputs outside the documented models.

#### Running only the MBCC class through Gradle

Place the file in `src/test/java/sudoku/` and ensure the filename is exactly `SudokuMBCCTest.java`, matching its public class name. Run the command from the project directory containing `build.gradle` and the Gradle wrapper.

Windows PowerShell:

```powershell
.\gradlew.bat test --tests "sudoku.SudokuMBCCTest"
```

macOS/Linux:

```bash
bash gradlew test --tests "sudoku.SudokuMBCCTest"
```

The filtered run selects the 40 methods in this MBCC class. The Gradle HTML test report is generated at:

```text
build/reports/tests/test/index.html
```

Use a JDK compatible with the project's Gradle wrapper. A direct JUnit verification under Java 17 does not establish that the supplied Gradle 5.2.1 wrapper can run under Java 17. If using IntelliJ for the demonstration, configure it to run tests through Gradle.

### 7. Interpretation of the results

The passing makeMove cases confirm the expected state transitions for the selected accepted moves, including both requested mutability values and replacement of a different existing digit. The rejected cases verify that unsupported values, selected conflicts, and locked targets leave the state unchanged.

The passing numInBox cases confirm that the selected matches can be found at the beginning, interior, and end of a box scan, while an outside match or complete absence produces `false`. Every search case also verifies that the method is read-only.

For the defined models, the implemented cases satisfy the MBCC requirements: 28 distinct makeMove combinations and 12 distinct numInBox combinations. This input-model coverage should not be reported as 100% statement coverage, 100% branch coverage, or proof that the software has no defects.

### 8. Limitations and known boundary behaviour

The following inputs or states are outside the two MBCC models:

- Negative coordinates or coordinates greater than 8.
- Board sizes other than 9 x 9 or box sizes other than 3 x 3.
- Malformed boards, including null stored cell strings.
- A makeMove target already containing the same proposed allowed digit.
- numInBox searches using other values, multiple matching occurrences, or non-centre query cells.
- Combinations involving simultaneous non-base changes that are not selected by the stated MBCC construction.

The production `inRange()` method uses `row <= ROWS` and `col <= COLUMNS`. On a 9 x 9 board this incorrectly accepts index 9, although the last valid index is 8. Separate diagnostic calls to `makeMove(4,9,"5",true)` and `numInBox(4,9,"5")` produced `ArrayIndexOutOfBoundsException`.

Those diagnostic calls are **not part of the 40 MBCC tests** and are not included in the pass-count table. They show why the valid-coordinate scope must be stated explicitly. The production defect was not fixed or hidden by changing the expected outcomes of the MBCC cases.

### 9. References

1. **ITCS386 Project Assignment 1: Unit Test for Open-Source Software Projects**, supplied project description, pages 1-4. Requirements for input domain modelling, JUnit implementation, README documentation, and execution using the existing build framework.
2. **Week 4, Module 6: Input Space Partitioning 2**, supplied lecture (`W4-Module6-Input_Space_Partitioning_2_Student(1).pdf`), pages 28-29. MBCC definition, base selection, and test-count formula.
3. The project's **SudokuPuzzle.java** implementation and the accompanying **SudokuMBCCTest.java** test class. Concrete interfaces, fixtures, assertions, and method-name traceability.

## 8. BCC — Piyada Chalermnontakarn

**Owner:** Piyada Chalermnontakarn (Nudee)  
**Numbering:** Subsection numbers below are local to this contribution.

> **Scope review:** The invalid-coordinate rows test rejection before a target cell is accessed. Their cell-state/conflict labels need a neutral-fixture or not-applicable interpretation. The supplied report also omits the exact conflict fixture for BCC-1/T4. See Section 10.

### BCC-1: isValidMove()
#### 1.Testable Function
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

#### 6. BCC Test Cases
| Test | Row Position | Column Position | Slot State | Expected Result |
|---|---|---|---|---|
| T1 (Base) | A1: Valid | B1: Valid | C1: Available | `true` |
| T2 | A2: Invalid | B1: Valid | C1: Available | `false` |
| T3 | A1: Valid | B2: Invalid | C1: Available | `false` |
| T4 | A1: Valid | B1: Valid | C2: Unavailable | `false` |

#### 7. Test Values
The test values are derived from the BCC test requirements and the behavior of the `SudokuPuzzle` class. The test fixture uses a 9×9 board where the slots are initialized as empty (`""`) and mutable. For T4, the slot at `(0,2)` is set to `"8"` to represent an unavailable slot.
| Test | `row` | `col` | Slot State | Expected Result |
|---|---:|---:|---|---|
| T1 (Base) | `0` | `0` | Available | `true` |
| T2 | `-1` | `0` | Available | `false` |
| T3 | `0` | `-1` | Available | `false` |
| T4 | `0` | `2` | Unavailable | `false` |

<img width="706" height="614" alt="image" src="https://github.com/user-attachments/assets/c6208fa8-f8f3-494e-8073-8b0e876963e2" />


## 9. Consolidated results and known defect

### 9.1 What the supplied evidence establishes

| Contribution | Designed cases | Execution evidence supplied in member report | Combined-run status |
|---|---:|---|---|
| ACoC | 20 | Historical correctness version: 14 new cases passed, 6 failed. Contributor reports success after changing six characterization expectations; no detailed revised summary supplied. | Revised results need final Gradle evidence |
| ECC | 4 | Design tables and expected results only | Actual outcome not supplied |
| PWC | 9 | Design tables and expected results only | Actual outcome not supplied; model review outstanding |
| MBCC | 40 | Member reports 40 passed, 0 failed on 20 September 2026 using a direct JUnit runner | A Gradle run remains to be evidenced |
| BCC | 8 | Design tables and expected results only | Actual outcome not supplied |
| **Total** | **81** | **No single combined execution report supplied** | **Do not report 81 passes as an observed result** |

If all 81 designed scenarios are implemented as separate discovered JUnit methods, and the three original tests remain, the anticipated complete-run count is **84 tests**. This is conditional: test grouping, missing implementations, additional tests, or revisions can change the count. The final Gradle report determines the actual total.

Record the final run here after execution:

| Evidence field | Final value |
|---|---|
| Tested commit | Not yet recorded |
| Run date and time | Not yet recorded |
| JDK and Gradle versions | Not yet recorded |
| Full execution command | `gradlew.bat clean test` or `bash gradlew clean test` |
| Executed / passed / failed / skipped | Not yet recorded |
| Saved report or screenshot location | Not yet recorded |

### 9.2 D01 — Inclusive upper bounds

`SudokuPuzzle.inRange()` uses `row <= ROWS` and `col <= COLUMNS`. On a 9×9 board, valid indices are 0–8. Accepting index 9 can lead to an out-of-bounds array access in methods that trust this guard.

ACoC documents incorrect `true` results for `(4,9)`, `(9,4)`, and `(9,9)`, followed by exceptions when those coordinates are used with `getValue()`. These are manifestations of one root defect, not six independent defects. The MBCC report additionally records diagnostic exceptions for `makeMove(4,9,"5",true)` and `numInBox(4,9,"5")`, outside its 40 counted tests.

**Disposition:** Production code remains unchanged. ACoC's current boundary tests characterize the observed defect with explicit expectations. The distinction between intended correctness and current behavior must remain visible in the presentation.

## 10. Integration review and submission checklist

### 10.1 Items to reconcile before submission

The following observations come from combining the reports. They do not change the supplied test inputs or assert that new code has been implemented.

| Item | Evidence and implication | Required follow-up |
|---|---|---|
| Existing-test overlap | MBCC-2 targets `numInBox()`, which the earlier project review identifies as already tested. Same-method testing may add new coverage, but duplicate scenarios do not meet the assignment. | Compare every proposed NB case against the original tests and document its additional purpose; replace duplicated scenarios if necessary. |
| Cross-member overlap | PWC and MBCC both test `makeMove()`; PWC and BCC both test `isSlotAvailable()`. Some normal acceptance/rejection scenarios may overlap. | Compare concrete fixtures and assertions. Explain distinct requirements and eliminate exact duplicates. |
| PWC-1 feasibility | T3/T4 describe content and mutability at nonexistent target coordinates. Abstract label pairs are present, but those target states cannot be instantiated. | Define constrained blocks such as NO_CELL/not applicable, or explicitly model independently prepared reference-cell state. Re-derive feasible pairs and synchronize the Java tests and report. |
| PWC-2 fixtures | T3/T5 have no target cell. T5 proposes `"X"` but its listed conflict fixture contains `"5"`; this is not a matching-value conflict. | Correct the input model and concrete fixtures together. Retain honest short-circuit rejection tests without claiming that uninstantiated conflict blocks are covered. |
| PWC-2 missing argument | Concrete tables do not specify the `isMutable` argument, although it is part of the method signature. Checking only `(0,0)` also does not prove the entire board was unchanged. | Copy the actual boolean argument and assertions from each Java test into the report. State precisely which state changes are checked. |
| BCC-1 fixture | T4 expects a conflict with `"8"`, but the report does not identify where that value is placed. | Document the exact pre-state from the Java test. `isValidMove()` checks conflicts and coordinates; it does not itself validate membership in VALIDVALUES. |
| BCC model constraints | Cell-state and conflict labels are undefined for nonexistent targets. BCC-2's available/unavailable blocks omit empty immutable cells. | Declare the restricted fixture scope and neutral/not-applicable interpretation; avoid claiming exhaustive coverage of all possible states. |
| Case-name traceability | ECC, PWC, and BCC provide local T identifiers but no exact JUnit method names. | Add the actual class and method names, and a one-sentence goal per case, from the implemented tests. Do not invent names in the report. |
| ACoC model limits | Cell existence is derived from coordinates. The above-range block includes both 9 and larger values, although the buggy implementation behaves differently at 9 and 10. | Keep the boundary representative and explain that full block-combination coverage does not prove uniform behavior throughout each block. |
| Final execution | The individual reports do not establish one successful full-team Gradle run. | Run the complete test set through Gradle and fill Section 9.1 with observed results. |
