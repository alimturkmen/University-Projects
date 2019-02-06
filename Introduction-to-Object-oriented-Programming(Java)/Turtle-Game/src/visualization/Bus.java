package visualization;

import java.awt.Color;
import java.awt.Font;

import acm.graphics.GLabel;
import acm.graphics.GOval;
import acm.graphics.GRect;

/**
 * {@inheritDoc}
 *  * Has two fields in addition to its subclass' fields. To construct the bus, it needs
 * width and height of the car which is given 220 and 120.
 */
public class Bus extends Vehicle{
	
	/**
	 * The default body width of the bus
	 */
	private int width=220;
	
	/**
	 * The default body height of the bus
	 */
	private int height=120;
	
	/**
	 * Constructs a new Bus. The location of the bus is given by the parameters. 
	 * 
	 * @param objX the x coordinate of the bus
	 * @param objY the y coordinate of the bus
	 */
	public Bus(int objX, int objY) {
		addBody(objX, objY);
		addWindows(objX, objY);
		addWheels(objX, objY);
		addLabel(objX, objY);
	}
	
	/**
	 * {@inheritDoc}
	 */	
	public void addBody(int objX, int objY){
		body = new GRect(width, height);
		body.setFillColor(Color.RED);
		body.setFilled(true); 
		add(body, objX, objY);
	}
	
	/**
	 * {@inheritDoc}
	 */	
	public void addWindows(int objX, int objY){
		windows = new GRect[2];
		windowLength = 35;
		for (int i=0; i<2; i++) {
			windows[i] = new GRect(windowLength,windowLength);
			windows[i].setFillColor(Color.WHITE);
			windows[i].setFilled(true); 
		}
		add(windows[0], objX+(width-2*windowLength)/3, objY+10);
		add(windows[1], objX+windowLength+2*(width-2*windowLength)/3, objY+10);
	}
	
	/**
	 * {@inheritDoc}
	 */	
	public void addWheels(int objX, int objY){
		wheels = new GOval[4];
		wheelCircle = 30;
		for (int i=0; i<4; i++) {
			wheels[i] = new GOval(wheelCircle,wheelCircle);
			wheels[i].setFilled(true); 
			wheels[i].setColor(Color.WHITE);
			wheels[i].setFillColor(Color.BLUE);
			
		}
		add(wheels[0], objX+(width-4*wheelCircle)/5, objY+height-10);
		add(wheels[1], objX+wheelCircle+2*(width-4*wheelCircle)/5, objY+height-10);
		add(wheels[2], objX+wheelCircle*2+3*(width-4*wheelCircle)/5, objY+height-10);
		add(wheels[3], objX+wheelCircle*3+4*(width-4*wheelCircle)/5, objY+height-10);
	}
	
	/**
	 * {@inheritDoc}
	 */	
	public void addLabel(int objX, int objY){
		label = new GLabel("BUS");
		label.setFont(new Font("Arial", Font.BOLD, 18));
		label.setColor(Color.WHITE);
		add(label, objX+90, objY+60);
	}
	/**
	 * Sets the direction to 1 for right or -1 for left. The direction
	 * is given in a parameter.
	 * 
	 * Makes available to change the direction without reaching the fields of this class.
	 * 
	 * @param direction
	 */
	public void setDirection(int direction){
		this.direction=direction;
	}
	/**
	 * Sets the lane to 1 or 2 or 3 or 4. The lane is given in a parameter.
	 * 
	 * Makes available to change the lane without reaching the fields of this class.
	 * 
	 * @param lane
	 */
	public void setLane(int lane){
		this.lane=lane;
	}
	
	
}
