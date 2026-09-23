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
 * BF01-BF06: boardFull() - 6 tests.
 * Total: 34 tests.
 * Each @Test receives a fresh puzzle instance through setUp().
 */
public class SudokuMBccTest {
    private SudokuPuzzle puzzle;

    @Before
    public void setUp() {
        puzzle = new SudokuPuzzle(9, 9, 3, 3,
                new String[]{"1", "2", "3", "4", "5", "6", "7", "8", "9"});
    }

    // Group 1: makeMove() - two bases and their one-characteristic variations (MM01 - MM28)
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

    // Group 2: boardFull() - two bases and their one-characteristic variations (BF01 - BF06)
    @Test
    public void testBF01_BaseChoice1_CompletelyFull_9x9() {
        SudokuPuzzle fullPuzzle = createFull9x9Board();
        assertTrue(fullPuzzle.boardFull());
    }

    @Test
    public void testBF02_VaryC2_CompletelyFull_6x6() {
        SudokuPuzzle fullPuzzle = createFull6x6Board();
        assertTrue(fullPuzzle.boardFull());
    }

    @Test
    public void testBF03_BaseChoice2_AlmostFull_9x9() {
        SudokuPuzzle almostFullPuzzle = createFull9x9Board();
        almostFullPuzzle.board[8][8] = ""; // Boundary: clear exactly 1 slot
        assertFalse(almostFullPuzzle.boardFull());
    }

    @Test
    public void testBF04_VaryC2_AlmostFull_6x6() {
        SudokuPuzzle almostFullPuzzle = createFull6x6Board();
        almostFullPuzzle.board[5][5] = ""; // Boundary: clear exactly 1 slot
        assertFalse(almostFullPuzzle.boardFull());
    }

    @Test
    public void testBF05_VaryC1_PartiallyFilled_9x9() {
        puzzle.makeMove(0, 0, "1", true);
        assertFalse(puzzle.boardFull());
    }

    @Test
    public void testBF06_VaryC1_CompletelyEmpty_9x9() {
        assertFalse(puzzle.boardFull());
    }

    // Helper: Prepare a move scenario, call makeMove(), and compare expected state
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

    // Helper: Generate a full valid 9x9 Sudoku board
    private SudokuPuzzle createFull9x9Board() {
        SudokuPuzzle p = new SudokuPuzzle(9, 9, 3, 3,
                new String[]{"1", "2", "3", "4", "5", "6", "7", "8", "9"});
        int[][] pattern = {
                {1,2,3, 4,5,6, 7,8,9},
                {4,5,6, 7,8,9, 1,2,3},
                {7,8,9, 1,2,3, 4,5,6},
                {2,3,4, 5,6,7, 8,9,1},
                {5,6,7, 8,9,1, 2,3,4},
                {8,9,1, 2,3,4, 5,6,7},
                {3,4,5, 6,7,8, 9,1,2},
                {6,7,8, 9,1,2, 3,4,5},
                {9,1,2, 3,4,5, 6,7,8}
        };
        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                p.board[r][c] = String.valueOf(pattern[r][c]);
            }
        }
        return p;
    }

    // Helper: Generate a full valid 6x6 Sudoku board
    private SudokuPuzzle createFull6x6Board() {
        SudokuPuzzle p = new SudokuPuzzle(6, 6, 3, 2,
                new String[]{"1", "2", "3", "4", "5", "6"});
        int[][] pattern = {
                {1,2,3, 4,5,6},
                {4,5,6, 1,2,3},
                {2,3,1, 5,6,4},
                {5,6,4, 2,3,1},
                {3,1,2, 6,4,5},
                {6,4,5, 3,1,2}
        };
        for (int r = 0; r < 6; r++) {
            for (int c = 0; c < 6; c++) {
                p.board[r][c] = String.valueOf(pattern[r][c]);
            }
        }
        return p;
    }
}
