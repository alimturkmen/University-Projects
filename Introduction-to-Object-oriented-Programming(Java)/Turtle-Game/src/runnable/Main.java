package runnable;

import java.util.ArrayList;
import visualization.Board;
import visualization.Car;
import visualization.Bus;  
import acm.graphics.GCompound;
import java.util.*;
import java.util.Random;
import visualization.Vehicle;
import java.util.*;
import java.io.*;

/**
 * Creates and triggers the execution of the game.
 * 
 * The implementation of the whole process of the game.
 * 
 * The game consists of vehicles (bus and car) and a turtle. The aim of the game is get the turtle to the opposite side
 * and turn back to safe zone by using arrow keys. There are vehicles moving left and right. The types, directions
 * and lanes of the vehicles are determined randomly. When a vehicle hits the the turtle, the game is over. 
 * 
 * Asks for a name before starting the game to get the user name and calculates the score. As round number gets greater
 * vehicles moves faster and probability of creation of vehicles increases. 
 * 
 * There are two fields: board which is game played on, vehicles which stores the all vehicles on the board.
 * @author alim
 *
 */
public class Main {
	
	/**
	 * The board provides the game screen
	 */
	public static Board board;
	
	/**
	 * Contains all the created vehicles
	 */
	public static ArrayList<Vehicle> vehicles ;
	
	/**
	 * Contains the main loop of the game.
	 * 
	 * Gets a name from the user and creates the board with 1040 pixel width and 730 pixel height
	 * In the loop new vehicles are produced and they are added to arraylist. Then the vehicles move.
	 * If any vehicle hits the turtle game is over otherwise the loop keeps executing. 
	 * Before ending the loop updates the round and score.
	 * 
	 * After the loop, if the user manage to make a greater score than the ones in the highscores table,
	 * highscores table is recreated.
	 * 
	 * @param args
	 * @throws FileNotFoundException
	 */

	public static void main (String[] args) throws FileNotFoundException{
		
		Scanner console = new Scanner(System.in);
		String name = console.next();

		vehicles = new ArrayList<Vehicle>();
		board = new Board("Sprinter Turtle", 1040, 730);

		// The main loop of the game
		
		boolean gameOver = false;
		
		while(!gameOver){
			
			Vehicle newVehicle = createVehicle();
			if(newVehicle!=null)
			vehicles.add(newVehicle);
			for(int i = 0; i<vehicles.size(); i++){
				board.addObject(vehicles.get(i));
			}
			
			moveVehicles();

			board.waitFor(30);
			if(checkForCollision()){
				gameOver=true;
			}
			update(board.checkRound);
			
		}
		updateHighscores(name);
}
	/**
	 * Moves each vehicle on the arraylist one step in their corresponding direction and
	 * also removes the vehicles that are out of the board.
	 * 
	 * Speed of the vehicles increases as the round number goes up.
	 * The vehicles out of the board are both removed from arraylist and the board.
	 */
	private static void moveVehicles() {
		for(int i=0; i<vehicles.size(); i++){
			if(vehicles.get(i).getDirection()==-1){
				vehicles.get(i).move(-0.5-board.round*0.5, 0);
			}
			if(vehicles.get(i).getDirection()==1){
				vehicles.get(i).move(0.5+board.round*0.5, 0);		
			}
			if(vehicles.get(i).getX()>1000 || vehicles.get(i).getX()<-vehicles.get(i).getWidth()+40){
				vehicles.get(i).removeAll();
				vehicles.remove(i);
			}
		}
	}

