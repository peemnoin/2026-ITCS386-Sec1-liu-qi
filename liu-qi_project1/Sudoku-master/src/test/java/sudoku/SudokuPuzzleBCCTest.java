/* Copyright (C) 2026 Piyada Chalermnontakarn - All Rights Reserved
 * You may use, distribute and modify this code under the terms of the MIT license.
 */
package sudoku;
import org.junit.Test;
import static org.junit.Assert.*;
public class SudokuPuzzleBCCTest {
    private SudokuPuzzle puzzle;
    // BCC-1: isValidMove()
    @Test
    public void testIsValidMoveBase() {
        String[][] board = new String[][] {
                {"0","0","0","3","4","2","9","0","0"},
                {"0","0","9","0","0","0","7","0","0"},
                {"4","0","0","0","0","0","0","0","3"},
                {"0","0","6","4","7","3","2","0","0"},
                {"0","3","0","0","0","0","0","1","0"},
                {"0","0","2","8","5","1","6","0","0"},
                {"7","0","0","0","0","0","0","0","8"},
                {"0","0","4","0","0","0","1","0","0"},
                {"0","0","3","6","9","7","5","0","0"}
        };

        puzzle = new SudokuPuzzleForTesting(board);

        // Base: valid row, valid column, no row/column/box conflict
        assertTrue(puzzle.isValidMove(0, 0, "1"));
    }

    @Test
    public void testIsValidMoveInvalidRow() {
        String[][] board = new String[][] {
                {"0","0","0","3","4","2","9","0","0"},
                {"0","0","9","0","0","0","7","0","0"},
                {"4","0","0","0","0","0","0","0","3"},
                {"0","0","6","4","7","3","2","0","0"},
                {"0","3","0","0","0","0","0","1","0"},
                {"0","0","2","8","5","1","6","0","0"},
                {"7","0","0","0","0","0","0","0","8"},
                {"0","0","4","0","0","0","1","0","0"},
                {"0","0","3","6","9","7","5","0","0"}
        };

        puzzle = new SudokuPuzzleForTesting(board);

        // Invalid row
        assertFalse(puzzle.isValidMove(-1, 0, "1"));
    }

    @Test
    public void testIsValidMoveInvalidColumn() {
        String[][] board = new String[][] {
                {"0","0","0","3","4","2","9","0","0"},
                {"0","0","9","0","0","0","7","0","0"},
                {"4","0","0","0","0","0","0","0","3"},
                {"0","0","6","4","7","3","2","0","0"},
                {"0","3","0","0","0","0","0","1","0"},
                {"0","0","2","8","5","1","6","0","0"},
                {"7","0","0","0","0","0","0","0","8"},
                {"0","0","4","0","0","0","1","0","0"},
                {"0","0","3","6","9","7","5","0","0"}
        };

        puzzle = new SudokuPuzzleForTesting(board);

        // Invalid column
        assertFalse(puzzle.isValidMove(0, -1, "1"));
    }

    @Test
    public void testIsValidMoveRowConflict() {
        String[][] board = new String[][] {
                {"0","0","0","8","4","2","9","0","0"},
                {"0","0","9","0","0","0","7","0","0"},
                {"4","0","0","0","0","0","0","0","3"},
                {"0","0","6","4","7","3","2","0","0"},
                {"0","3","0","0","0","0","0","1","0"},
                {"0","0","2","8","5","1","6","0","0"},
                {"7","0","0","0","0","0","0","0","8"},
                {"0","0","4","0","0","0","1","0","0"},
                {"0","0","3","6","9","7","5","0","0"}
        };

        puzzle = new SudokuPuzzleForTesting(board);

        // Row conflict only:
        // "8" is in the same row but outside the target 3x3 box
        assertFalse(puzzle.isValidMove(0, 0, "8"));
    }

    @Test
    public void testIsValidMoveColumnConflict() {
        String[][] board = new String[][] {
                {"0","0","0","3","4","2","9","0","0"},
                {"0","0","9","0","0","0","7","0","0"},
                {"4","0","0","0","0","0","0","0","3"},
                {"8","0","6","4","7","3","2","0","0"},
                {"0","3","0","0","0","0","0","1","0"},
                {"0","0","2","8","5","1","6","0","0"},
                {"7","0","0","0","0","0","0","0","8"},
                {"0","0","4","0","0","0","1","0","0"},
                {"0","0","3","6","9","7","5","0","0"}
        };

        puzzle = new SudokuPuzzleForTesting(board);

        // Column conflict only:
        // "8" is in the same column but outside the target 3x3 box
        assertFalse(puzzle.isValidMove(0, 0, "8"));
    }

    @Test
    public void testIsValidMoveBoxConflict() {
        String[][] board = new String[][] {
                {"0","0","0","3","4","2","9","0","0"},
                {"0","8","0","0","0","0","7","0","0"},
                {"4","0","0","0","0","0","0","0","3"},
                {"0","0","6","4","7","3","2","0","0"},
                {"0","3","0","0","0","0","0","1","0"},
                {"0","0","2","8","5","1","6","0","0"},
                {"7","0","0","0","0","0","0","0","8"},
                {"0","0","4","0","0","0","1","0","0"},
                {"0","0","3","6","9","7","5","0","0"}
        };

        puzzle = new SudokuPuzzleForTesting(board);

        // Box conflict only:
        // "8" is in the same 3x3 box but different row and column
        assertFalse(puzzle.isValidMove(0, 0, "8"));
    }
    // BCC-2: isSlotAvailable()
    @Test
    public void testIsSlotAvailableBase() {
        String[][] board = new String[][] {
                {"", "", "8", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""}
        };

        puzzle = new SudokuPuzzleForTesting(board);

        assertTrue(puzzle.isSlotAvailable(0, 0));
    }
    @Test
    public void testIsSlotAvailableInvalidRow() {
        String[][] board = new String[][] {
                {"", "", "8", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""}
        };

        puzzle = new SudokuPuzzleForTesting(board);

        assertFalse(puzzle.isSlotAvailable(-1, 0));
    }
    @Test
    public void testIsSlotAvailableInvalidColumn() {
        String[][] board = new String[][] {
                {"", "", "8", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", "", ""}
        };

        puzzle = new SudokuPuzzleForTesting(board);

        assertFalse(puzzle.isSlotAvailable(0, -1));
    }
    @Test
    public void testIsSlotAvailableUnavailableSlot() {
        String[][] board = new String[][] {
                {"", "", "8", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", ""},
                {"", "", "", "", "", "", "", ""}
        };

        puzzle = new SudokuPuzzleForTesting(board);

        assertFalse(puzzle.isSlotAvailable(0, 2));
    }
private class SudokuPuzzleForTesting extends SudokuPuzzle {

    public SudokuPuzzleForTesting(String[][] board) {
        super(9, 9, 3, 3,
                new String[]{"1", "2", "3", "4", "5", "6", "7", "8", "9"});
        this.board = board;
        }
    }
}
