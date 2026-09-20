
/* Copyright (C) 2026 Tinakome Rasripenngam - All Rights Reserved
 * You may use, distribute and modify this code under the terms of the MIT license.
 */
package sudoku;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

public class ECC_SudokuPuzzleTest {

    private SudokuPuzzle puzzle;

    @Before
    public void setUp() {
        puzzle = new SudokuPuzzleForTesting();
    }

    // isSlotMutable()
    @Test
    public void testIsSlotMutable_ECC() {
        Assert.assertTrue(puzzle.isSlotMutable(0, 0));
        Assert.assertFalse(puzzle.isSlotMutable(0, 1));
    }

    // makeSlotEmpty()
    @Test
    public void testMakeSlotEmpty_ECC() {
        // T1
        puzzle.makeSlotEmpty(0, 0);
        Assert.assertEquals("", puzzle.getValue(0, 0));

        // T2
        puzzle.makeSlotEmpty(0, 2);
        Assert.assertEquals("", puzzle.getValue(0, 2));
    }

    private class SudokuPuzzleForTesting extends SudokuPuzzle {

        public SudokuPuzzleForTesting() {
            super(9, 9, 3, 3,
                    new String[] {
                            "1", "2", "3", "4", "5",
                            "6", "7", "8", "9"
                    });

            this.board[0][0] = "5";
            this.board[0][1] = "3";

            this.mutable[0][0] = true;
            this.mutable[0][1] = false;
        }
    }
}