	/**
	 * Creates new vehicle checking the already created ones.
	 * Creation, type and lane of the vehicle are decided randomly.
	 * 
	 * Once the vehicle created, if the lane is not available (occupied with some other vehicle),
	 * the newly created one is discarded.
	 * 
	 * The probability of the creation of the vehicles increases as the round number goes up.
	 * @return vehicle to be added to the board
	 */
	private static Vehicle createVehicle() {
		
		double createNew = Math.random();
		double createNew2 = Math.random();
		double createNew3 = Math.random();
		double createNew4 = Math.random();
		if(createNew<0.99-0.005*board.round){
			return null;
		}
		if(createNew2>0.5){
			Bus newVeh = new Bus(0,0);
			
			if(createNew3<0.125){
				newVeh.setLocation(0,20);
				newVeh.setLane(1);
			}else if(createNew3<0.25){
				newVeh.setLocation(0,180);
				newVeh.setLane(2);
			}else if(createNew3<0.375){
				newVeh.setLocation(0,340);
				newVeh.setLane(3);
			}else if(createNew3<0.5){
				newVeh.setLocation(0,500);
				newVeh.setLane(4);
			}else if(createNew3<0.625){
				newVeh.setLocation(820,20);
				newVeh.setLane(1);
			}else if(createNew3<0.75){
				newVeh.setLocation(820,180);
				newVeh.setLane(2);
			}else if(createNew3<0.875){
				newVeh.setLocation(820,340);
				newVeh.setLane(3);
			}else {
				newVeh.setLocation(820,500);
				newVeh.setLane(4);
			}
			if(createNew4>0.5)
				newVeh.setDirection(1);
			else
				newVeh.setDirection(-1);
			
			for(int i=0; i<vehicles.size(); i++){
				if(vehicles.get(i).getBounds().contains(newVeh.getX(), newVeh.getY()+55) ||
						vehicles.get(i).getBounds().contains(newVeh.getX()+newVeh.getWidth(), newVeh.getY()+55) ||
						vehicles.get(i).getBounds().contains(newVeh.getX()+newVeh.getWidth()/2, newVeh.getY()+55)
					)
					return null;
			}
			return newVeh;
			
		}else{
			Car newVeh = new Car(0,0);
			
			if(createNew3<0.125){
				newVeh.setLocation(0,70);
				newVeh.setLane(1);
			}else if(createNew3<0.25){
				newVeh.setLocation(0,230);
				newVeh.setLane(2);
			}else if(createNew3<0.375){
				newVeh.setLocation(0,390);
				newVeh.setLane(3);
			}else if(createNew3<0.5){
				newVeh.setLocation(0,550);
				newVeh.setLane(4);
			}else if(createNew3<0.625){
				newVeh.setLocation(870,70);
				newVeh.setLane(1);
			}else if(createNew3<0.75){
				newVeh.setLocation(870,230);
				newVeh.setLane(2);
			}else if(createNew3<0.875){
				newVeh.setLocation(870,390);
				newVeh.setLane(3);
			}else {
				newVeh.setLocation(870,550);
				newVeh.setLane(4);
			}
			if(createNew4>0.5)
				newVeh.setDirection(1);
			else
				newVeh.setDirection(-1);
			
			for(int i=0; i<vehicles.size(); i++){
				if(vehicles.get(i).getBounds().contains(newVeh.getX(), newVeh.getY()+55) ||
						vehicles.get(i).getBounds().contains(newVeh.getX()+newVeh.getWidth(), newVeh.getY()+55) ||
						vehicles.get(i).getBounds().contains(newVeh.getX()+newVeh.getWidth()/2, newVeh.getY()+55)
					)
					return null;
			}
			return newVeh;
		}
	}
	/**
	 * Checks whether vehicles collide with each other or the turtle.
	 * 
	 * Checks for the vehicles that are in the same lane and opposite directions. 
	 * If any collision is detected between vehicles, reverses the direction of both vehicles.
	 * If the turtle is hit by any vehicle returns true.
	 * @return a boolean if any collision occurs between the vehicles and the turtle
	 */
	private static boolean checkForCollision(){
		for(int i=0; i<vehicles.size(); i++){
			Vehicle tempVeh = vehicles.get(i);
			if(tempVeh.contains(board.getTurtle().getX(), board.getTurtle().getY()) || 
				tempVeh.contains(board.getTurtle().getX()+board.getTurtle().getWidth(), board.getTurtle().getY())||
				tempVeh.contains(board.getTurtle().getX(), board.getTurtle().getY()+board.getTurtle().getHeight())||
				tempVeh.contains(board.getTurtle().getX()+board.getTurtle().getWidth(), board.getTurtle().getY()+board.getTurtle().getHeight()))
				return true;
			for(int j=i+1; j<vehicles.size(); j++){
				Vehicle tempVeh2 = vehicles.get(j);
				if(tempVeh.getLane()==tempVeh2.getLane() && (
					tempVeh.getBounds().contains(tempVeh2.getX()-3,tempVeh2.getY()+55) ||
					tempVeh.getBounds().contains(tempVeh2.getX()+tempVeh2.getWidth()+3,tempVeh2.getY()+55))){
					if(tempVeh instanceof Car)
						((Car)tempVeh).setDirection(-tempVeh.getDirection());
					else if(tempVeh instanceof Bus)
						((Bus)tempVeh).setDirection(-tempVeh.getDirection());
					if(tempVeh2 instanceof Car)
						((Car)tempVeh2).setDirection(-tempVeh2.getDirection());
					else if(tempVeh2 instanceof Bus)
						((Bus)tempVeh2).setDirection(-tempVeh2.getDirection());
				}
			}
		}
		return false;
	}
	/**
	 * Updates the round number and the score made by player.
	 * 
	 * First, checks whether the turtle reaches the opposite side before gets back the safezone.
	 * Take a parameter to check the condition
	 * Then increases the round by one for each turn.
	 * Also arranges the score according to round.
	 * Finally adds round number and score to board.
	 * 
	 * @param num
	 */
	private static void update(int num){
		
		if(num==1 && board.getTurtle().getY()<= 0){
			board.checkRound=0;
		}else if(num== 0 && board.getTurtle().getY() >= 640){
			board.round ++;
			board.checkRound=1;
			board.score += board.round*2+Math.pow(board.round,2);
		}
		board.setLabel();
		
	}
	/**
	 * Updates the highscores table made by players.
	 * 
	 * Lists the top 10 score and the user names by decreasing scores. 
	 * Takes the user name from the parameter.
	 * Reads the file created for top 10 scores and compares the score made by
	 * the user with these scores. Adds that score if it is greater than any of the scores in the list
	 * and the user name.
	 * 
	 * @param name
	 * @throws FileNotFoundException incase the file does not exist
	 */
	private static void updateHighscores(String name) throws FileNotFoundException{
		
		File HighScores = new File("HighScores.txt");
		if(!HighScores.isFile()){
			PrintStream pt = new PrintStream(HighScores);
		}
		Scanner input = new Scanner(HighScores);
		input = new Scanner(HighScores);
		ArrayList<Integer> scoresList = new ArrayList<Integer>();
		ArrayList<String> names = new ArrayList<String>();
	
		while(input.hasNext()){
			input.next();
			names.add(input.next());
			int score = input.nextInt();
			scoresList.add(score);
		}
		
		boolean test = true;
		for(int i=0; i<scoresList.size(); i++){
			if(board.score>scoresList.get(i)){
					scoresList.add(i,board.score);
					names.add(i,name);
					test = false;
					break;
				}
		}
		if(test)
			scoresList.add(board.score);
			names.add(name);
		PrintStream pt = new PrintStream(HighScores);
		for(int i=0; i<Math.min(scoresList.size(),10); i++){
			pt.println((i+1)+". \t" + names.get(i) + "\t" + scoresList.get(i));
		}
	}
}