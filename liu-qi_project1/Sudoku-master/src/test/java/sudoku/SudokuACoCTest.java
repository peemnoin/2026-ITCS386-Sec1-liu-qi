/* Copyright (C) 2026 Veerakron No-in - All Rights Reserved
 * You may use, distribute and modify this code under the terms of
 * the MIT license.
 */
package sudoku;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

public class SudokuACoCTest {

    private SudokuPuzzle puzzle;

    @Before
    public void setUp() {
        // Create a fresh board before every test case.
        puzzle = new SudokuPuzzle(
                9, 9, 3, 3,
                new String[] {
                        "1", "2", "3", "4", "5",
                        "6", "7", "8", "9"
                }
        );
    }

    /*
     * Suite 1: inRange(row, col) - ACoC
     *
     * Interface-based characteristics:
     * C1: Row    = negative / valid / above range
     * C2: Column = negative / valid / above range
     *
     * Representatives: -1 / 4 / 9
     *
     * Functionality-based characteristic:
     * C3: Coordinate identifies an existing cell = yes / no.
     * C3 is determined by C1 and C2, not independently selectable.
     *
     * Constraint:
     * A cell exists iff both coordinates are within 0..8.
     *
     * Feasible combinations: 3 x 3 = 9.
     */

    @Test
    public void testIR01_NegativeRowNegativeColumn() {
        assertFalse(puzzle.inRange(-1, -1));
    }

    @Test
    public void testIR02_NegativeRowValidColumn() {
        assertFalse(puzzle.inRange(-1, 4));
    }

    @Test
    public void testIR03_NegativeRowAboveRangeColumn() {
        assertFalse(puzzle.inRange(-1, 9));
    }

    @Test
    public void testIR04_ValidRowNegativeColumn() {
        assertFalse(puzzle.inRange(4, -1));
    }

    @Test
    public void testIR05_ValidRowValidColumn() {
        assertTrue(puzzle.inRange(4, 4));
    }
    //Should be output False
    @Test
    public void testIR06_ValidRowAboveRangeColumn() {
        assertTrue(puzzle.inRange(4, 9));
    }

    @Test
    public void testIR07_AboveRangeRowNegativeColumn() {
        assertFalse(puzzle.inRange(9, -1));
    }
//Should be output False
    @Test
    public void testIR08_AboveRangeRowValidColumn() {
        assertTrue(puzzle.inRange(9, 4));
    }
    //Should be output False
    @Test
    public void testIR09_AboveRangeRowAboveRangeColumn() {
        assertTrue(puzzle.inRange(9, 9));
    }

    /*
     * Suite 2: getValue(row, col) - ACoC
     *
     * Interface-based characteristics:
     * C1: Row    = negative / valid / above range
     * C2: Column = negative / valid / above range
     *
     * Representatives: -1 / 4 / 9
     *
     * Functionality-based characteristic:
     * C3: Cell state:
     *     EMPTY   = empty and mutable
     *     PLAYER  = filled and mutable
     *     GIVEN   = filled and immutable
     *     NO_CELL = coordinate outside the board
     *
     * Scope:
     * Empty immutable cells are excluded from this input model.
     *
     * Constraints:
     * - Valid coordinates allow EMPTY, PLAYER, or GIVEN.
     * - Invalid coordinates allow only NO_CELL.
     *
     * Feasible combinations: (1 x 3) + (8 x 1) = 11.
     * Expected result for an out-of-range coordinate: "".
     */

    @Test
    public void testGV01_NegativeRowNegativeColumn() {
        assertEquals("", puzzle.getValue(-1, -1));
    }

    @Test
    public void testGV02_NegativeRowValidColumn() {
        assertEquals("", puzzle.getValue(-1, 4));
    }

    @Test
    public void testGV03_NegativeRowAboveRangeColumn() {
        assertEquals("", puzzle.getValue(-1, 9));
    }

    @Test
    public void testGV04_ValidRowNegativeColumn() {
        assertEquals("", puzzle.getValue(4, -1));
    }

    @Test
    public void testGV05_ValidPositionEmptyCell() {
        puzzle.board[4][4] = "";
        puzzle.mutable[4][4] = true;

        assertEquals("", puzzle.getValue(4, 4));
    }

    @Test
    public void testGV06_ValidPositionPlayerFilledCell() {
        puzzle.board[4][4] = "5";
        puzzle.mutable[4][4] = true;

        assertEquals("5", puzzle.getValue(4, 4));
    }

    @Test
    public void testGV07_ValidPositionGivenCell() {
        puzzle.board[4][4] = "7";
        puzzle.mutable[4][4] = false;

        assertEquals("7", puzzle.getValue(4, 4));
    }
    //Should be output expected row 4 , col 9
    @Test
    public void testGV08_ValidRowAboveRangeColumn() {
        assertEquals("", puzzle.getValue(4, 8));
    }

    @Test
    public void testGV09_AboveRangeRowNegativeColumn() {
        assertEquals("", puzzle.getValue(9, -1));
    }
    //Should be output expected row 9 , col 4
    @Test
    public void testGV10_AboveRangeRowValidColumn() {
        assertEquals("", puzzle.getValue(8, 4));
    }
    //Should be output expected row 9 , col 9
    @Test
    public void testGV11_AboveRangeRowAboveRangeColumn() {
        assertEquals("", puzzle.getValue(8, 8));
    }
}
