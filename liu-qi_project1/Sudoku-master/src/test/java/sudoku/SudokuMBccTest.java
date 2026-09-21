/* Copyright (C) 2026 Wirunya Kaewthong - All Rights Reserved
 * You may use, distribute and modify this code under the terms of
 * the MIT license.
 */
package sudoku;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Multiple Base Choice Coverage (MBCC) in one test class.
 * MM01-MM28: makeMove() - 28 tests.
 * NB01-NB12: numInBox() - 12 tests.
 * Each @Test receives a fresh 9x9 puzzle through setUp().
 */
public class SudokuMBccTest {
    private SudokuPuzzle puzzle;

    @Before
    public void setUp() {
        puzzle = new SudokuPuzzle(9, 9, 3, 3,
                new String[]{"1", "2", "3", "4", "5", "6", "7", "8", "9"});
    }

    // Group 1: makeMove() - two bases and their one-characteristic variations.
    @Test
    public void testMM01_Base_Editable() {
        checkMove(4, 4, "5", "NONE", true, "", true);
    }

    @Test
    public void testMM02_Row_0_Editable() {
        checkMove(0, 4, "5", "NONE", true, "", true);
    }

    @Test
    public void testMM03_Row_8_Editable() {
        checkMove(8, 4, "5", "NONE", true, "", true);
    }

    @Test
    public void testMM04_Column_0_Editable() {
        checkMove(4, 0, "5", "NONE", true, "", true);
    }

    @Test
    public void testMM05_Column_8_Editable() {
        checkMove(4, 8, "5", "NONE", true, "", true);
    }

    @Test
    public void testMM06_Value_X_Editable() {
        checkMove(4, 4, "X", "NONE", true, "", true);
    }

    @Test
    public void testMM07_Value_Empty_Editable() {
        checkMove(4, 4, "", "NONE", true, "", true);
    }

    @Test
    public void testMM08_Value_Null_Editable() {
        checkMove(4, 4, null, "NONE", true, "", true);
    }

    @Test
    public void testMM09_Conflict_ROW_Editable() {
        checkMove(4, 4, "5", "ROW", true, "", true);
    }

    @Test
    public void testMM10_Conflict_COLUMN_Editable() {
        checkMove(4, 4, "5", "COLUMN", true, "", true);
    }

    @Test
    public void testMM11_Conflict_BOX_Editable() {
        checkMove(4, 4, "5", "BOX", true, "", true);
    }

    @Test
    public void testMM12_Conflict_MULTIPLE_Editable() {
        checkMove(4, 4, "5", "MULTIPLE", true, "", true);
    }

    @Test
    public void testMM13_CurrentMutable_False_Editable() {
        checkMove(4, 4, "5", "NONE", false, "", true);
    }

    @Test
    public void testMM14_ExistingValue_2_Editable() {
        checkMove(4, 4, "5", "NONE", true, "2", true);
    }

    @Test
    public void testMM15_Base_Locked() {
        checkMove(4, 4, "5", "NONE", true, "", false);
    }

    @Test
    public void testMM16_Row_0_Locked() {
        checkMove(0, 4, "5", "NONE", true, "", false);
    }

    @Test
    public void testMM17_Row_8_Locked() {
        checkMove(8, 4, "5", "NONE", true, "", false);
    }

    @Test
    public void testMM18_Column_0_Locked() {
        checkMove(4, 0, "5", "NONE", true, "", false);
    }

    @Test
    public void testMM19_Column_8_Locked() {
        checkMove(4, 8, "5", "NONE", true, "", false);
    }

    @Test
    public void testMM20_Value_X_Locked() {
        checkMove(4, 4, "X", "NONE", true, "", false);
    }

    @Test
    public void testMM21_Value_Empty_Locked() {
        checkMove(4, 4, "", "NONE", true, "", false);
    }

    @Test
    public void testMM22_Value_Null_Locked() {
        checkMove(4, 4, null, "NONE", true, "", false);
    }

    @Test
    public void testMM23_Conflict_ROW_Locked() {
        checkMove(4, 4, "5", "ROW", true, "", false);
    }

    @Test
    public void testMM24_Conflict_COLUMN_Locked() {
        checkMove(4, 4, "5", "COLUMN", true, "", false);
    }

    @Test
    public void testMM25_Conflict_BOX_Locked() {
        checkMove(4, 4, "5", "BOX", true, "", false);
    }

    @Test
    public void testMM26_Conflict_MULTIPLE_Locked() {
        checkMove(4, 4, "5", "MULTIPLE", true, "", false);
    }

    @Test
    public void testMM27_CurrentMutable_False_Locked() {
        checkMove(4, 4, "5", "NONE", false, "", false);
    }

