package runnable;

public class Locomotive extends Waggon implements Comparable<Locomotive> {
	
	/**
	 * The enginePower of the locomotive
	 */
	double enginePower;

	/**
	 * {@inheritDoc}
	 */
	@Override
	public int compareTo(Locomotive loc) {
		if(enginePower>loc.enginePower)
			return 1;
		else if(enginePower<loc.enginePower)
			return -1;
		return 0;
	}
}
