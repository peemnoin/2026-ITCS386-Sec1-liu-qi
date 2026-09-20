# 2026-ITCS386-Sec1-liu-qi
# Multiple Base Choice Coverage (MBCC) for SudokuPuzzle

**Course:** ITCS386 Software Verification and Validation  
**Assignment:** Project 1 - Unit Testing for Open-Source Software  
**Test file:** `src/test/java/sudoku/SudokuMBCCTest.java`  
**Framework:** JUnit 4.12; the project uses Gradle

## 1. Objective and scope

This report documents the Multiple Base Choice Coverage (MBCC) tests implemented in `SudokuMBCCTest.java`. The objective is to check whether `SudokuPuzzle` correctly performs a move and searches the selected Sudoku box under systematically chosen input conditions.

The single Java file contains two method-based test groups:

| Method under test | Test identifiers | JUnit test methods |
|---|---|---:|
| `makeMove(int row, int col, String value, boolean isMutable)` | MM01-MM28 | 28 |
| `numInBox(int row, int col, String value)` | NB01-NB12 | 12 |
| **Total for this MBCC file** | | **40** |

Each `@Test` method implements one concrete scenario. Multiple assertions within a method verify different parts of that scenario; they are not counted as additional test cases. These tests form the MBCC contribution to the project. The report covers only this test file.

The production code is tested without modification. The models use a fixed 9 x 9 board with 3 x 3 boxes, valid coordinates from 0 to 8, and non-null strings stored in board cells. Additional restrictions are stated for each method. Coverage claims apply to these documented input models.

## 2. MBCC design procedure

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

## 3. Common test setup

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

## 4. Test group 1: makeMove()

### 4.1 Function, parameters, and expected behaviour

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

### 4.2 Characteristics and blocks

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

### 4.3 Base choices and rationale

Tuple order throughout this group is:

```text
(row, col, value, conflict, currentMutable, oldValue, requestedMutable)
```

| Base | Test | Concrete tuple | Rationale |
|---|---|---|---|
| A | MM01 | `(4, 4, "5", NONE, true, "", true)` | An accepted entry that remains editable |
| B | MM15 | `(4, 4, "5", NONE, true, "", false)` | An accepted entry that becomes locked |

Both bases use a valid interior location, an allowed value, no conflict, and an editable empty target. They differ in the requested final mutability, so both boolean choices can be observed under conditions where a move should succeed.

### 4.4 Derivation of 28 tests

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

### 4.5 Fixture construction and assertions

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

### 4.6 Concrete test cases and expected results

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

## 5. Test group 2: numInBox()

### 5.1 Function, parameters, and expected behaviour

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

### 5.2 Characteristics, blocks, and scope

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

### 5.3 Base choices and rationale

| Base | Test | D1, D2, D3 | Query | Match location | Expected result |
|---|---|---|---|---|---|
| A | NB01 | Top, left, FIRST | `(1,1,"5")` | `(0,0)` | `true` |
| B | NB07 | Bottom, right, LAST | `(7,7,"5")` | `(8,8)` | `true` |

These bases exercise opposite board regions and both endpoints of the box scan. Every selected base block appears at least once. The two bases do not need to include every combination of top/bottom, left/right, and first/last.

### 5.4 Derivation of 12 tests

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

### 5.5 Fixture construction and assertions

The helper `checkBox(rowBand, colBand, match, expected)` receives box-band indices 0, 1, or 2. These are not direct board-cell coordinates. It calculates:

```text
firstRow = rowBand x 3
firstCol = colBand x 3
query row = firstRow + 1
query column = firstCol + 1
```

It places `"5"` according to the selected match category and snapshots both arrays. It then calls `numInBox(queryRow, queryColumn, "5")` once. `assertEquals()` checks the expected boolean, and `assertArrayEquals()` checks that every row of the board and mutable arrays remains unchanged.

### 5.6 Concrete test cases, goals, and expected results

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

## 6. Automated execution and results

The class was compiled and executed using **JUnit 4.12**. All 40 MBCC test methods passed in the recorded verification run. The table reports only the tests belonging to `SudokuMBCCTest.java`.

| MBCC test group | Executed | Passed | Failed |
|---|---:|---:|---:|
| makeMove: MM01-MM28 | 28 | 28 | 0 |
| numInBox: NB01-NB12 | 12 | 12 | 0 |
| **Total** | **40** | **40** | **0** |

**Verification date:** 20 September 2026. Compilation used OpenJDK 17.0.20 with Java 8 target compatibility (`--release 8`) and produced no compiler diagnostics. The recorded verification used the JUnit runner directly; these results are not presented as a verified Gradle run. A successful Gradle report from the submission environment should accompany the required build-framework demonstration.

The tests passed for the selected inputs and expected outcomes. This does not establish correct behaviour for inputs outside the documented models.

### Running only the MBCC class through Gradle

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

## 7. Interpretation of the results

The passing makeMove cases confirm the expected state transitions for the selected accepted moves, including both requested mutability values and replacement of a different existing digit. The rejected cases verify that unsupported values, selected conflicts, and locked targets leave the state unchanged.

The passing numInBox cases confirm that the selected matches can be found at the beginning, interior, and end of a box scan, while an outside match or complete absence produces `false`. Every search case also verifies that the method is read-only.

For the defined models, the implemented cases satisfy the MBCC requirements: 28 distinct makeMove combinations and 12 distinct numInBox combinations. This input-model coverage should not be reported as 100% statement coverage, 100% branch coverage, or proof that the software has no defects.

## 8. Limitations and known boundary behaviour

The following inputs or states are outside the two MBCC models:

- Negative coordinates or coordinates greater than 8.
- Board sizes other than 9 x 9 or box sizes other than 3 x 3.
- Malformed boards, including null stored cell strings.
- A makeMove target already containing the same proposed allowed digit.
- numInBox searches using other values, multiple matching occurrences, or non-centre query cells.
- Combinations involving simultaneous non-base changes that are not selected by the stated MBCC construction.

The production `inRange()` method uses `row <= ROWS` and `col <= COLUMNS`. On a 9 x 9 board this incorrectly accepts index 9, although the last valid index is 8. Separate diagnostic calls to `makeMove(4,9,"5",true)` and `numInBox(4,9,"5")` produced `ArrayIndexOutOfBoundsException`.

Those diagnostic calls are **not part of the 40 MBCC tests** and are not included in the pass-count table. They show why the valid-coordinate scope must be stated explicitly. The production defect was not fixed or hidden by changing the expected outcomes of the MBCC cases.

## 9. References

1. **ITCS386 Project Assignment 1: Unit Test for Open-Source Software Projects**, supplied project description, pages 1-4. Requirements for input domain modelling, JUnit implementation, README documentation, and execution using the existing build framework.
2. **Week 4, Module 6: Input Space Partitioning 2**, supplied lecture (`W4-Module6-Input_Space_Partitioning_2_Student(1).pdf`), pages 28-29. MBCC definition, base selection, and test-count formula.
3. The project's **SudokuPuzzle.java** implementation and the accompanying **SudokuMBCCTest.java** test class. Concrete interfaces, fixtures, assertions, and method-name traceability.
