package visualization;

import acm.graphics.GCompound;
import acm.graphics.GLabel;
import acm.graphics.GOval;
import acm.graphics.GRect;

/**
 * The implementation of the design of a vehicle.
 * 
 * The vehicles is set to have a body part, wheels (can be different in numbers and size), windows, and a label.
 * The body part and windows are rectangle. So they are defined as GRect whereas wheels are defined as GOval.
 * 
 * The fields width and height set the body of the vehicles size.Similarly wheelCircle and windowLength determines the 
 * wheel and window sizes.
 * 
 * The field direction is 1 for the ones moving right, and -1 for the ones moving left
 * There are four lanes on the background image. So the lane is the any value between 1 and 4.
 * 
 * @author alim
 * 
 */
public abstract class Vehicle extends GCompound {
	
	/**
	 * The rectangle body of the vehicle
	 */
	protected GRect body;
	
	/**
	 * The rectangle windows of the vehicle
	 */
	protected GRect[] windows;
	
	/**
	 * The oval wheels of the vehicle
	 */
	protected GOval[] wheels;
	
	/**
	 * The label of the vehicle
	 */
	protected GLabel label;
	
	/**
	 * The width of the body of the vehicle
	 * The height of the body of the vehicle
	 * The length of the windows of the vehicle
	 * The size of the wheels of the vehicle
	 */
	protected int width, height, windowLength, wheelCircle;
	
	/**
	 * The direction the moving vehicle
	 * The lane of the moving vehicle
	 */
	protected int direction, lane;

	/**
	 * Builds the body of the vehicle by given body width and body height and adds
	 * this body on the location which is determined by parameters.
	 * 
	 * @param objX the x coordinate of the body
	 * @param objY the y coordinate of the body
	 */
	public abstract void addBody(int objX, int objY);
	
	/**
	 * Creates the windows of the vehicle by given body width and body height and adds
	 * these windows to the body of the vehicle. 
	 * The number of the windows can be changed according to type of the vehicle.
	 * The location of the body of the vehicle is given by parameters.
	 * 
	 * @param objX the x coordinate of the body
	 * @param objY the y coordinate of the body
	 */
	public abstract void addWindows(int objX, int objY);
	
	/**
	 * Creates the wheels of the vehicle by given body width and body height and adds
	 * these wheels to the body of the vehicle.
	 * The number of the wheels can be changed according to type of the vehicle.
	 * The location of the body of the vehicle is given by parameters.
	 * 
	 * @param objX the x coordinate of the body
	 * @param objY the y coordinate of the body
	 */
	public abstract void addWheels(int objX, int objY);

	/**
	 *Writes the label at the middle of the body of the vehicle.
	 *The location is determined by parameters.
	 * 
	 * @param objX the x coordinate of the body
	 * @param objY the y coordinate of the body
	 */
	
	public abstract void addLabel(int objX, int objY);
	
	/**
	 * Returns the direction of the vehicle since direction is not visible.
	 * @return the direction of the vehicle
	 */
	public int getDirection(){
		return direction;
	}
	/**
	 * Returns the lane of the vehicle since lane is not visible.
	 * @return the lane of the vehicle.
	 */
	public int getLane() {
		return lane;
	}
	
}
