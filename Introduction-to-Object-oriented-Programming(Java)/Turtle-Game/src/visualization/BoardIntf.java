package visualization;

import java.util.ArrayList;

import acm.graphics.GObject;

/**
 * 
 * The implementation of creation of a board with a given name, height and width.
 * 
 * Allows adding object and creating a game board.
 * 
 * @author alim
 * @see Board
 *
 */

public interface BoardIntf {
	/**
	 * Not used
	 */
	ArrayList<GObject> objects = new ArrayList<GObject>();
	
	/**
	 * Creates a frame that surrounds the board and add the board to this frame. The width, height
	 * and name of the board is given in parameters.
	 * 
	 * @param boardName is the name of the board we create
	 * @param width is the width of the board
	 * @param height is the height of the board
	 */
	public void setCanvas(String boardName, int width, int height);
	
	/**
	 * Adds the background image to the board.
	 * Also adjusts the size of the background image.
	 */
	public void setBackground();
	
	/**
	 * Makes the turtle move according to pressed button.
	 * 
	 * Each arrowkey moves the turtle towards their corresponding directions.
	 * 
	 */
	public void addKeyBoardListener();
	

	/**
	 * Adds the round number and the score at the left bottom of the board.
	 */
	public void addGameInfoLabels();
	
	/**
	 * Adds the object given by the parameter to the board. 
	 * The parameters in this game vehicles, labels and the turtle.
	 * 
	 * @param g is the object
	 */
	public void addObject(GObject g);
	
	/**
	 * Waits for in milliseconds which is given in a parameter. 
	 * 
	 * @param millisecs is time in milliseconds
	 */
	public void waitFor(long millisecs);
}
