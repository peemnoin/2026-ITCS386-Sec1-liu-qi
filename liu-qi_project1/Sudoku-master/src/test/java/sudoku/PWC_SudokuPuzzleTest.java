/* Copyright (C) 2026 Sunattha Boonl-or - All Rights Reserved
 * You may use, distribute and modify this code under the terms of the MIT license.
 */
package sudoku;

import org.junit.Assert;
import org.junit.Test;

public class PWC_SudokuPuzzleTest {

    // isSlotAvailable()
    // Characteristics: Position (Boundary/Interior), Content (Empty/Occupied), Mutability (Mutable/Immutable)
    @Test
    public void testIsSlotAvailable_PWC() {
        // T1
        SudokuPuzzle p1 = new SudokuPuzzleForAvailableTest(emptyBoard(), allMutable());
        Assert.assertTrue(p1.isSlotAvailable(0, 0));

        // T2
        String[][] b2 = emptyBoard();
        b2[0][0] = "5";
        boolean[][] m2 = allMutable();
        m2[0][0] = false;
        SudokuPuzzle p2 = new SudokuPuzzleForAvailableTest(b2, m2);
        Assert.assertFalse(p2.isSlotAvailable(0, 0));

        // T3
        boolean[][] m3 = allMutable();
        m3[4][4] = false;
        SudokuPuzzle p3 = new SudokuPuzzleForAvailableTest(emptyBoard(), m3);
        Assert.assertFalse(p3.isSlotAvailable(4, 4));

        // T4
        String[][] b4 = emptyBoard();
        b4[4][4] = "5";
        SudokuPuzzle p4 = new SudokuPuzzleForAvailableTest(b4, allMutable());
        Assert.assertFalse(p4.isSlotAvailable(4, 4));
    }

    private class SudokuPuzzleForAvailableTest extends SudokuPuzzle {
        public SudokuPuzzleForAvailableTest(String[][] board, boolean[][] mutable) {
            super(9, 9, 3, 3, new String[] {"1","2","3","4","5","6","7","8","9"});
            this.board = board;
            this.mutable = mutable;
        }
    }

    // makeMove()
    // Characteristics: Value (Valid/Invalid), Position (In-range/Out-of-range), Conflict (No/Yes), Mutability (Mutable/Locked)
    @Test
    public void testMakeMove_PWC() {
        // T1
        SudokuPuzzle p1 = new SudokuPuzzleForMakeMoveTest(emptyBoard(), allMutable());
        p1.makeMove(0, 0, "5", true);
        Assert.assertEquals("5", p1.getValue(0, 0));

        // T2
        String[][] b2 = emptyBoard();
        b2[0][4] = "5";
        boolean[][] m2 = allMutable();
        m2[0][0] = false;
        SudokuPuzzle p2 = new SudokuPuzzleForMakeMoveTest(b2, m2);
        p2.makeMove(0, 0, "5", true);
        Assert.assertEquals("", p2.getValue(0, 0));

        // T3
        boolean[][] m3 = allMutable();
        m3[0][0] = false;
        SudokuPuzzle p3 = new SudokuPuzzleForMakeMoveTest(emptyBoard(), m3);
        p3.makeMove(-1, 0, "5", true);
        Assert.assertEquals("", p3.getValue(0, 0));

        // T4
        boolean[][] m4 = allMutable();
        m4[0][0] = false;
        SudokuPuzzle p4 = new SudokuPuzzleForMakeMoveTest(emptyBoard(), m4);
        p4.makeMove(0, 0, "X", true);
        Assert.assertEquals("", p4.getValue(0, 0));

        // T5
        String[][] b5 = emptyBoard();
        b5[0][4] = "5";
        SudokuPuzzle p5 = new SudokuPuzzleForMakeMoveTest(b5, allMutable());
        p5.makeMove(-1, -1, "X", true);
        Assert.assertEquals("", p5.getValue(0, 0));
    }

    private String[][] emptyBoard() {
        String[][] board = new String[9][9];
        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                board[r][c] = "";
            }
        }
        return board;
    }

    private boolean[][] allMutable() {
        boolean[][] mutable = new boolean[9][9];
        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                mutable[r][c] = true;
            }
        }
        return mutable;
    }

    private class SudokuPuzzleForMakeMoveTest extends SudokuPuzzle {
        public SudokuPuzzleForMakeMoveTest(String[][] board, boolean[][] mutable) {
            super(9, 9, 3, 3, new String[] {"1","2","3","4","5","6","7","8","9"});
            this.board = board;
            this.mutable = mutable;
        }
    }
}        if (!full) {
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