    @Test
    public void testMM28_ExistingValue_2_Locked() {
        checkMove(4, 4, "5", "NONE", true, "2", false);
    }

    // Group 2: numInBox() - two bases and their one-characteristic variations.
    @Test
    public void testNB01_Base_FIRST() {
        checkBox(0, 0, "FIRST", true);
    }

    @Test
    public void testNB02_RowBand_FIRST() {
        checkBox(1, 0, "FIRST", true);
    }

    @Test
    public void testNB03_ColumnBand_FIRST() {
        checkBox(0, 1, "FIRST", true);
    }

    @Test
    public void testNB04_Match_MIDDLE() {
        checkBox(0, 0, "MIDDLE", true);
    }

    @Test
    public void testNB05_Match_OUTSIDE() {
        checkBox(0, 0, "OUTSIDE", false);
    }

    @Test
    public void testNB06_Match_ABSENT() {
        checkBox(0, 0, "ABSENT", false);
    }

    @Test
    public void testNB07_Base_LAST() {
        checkBox(2, 2, "LAST", true);
    }

    @Test
    public void testNB08_RowBand_LAST() {
        checkBox(1, 2, "LAST", true);
    }

    @Test
    public void testNB09_ColumnBand_LAST() {
        checkBox(2, 1, "LAST", true);
    }

    @Test
    public void testNB10_Match_MIDDLE() {
        checkBox(2, 2, "MIDDLE", true);
    }

    @Test
    public void testNB11_Match_OUTSIDE() {
        checkBox(2, 2, "OUTSIDE", false);
    }

    @Test
    public void testNB12_Match_ABSENT() {
        checkBox(2, 2, "ABSENT", false);
    }

    // Prepare a move scenario, call makeMove(), and compare the full expected state.
    private void checkMove(int row, int col, String value, String conflict,
                           boolean currentMutable, String oldValue, boolean requestedMutable) {
        puzzle.board[row][col] = oldValue;
        puzzle.mutable[row][col] = currentMutable;
        int outsideRow = (row + 3) % 9;
        int outsideCol = (col + 3) % 9;
        int insideRow = (row / 3) * 3 + (row + 1) % 3;
        int insideCol = (col / 3) * 3 + (col + 1) % 3;
        if (conflict.equals("ROW") || conflict.equals("MULTIPLE"))
            puzzle.board[row][outsideCol] = "5";
        if (conflict.equals("COLUMN") || conflict.equals("MULTIPLE"))
            puzzle.board[outsideRow][col] = "5";
        if (conflict.equals("BOX") || conflict.equals("MULTIPLE"))
            puzzle.board[insideRow][insideCol] = "5";

        String[][] expectedBoard = new String[9][];
        boolean[][] expectedMutable = new boolean[9][];
        for (int r = 0; r < 9; r++) {
            expectedBoard[r] = puzzle.board[r].clone();
            expectedMutable[r] = puzzle.mutable[r].clone();
        }
        // This suite's only accepted input value is "5".
        boolean accepted = "5".equals(value) && conflict.equals("NONE") && currentMutable;
        if (accepted) {
            expectedBoard[row][col] = value;
            expectedMutable[row][col] = requestedMutable;
        }
        puzzle.makeMove(row, col, value, requestedMutable);
        for (int r = 0; r < 9; r++) {
            assertArrayEquals("Board row " + r, expectedBoard[r], puzzle.board[r]);
            assertArrayEquals("Mutable row " + r, expectedMutable[r], puzzle.mutable[r]);
        }
    }

    // Prepare a box-search scenario, check its result, and verify no state changes.
    private void checkBox(int rowBand, int colBand, String match, boolean expected) {
        int firstRow = rowBand * 3;
        int firstCol = colBand * 3;
        if (match.equals("FIRST")) puzzle.board[firstRow][firstCol] = "5";
        if (match.equals("MIDDLE")) puzzle.board[firstRow + 1][firstCol + 1] = "5";
        if (match.equals("LAST")) puzzle.board[firstRow + 2][firstCol + 2] = "5";
        if (match.equals("OUTSIDE")) puzzle.board[firstRow][(firstCol + 3) % 9] = "5";
        String[][] before = new String[9][];
        boolean[][] mutableBefore = new boolean[9][];
        for (int r = 0; r < 9; r++) {
            before[r] = puzzle.board[r].clone();
            mutableBefore[r] = puzzle.mutable[r].clone();
        }
        // Query the center of the selected box, regardless of match location.
        assertEquals(expected, puzzle.numInBox(firstRow + 1, firstCol + 1, "5"));
        for (int r = 0; r < 9; r++) {
            assertArrayEquals("Board row " + r, before[r], puzzle.board[r]);
            assertArrayEquals("Mutable row " + r, mutableBefore[r], puzzle.mutable[r]);
        }
    }
}
