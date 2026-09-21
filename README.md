# 2026-ITCS386-Sec1-liu-qi
# ITCS386 Project 1 — ACoC Test Report
**Contributor:** Veerakron No-in  
**Team:** liu-qi  
**Production class:** `sudoku.SudokuPuzzle`  
**Test class:** `sudoku.SudokuACoCTest`  
**Scope:** Two logical test suites: `inRange()` and `getValue()`.

> This report covers this contributor's two suites, not the entire team's ten-suite submission. It can be incorporated into the team's README.md. The original production code is not modified.

## 1. Purpose and test strategy

The tests apply Input Space Partitioning (ISP) and All Combinations Coverage (ACoC) to select concrete input combinations.

The first test version used correctness expectations: coordinates outside a 9×9 board should be rejected, and getValue() should return an empty string for coordinates rejected as out of range. Its execution exposed six failures.

The current version is a **characterization test suite**: it checks the observed behavior of the original implementation, including its known boundary defect. Six expected outcomes were changed; the inputs and number of test cases were not changed. A passing characterization test is not evidence that the boundary behavior is correct.

## 2. Test environment and execution

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

## 3. Shared fixture and test isolation

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

## 4. Suite 1 — inRange(row, col)

### 4.1 Testable function and objective

```java
public boolean inRange(int row, int col)
```

Check the return value for all combinations of the modeled row and column categories. The current version explicitly records the original implementation's acceptance of coordinates equal to the board size.

### 4.2 Parameters, returns, and exceptional behavior

| Item | Description |
|---|---|
| row | int: requested row index |
| col | int: requested column index |
| Implicit input | Initialized board with ROWS=9 and COLUMNS=9 |
| Return type | boolean |
| Correct bounds behavior | true iff 0 ≤ row < 9 and 0 ≤ col < 9 |
| Current implementation | true iff 0 ≤ row ≤ 9 and 0 ≤ col ≤ 9 |
| Exception for modeled cases | None expected; this method only compares integers |

### 4.3 Input domain model

| ID | Characteristic | Type | Blocks and representatives |
|---|---|---|---|
| C1 | Row relative to array bounds | Interface-based | B1: row < 0 → -1; B2: 0 ≤ row < 9 → 4; B3: row ≥ 9 → 9 |
| C2 | Column relative to array bounds | Interface-based | B1: col < 0 → -1; B2: 0 ≤ col < 9 → 4; B3: col ≥ 9 → 9 |
| C3 | Coordinate identifies an existing board cell | Functionality-based, derived | EXISTS / NO_CELL |

C1 and C2 are disjoint and collectively cover integer coordinates. The representatives -1 and 9 lie immediately outside the valid range, making them useful boundary probes. The value 4 represents an interior coordinate.

**Constraint:** C3=EXISTS iff C1=B2 and C2=B2. Otherwise C3=NO_CELL. This property describes actual array-cell existence; it is not taken from the possibly incorrect return value of inRange().

**Model limitation:** C3 is fully determined by C1/C2 and adds no independent test dimension. Its classification should be explained transparently; it should not be presented as additional independent coverage.

### 4.4 Why there are nine tests

The unconstrained product is 3×3×2=18 combinations. For each of the nine row/column block pairs, exactly one C3 value is feasible. Therefore nine combinations are excluded by the cell-existence constraint, leaving:

**18 − 9 = 9 feasible test requirements.**

All nine row/column block pairs appear exactly once in the table below. ACoC requires all feasible block combinations, not every possible integer input.

### 4.5 Concrete values, goals, and current expected outcomes

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

### 4.6 Test method mapping

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

## 5. Suite 2 — getValue(row, col)

### 5.1 Testable function and objective

```java
public String getValue(int row, int col)
```

Verify the returned content of modeled existing cells and characterize the behavior for nonexistent coordinates. Reading filled mutable and immutable cells demonstrates that both can be read; it does not test whether writes to immutable cells are prevented.

### 5.2 Parameters, returns, and exceptional behavior

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

### 5.3 Input domain model

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

### 5.4 Constraints and why there are eleven tests

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

### 5.5 Concrete values, goals, and current expected outcomes

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

### 5.6 Test method mapping

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

## 6. Execution results and evidence

### 6.1 Original correctness-oriented test version — observed log

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

### 6.2 Current characterization version — confirmation status

The contributor reported that the revised version worked successfully. A detailed post-revision Gradle summary or HTML report was not supplied when this README was prepared.

The following numbers are **expected from the current code, not independently verified execution counts**:

| Run scope | Expected executed | Expected passed | Expected failed |
|---|---:|---:|---:|
| SudokuACoCTest only | 20 | 20 | 0 |
| Entire project, if it still contains only these 20 and the original 3 tests | 23 | 23 | 0 |

Before submission, attach or link the latest generated report and record the actual executed/passed/failed counts, run date, revision, and environment. If teammates have added tests, the full-project count will differ.

### 6.3 What changed between versions

| Cases | Original expected | Current characterization expected |
|---|---|---|
| IR06, IR08, IR09 | false | true |
| GV08, GV10, GV11 | empty String | ArrayIndexOutOfBoundsException |

The production code, tested coordinates, and total number of new test methods remain unchanged. The six changes alter the test oracle, meaning the rule used to judge an outcome. They do not repair the program.

## 7. Defect report — D01: inclusive upper bounds

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

