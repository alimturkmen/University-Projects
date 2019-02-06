package runnable;
import adts.MyDLL;
import adts.MyPQ;
import adts.MyStack;


import java.io.*;
import java.util.*;
/**
 * Reads the corresponding files
 * First locates the waggons to their garages by given information Then applies the mission: Takes the waggons 
 * from the station and the most powerful locomotive, leaves some of the waggons at the middle station and takes
 * new ones from the middle station, at last, puts all the waggons in the waggon garage and the locomotive in the 
 * locomotive garage of the terminal station. The information about this transfer is given by the corresponding files.
 * 
 * @author alim
 *
 */
public class Main {
	/**
	 * 
	 * Calls the simulation method and executes it
	 * @see runSimulation
	 * @param args
	 *
	 */
	public static void main(String[] args){
	
		
		runSimulation("data/dests.txt", "data/waggons.txt", "data/locs.txt", "data/missions.txt", "data/result.txt");	
	}
	
	/**
	 * 
	 * The main method that does all the job.
	 * By given files, creates the locomotive garages, priority queues,  and waggon garages ,stacks, of the stations.
	 * Then creates a train ,a doubly linked list, and gets the most powerful locomotive and attaches the waggons
	 * to the locomotive. After the transfer of waggons writes the last appearance of the garages on a file.
	 * 
	 * @param destsFileName
	 * @param waggonsFileName
	 * @param locsFileName
	 * @param missionsFileName
	 * @param outputFileName
	 * 
	 */
	public static void runSimulation(String destsFileName, String waggonsFileName, 
			String locsFileName, String missionsFileName, String outputFileName){
		// your code goes below	
		try{
			Scanner input1= new Scanner(new File(destsFileName));
			Scanner input2= new Scanner(new File(waggonsFileName));
			Scanner input3= new Scanner(new File(locsFileName));
			Scanner input4= new Scanner(new File(missionsFileName));
			PrintStream pt = new PrintStream(outputFileName);
			ArrayList<String> cities = new ArrayList<String>();
			
			while(input1.hasNext()){
				cities.add(input1.next());
			}
			
			
			ArrayList<MyStack<Waggon>> waggGarages = new ArrayList<MyStack<Waggon>>();
			for(int i=0; i<cities.size(); i++){
				MyStack<Waggon> waggGarage = new MyStack<Waggon>();
				waggGarages.add(waggGarage);
			}
			
			ArrayList<MyPQ<Locomotive>> locGarages = new ArrayList<MyPQ<Locomotive>>();
			for(int i=0; i<cities.size(); i++){
				MyPQ<Locomotive> locGarage = new MyPQ<Locomotive>();
				locGarages.add(locGarage);
			}
			
			while(input2.hasNext()){
				Waggon tempWaggon = new Waggon();
				tempWaggon.name=input2.next();
				tempWaggon.city=input2.next();
				for(int i=0; i<cities.size(); i++){
					if(tempWaggon.city.equals(cities.get(i))){
						waggGarages.get(i).push(tempWaggon);
					}
				}	
			}
			while(input3.hasNext()){
				Locomotive tempLoc = new Locomotive();
				tempLoc.name=input3.next();
				tempLoc.city=input3.next();
				tempLoc.enginePower=input3.nextDouble();
				for(int i=0; i<cities.size(); i++){
					if(tempLoc.city.equals(cities.get(i))){
						locGarages.get(i).offer(tempLoc);
				
					}
				}				
			}
			
			while(input4.hasNext()){
				
				String[] mission = input4.next().split("-");
				String startSt = mission[0];
				String midSt = mission[1];
				String finalSt = mission[2];
				int num1 = Integer.valueOf(mission[3]);
				int num2 = Integer.valueOf(mission[4]);
				String[] indexes = mission[5].split(",");
				int[] index=new int[indexes.length];
				
				for(int i=0; i<indexes.length; i++){
					index[i]=Integer.valueOf(indexes[i]);
				}		
				Arrays.sort(index);
				
				MyDLL<Waggon> train = new MyDLL<Waggon>();
			
				for(int i=0; i<cities.size(); i++){
					if(cities.get(i).equals(startSt)){
						train.add(locGarages.get(i).poll());
						for(int j=0; j<num1; j++){
							train.add(waggGarages.get(i).pop());
						}
					}
				}
				
				for(int i=0; i<cities.size(); i++){
					if(cities.get(i).equals(midSt)){
						ArrayList<Waggon> tempWag = new ArrayList<Waggon>();
						for(int j=index.length-1; j>=0; j--){
							int n = index[j];
							tempWag.add(train.remove(n+1));
						}
						for(int k=0; k<num2; k++){
							train.add(waggGarages.get(i).pop());
						}
						for(int m=tempWag.size()-1; m>=0; m--){
							waggGarages.get(i).push(tempWag.get(m));
						}
					}
				}
		
				for(int i=0; i<cities.size(); i++){
					if(cities.get(i).equals(finalSt)){
						
						Locomotive tempLoc = (Locomotive) train.remove(0);
						locGarages.get(i).offer(tempLoc);
						int n=train.size();
						for(int j=0; j<n; j++){
							waggGarages.get(i).push(train.remove(0));
						}
					}
				}
			}
				
			for(int i=0; i<cities.size(); i++){
				MyStack<Waggon> wg = waggGarages.get(i);
				MyPQ<Locomotive> lg = locGarages.get(i);
				pt.println(cities.get(i));
				int n =wg.count();
				int m= lg.count();
				
				pt.println("Waggon Garage");
				
				for(int j=0; j<n; j++){
					pt.println(wg.pop().name);
				}
				
				pt.println("Locomotive Garage");
				
				for(int j=0; j<m; j++){	 	
					pt.println(lg.poll().name);
				}
				pt.println("---------------");		
			}	
		}catch(FileNotFoundException e){
			System.err.println("File Does Not Exist");
		}
	}
}