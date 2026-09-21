/* Copyright (C) 2026 Sunattha Boonl-or - All Rights Reserved
 * You may use, distribute and modify this code under the terms of the MIT license.
 */
package sudoku;

import org.junit.Assert;
import org.junit.Test;

public class PWC_SudokuPuzzleTest {

    // isSlotAvailable()
    @Test
    public void testIsSlotAvailable_PWC() {
        String[][] board = new String[9][9];
        boolean[][] mutable = new boolean[9][9];
        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                board[r][c] = "";
                mutable[r][c] = true;
            }
        }
        board[0][1] = "5";
        mutable[0][1] = false;

        SudokuPuzzle puzzle = new SudokuPuzzleForAvailableTest(board, mutable);

        Assert.assertTrue(puzzle.isSlotAvailable(0, 0));
        Assert.assertFalse(puzzle.isSlotAvailable(0, 1));
        Assert.assertFalse(puzzle.isSlotAvailable(-1, 0));
        Assert.assertFalse(puzzle.isSlotAvailable(0, -1));
    }

    private class SudokuPuzzleForAvailableTest extends SudokuPuzzle {
        public SudokuPuzzleForAvailableTest(String[][] board, boolean[][] mutable) {
            super(9, 9, 3, 3, new String[] {"1","2","3","4","5","6","7","8","9"});
            this.board = board;
            this.mutable = mutable;
        }
    }

    // boardFull()
    @Test
    public void testBoardFull_PWC() {
        Assert.assertTrue(build9x9(true).boardFull());     // TC1: 9x9, full
        Assert.assertFalse(build9x9(false).boardFull());   // TC2: 9x9, not-full
        Assert.assertTrue(build12x12(true).boardFull());   // TC3: 12x12, full
        Assert.assertFalse(build12x12(false).boardFull()); // TC4: 12x12, not-full
    }

    private SudokuPuzzle build9x9(boolean full) {
        return new SudokuPuzzleForBoardFullTest(9, 9, 3, 3, fillBoard(9, full));
    }

    private SudokuPuzzle build12x12(boolean full) {
        return new SudokuPuzzleForBoardFullTest(12, 12, 4, 3, fillBoard(12, full));
    }

    private String[][] fillBoard(int size, boolean full) {
        String[][] board = new String[size][size];
        for (int r = 0; r < size; r++) {
            for (int c = 0; c < size; c++) {
                board[r][c] = full ? "1" : "";
            }
        }
        if (!full) {
            board[0][0] = "1";
        }
        return board;
    }

    private static String[] buildValidValues(int size) {
        String[] values = new String[size];
        for (int i = 0; i < size; i++) {
            values[i] = String.valueOf(i + 1);
        }
        return values;
    }

    private class SudokuPuzzleForBoardFullTest extends SudokuPuzzle {
        public SudokuPuzzleForBoardFullTest(int rows, int cols, int boxW, int boxH, String[][] board) {
            super(rows, cols, boxW, boxH, buildValidValues(rows));
            this.board = board;
        }
    }
}