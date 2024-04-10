Sudoku Solver can solve, or help you solve, Sudoku puzzles.

The rules of Sudoku are very simple:
 - each digit 1-9 must appear exactly once in each row, column or 3x3 square

Solving a puzzle.
=================

The basic step to solve a puzzle is to select a value for a square. If you click in a square which has only one possible value available, that square will be coloured in, and that value is removed from all the other squares in the same row, column and 3x3 square (because it has now been assigned to the square you clicked in, it cannot be also put in the other squares in the same row, column and 3x3 square).

If there are still multiple values possible for the square you click in, you will be presented with a pop-up menu of the possible values. Selecting any one of these will assign that value to the square (as above). Of course, you can also choose to not select on of the values, but releasing the mouse button while outside the pop-up menu.

When you assign a value like this, the "mechanical" work of removing that value from the row, column and 3x3 square is done for you. 

Note that the status bar at the bottom of the window will show the number of possible combinations left: this will decrease as the solution progresses, and should eventually reach 1.


There are three buttons which further automate the solving of a puzzle. Two of these (Singles and Soles) implement the two basic solution strategies, while the third (Solve it) simply applies the two strategies in turn until it succeeds (or goes as far as it can).

Singles.
--------

Any square for which there is only a single remaining value allowed is called a "single". Obviously, the initial values assigned as part of the puzzle definition are one example of this. The "single" value can be assigned to that square, and then that digit can be eliminate from the other squares in the same row, the same column and the same 3x3 square. This elimination of values may generate additional "singles" - they are not immediately taken, but clicking the button again will do them.

Soles.
------

There may be only one square in a row which can still contain one of the digits, and this will be called the "sole" place that digit can go. Note this square may not be a "single" - it may have any number of still-valid possibilities, but if a particular digit can only be in the one place in that row, then it can be assigned as the "sole" place for it to go. Obviously, this can be applied to columns, and to 3x3 squares as well.


Solve It
--------

As we said above, this simply applies each of the two methods (Singles and Soles) above in turn, until neither produces any progress.



There are three further buttons for use in solving puzzles. 

Blank
-----

This produces a new, blank puzzle (i.e. equivalent to selecting File / New from the menu).

Undo   and  Redo
----        ----

These are fairly self-explanatory - each click will undo (or redo) one step of the solution so far.


Simple, Moderate and Complex Puzzles.
====================================

The four built-in puzzles are in order of simple to more difficult. You will find that many puzzles, like the first three here, can be solved simply by applying the strategies described above (either by clicking the buttons, or more satisfyingly by working through the puzzle one square at a time).

However, some puzzles, such as the fourth built-in example, will not be fully resolved by using these techniques. While there are other analytical methods possible, the usual method to tackle these is simply to "postulate" (i.e. guess !!) one of the remaining values and see whether that leads to a solution or not. 

Well constructed Sudoku puzzles should have only a single solution, so this method will work. 

The easiest way to use this Sudoku Solver to do this is to simply choose the top, left square which still has multiple values possible, and do a trial assignment of the first value to it. Then click on "Solve it", and see what happens.

If this value-assignment is incorrect, it will usually lead to some square(s) having no possible values left, and it (they) will be coloured bright red, so will be easy to spot. You can then click "Undo" multiple times, until you reach the point at which you made the guess. Then try the next possible value, and again click "Solve it". If the assignment is correct, then clicking "Solve it" will usually lead to a complete solution.

Occasionally, the first guessed value will lead to neither a complete solution nor a complete conflict. In this case, you may need to move on to the next square which is not yet decided, and make a guess there. But do make sure that you remember to click on "Solve it" (or that you do the equivalent effort yourself) or you risk the possibility of not detecting the complete conflict or solution.

(I have not actually found a puzzle that requires this multi-step postulation, but it's theoretically possible - if you do find one, please send it to me.)



Defining or selecting a puzzle.
===============================

A puzzle definition sets the initial values for some of the squares assignments. There are four puzzles built-in, and you can add as many new puzzles as you like. The quickest way to create a new puzzle is to edit a text definition file, and the solve that puzzle by selecting File / Open from the menu.  The format for these files is simple; each row of the puzzle is a line in the file, each character is a single square, containing either a digit or 'x'. Extra spaces or blank lines are ignored. So the file to define the first built-in puzzle could look like:

98x 354 xxx
41x xx2 8xx
x32 x1x 7xx

29x 1x5 xxx
xxx x6x xxx
643 xx7 21x

xxx 8xx x2x
x5x x2x 6x7
xxx x3x x9x


You can also create a puzzle by starting with a blank puzzle (i.e. immediately after starting the program, or by clicking the "Blank" button), then specifying values for your initial squares (by clicking in a square, then selecting the value from the pop-up menu), and finally selecting menu File / Save as ... and storing the puzzle definition in a file.

You could also add more 'built-in' puzzles using the resource editor, by adding invisible buttons (similar to P1, P2, P3 P4) and adding menu entries (similar to File / Puzzle1 (the actual puzzle definition goes in the "userdata" of the invisible buttons). 

You can save a puzzle at any time, using the File / Save As .... menu selection. This will save the puzzle in the format described above, i.e. the only info saved is which squares have a single possible value assigned. All other squares will be simply marked as 'unknown' so if you later re-open this puzzle, you will be in an equivalent position, but will not see exactly the possibilities as you had seen before saving the puzzle state.

The File / Save menu item is currently disabled, because it rarely, if ever, makes sense to save the current state so as to overwrite the state in the file.


Further options
===============

The two buttons at the bottom of the window give you further options on how much help you are given. Toggling both of these will let you solve the puzzle with no help at all - equivalent to solving it on paper, but without any easy way to mark-up your partial solutions or ideas.

Hide Undecided
--------------

Normally, any square for which there are multiple values still possible will show all of those choices (and only those choices). [Remember that until you have assigned a value to a square (and the square background has been coloured in), the assignment has not happened, so even though there is only a single possible value showing, that value will continue to be available in the other squares in the row, column and 3x3 square).] Toggling this button down will hide the multiple values in such undecided squares (but if you click in the square, the pop-up menu will present only the valid choices).

Hide choices
------------

This controls which values are presented in the pop-up menu; when it is toggled, all values (1-9) are in the menu - whereas in the other case, only the values known to be valid are shown.

