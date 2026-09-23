/* Copyright (C) 2026 Sunattha Boonl-or - All Rights Reserved
 * You may use, distribute and modify this code under the terms of the MIT license.
 */
package sudoku;

import org.junit.Assert;
import org.junit.Test;

public class PWC_SudokuPuzzleTest {

    // isSlotAvailable()
    // Position (Boundary/Interior) x Content (Empty/Occupied) x Mutability (Mutable/Immutable)

    // T1
    @Test
    public void testIsSlotAvailableBoundaryEmptyMutable() {
        SudokuPuzzle puzzle = new SudokuPuzzleForAvailableTest(emptyBoard(), allMutable());
        Assert.assertTrue(puzzle.isSlotAvailable(0, 0));
    }

    // T2
    @Test
    public void testIsSlotAvailableBoundaryOccupiedImmutable() {
        String[][] board = emptyBoard();
        board[0][0] = "5";
        boolean[][] mutable = allMutable();
        mutable[0][0] = false;
        SudokuPuzzle puzzle = new SudokuPuzzleForAvailableTest(board, mutable);
        Assert.assertFalse(puzzle.isSlotAvailable(0, 0));
    }

    // T3
    @Test
    public void testIsSlotAvailableInteriorEmptyImmutable() {
        boolean[][] mutable = allMutable();
        mutable[4][4] = false;
        SudokuPuzzle puzzle = new SudokuPuzzleForAvailableTest(emptyBoard(), mutable);
        Assert.assertFalse(puzzle.isSlotAvailable(4, 4));
    }

    // T4
    @Test
    public void testIsSlotAvailableInteriorOccupiedMutable() {
        String[][] board = emptyBoard();
        board[4][4] = "5";
        SudokuPuzzle puzzle = new SudokuPuzzleForAvailableTest(board, allMutable());
        Assert.assertFalse(puzzle.isSlotAvailable(4, 4));
    }

    // makeMove()
    // Value (Valid/Invalid) x Position (In-range/Out-of-range) x Conflict (No/Yes) x Mutability (Mutable/Locked)

    // T1
    @Test
    public void testMakeMoveValidInRangeNoConflictMutable() {
        SudokuPuzzle puzzle = new SudokuPuzzleForMakeMoveTest(emptyBoard(), allMutable());
        puzzle.makeMove(0, 0, "5", true);
        Assert.assertEquals("5", puzzle.getValue(0, 0));
    }

    // T2
    @Test
    public void testMakeMoveValidInRangeConflictLocked() {
        String[][] board = emptyBoard();
        board[0][4] = "5";
        boolean[][] mutable = allMutable();
        mutable[0][0] = false;
        SudokuPuzzle puzzle = new SudokuPuzzleForMakeMoveTest(board, mutable);
        puzzle.makeMove(0, 0, "5", true);
        Assert.assertEquals("", puzzle.getValue(0, 0));
    }

    // T3
    @Test
    public void testMakeMoveValidOutOfRangeNoConflictLocked() {
        boolean[][] mutable = allMutable();
        mutable[0][0] = false;
        SudokuPuzzle puzzle = new SudokuPuzzleForMakeMoveTest(emptyBoard(), mutable);
        puzzle.makeMove(-1, 0, "5", true);
        Assert.assertEquals("", puzzle.getValue(0, 0));
    }

    // T4
    @Test
    public void testMakeMoveInvalidInRangeNoConflictLocked() {
        boolean[][] mutable = allMutable();
        mutable[0][0] = false;
        SudokuPuzzle puzzle = new SudokuPuzzleForMakeMoveTest(emptyBoard(), mutable);
        puzzle.makeMove(0, 0, "X", true);
        Assert.assertEquals("", puzzle.getValue(0, 0));
    }

    // T5
    @Test
    public void testMakeMoveInvalidOutOfRangeConflictMutable() {
        String[][] board = emptyBoard();
        board[0][4] = "5";
        SudokuPuzzle puzzle = new SudokuPuzzleForMakeMoveTest(board, allMutable());
        puzzle.makeMove(-1, -1, "X", true);
        Assert.assertEquals("", puzzle.getValue(0, 0));
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

    private class SudokuPuzzleForAvailableTest extends SudokuPuzzle {
        public SudokuPuzzleForAvailableTest(String[][] board, boolean[][] mutable) {
            super(9, 9, 3, 3, new String[] {"1","2","3","4","5","6","7","8","9"});
            this.board = board;
            this.mutable = mutable;
        }
    }

    private class SudokuPuzzleForMakeMoveTest extends SudokuPuzzle {
        public SudokuPuzzleForMakeMoveTest(String[][] board, boolean[][] mutable) {
            super(9, 9, 3, 3, new String[] {"1","2","3","4","5","6","7","8","9"});
            this.board = board;
            this.mutable = mutable;
        }
    }
}
