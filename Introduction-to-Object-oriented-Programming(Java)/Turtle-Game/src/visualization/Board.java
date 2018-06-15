package visualization;

import java.util.*;
import java.awt.Color;
import java.awt.Font;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.JFrame;

import acm.graphics.GCanvas;
import acm.graphics.GImage;
import acm.graphics.GLabel;
import acm.graphics.GObject;
import acm.graphics.GTurtle;


/**
 * The implementation of the construction of the screen that the game is displayed.
 * 
 * The background picture is adjusted and the turtle is added to the board. 
 * Other objects ( in that game, bus and car) are allowed to be added.
 * The round and score are stored and let be changed as the game goes on.
 * The display time is arranged
 *  
 * @author alim
 *
 */
public class Board implements BoardIntf{
	
	/**
	 * The width of the turtle image
	 */
	private static final int TURTLE_WIDTH = 80;
	/**
	 * The image of the turtle
	 */
	private static final String TURTLE_IMAGE_PATH = "turtle.png";
	/**
	 * The background image
	 */
	private static final String BACKGROUND_IMAGE_PATH = "asfalt.jpg";
	
	/**
	 * The round number 
	 */
	public int round;
	
	/**
	 * The score get by player
	 */
	public int score;
	/**
	 * Checks whether the turtle gets the opposite side.
	 * 1 for bottomside, 0 for upperside
	 */
	public int checkRound;
	/**
	 * Round number and the score
	 */
	GLabel label, label2;
	
	/**
	 * The frame of the board
	 */
	private JFrame frame;
	/**
	 * Allows the board to add objects
	 */
	private GCanvas canvas;
	/**
	 * The turtle object
	 */
	private GImage turtle;
	/**
	 * The background of the board
	 */
	private GImage background;
	
	/**
	 * Constructs a board with a given name, width and height which are given in parameters
	 * 
	 * Calls the setCanvas method to build the board. Then adds the background, the labels and the turtle
	 * onto the board. 
	 * Sets the checkRound and round 1 and the score 0.
	 * 
	 * @param boardName
	 * @param width
	 * @param height
	 */
	
	public Board(String boardName, int width, int height) {
		setCanvas(boardName, width, height);
		setBackground();
		addTurtle();
		addGameInfoLabels();
		checkRound = 1;
		round = 1;
		score=0;
		
	}
	
	/**
	 * {@inheritDoc}
	 */
	public void setCanvas(String boardName, int width, int height) {
		frame = new JFrame(boardName);
		frame.setSize(width, height);
		canvas = new GCanvas();
		frame.getContentPane().add(canvas);

		frame.setVisible(true);
		frame.addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent windowEvent) {
				System.exit(0);
			}
		});
		addKeyBoardListener();
	}

	/**
	 * {@inheritDoc}
	 */
	public void addKeyBoardListener() {
		frame.addKeyListener(new KeyListener() {

			@Override
			public void keyTyped(KeyEvent e) {
			}

			@Override
			public void keyReleased(KeyEvent e) {
			}

			@Override
			public void keyPressed(KeyEvent event) {
				int keyCode = event.getKeyCode();
				if (keyCode == KeyEvent.VK_UP) {
					if(turtle.getY()+turtle.getHeight()>0)
					turtle.move(0, -10);
				} else if (keyCode == KeyEvent.VK_DOWN) {
					if(turtle.getY()+turtle.getHeight()<frame.getHeight())
					turtle.move(0, 10);
				} else if (keyCode == KeyEvent.VK_RIGHT) {
					if(turtle.getX()+turtle.getWidth()<frame.getWidth())
					turtle.move(10, 0);
				} else if (keyCode == KeyEvent.VK_LEFT) {
					if(turtle.getX()+turtle.getWidth()>0)
					turtle.move(-10, 0);
				}
			}
		});
	}
	/**
	 * Creates a turtle by using the turtle image and adds it onto the board.
	 * 
	 * Sets the location and the size of the turtle.
	 */
	private void addTurtle() {
		turtle = new GImage(TURTLE_IMAGE_PATH);
		turtle.scale(0.33);
		turtle.setLocation(frame.getWidth()/2, frame.getHeight()
				- TURTLE_WIDTH);
		canvas.add(turtle);
	}
	
	/**
	 * Returns the turtle which is added to the board.
	 * Lets the main class reach the fields of the turtle
	 * 
	 * @return
	 */
	public GImage getTurtle(){
		return turtle;
	}
	
	/**
	 * {@inheritDoc}
	 */
	public void setBackground() {
		background = new GImage(BACKGROUND_IMAGE_PATH);
		background.scale(0.8);
		canvas.add(background);
		background.sendBackward();
	}
	/**
	 * {@inheritDoc}
	 */
	public void waitFor(long millisecs) {
		try {
			Thread.sleep(millisecs);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * {@inheritDoc}
	 */
	public void addObject(GObject g) {
		canvas.add(g);
		objects.add(g);

	}
	
	/**
	 * {@inheritDoc}
	 */
	public void addGameInfoLabels(){
		label = new GLabel("Round :" , 0,660);
		label2 = new GLabel("Score :",0, 680);
		label.setFont(new Font("Arial", Font.BOLD, 18));
		label.setColor(Color.BLACK);
		label2.setFont(new Font("Arial", Font.BOLD, 18));
		label2.setColor(Color.BLACK);
		
		addObject(label);
		addObject(label2);		
	}
	/**
	 * Changes the label when the round number or the score changes instead of creating a new Glabel
	 */
	public void setLabel(){
		label.setLabel("Round :" + round);
		label2.setLabel("Score: " + score);
	}

}