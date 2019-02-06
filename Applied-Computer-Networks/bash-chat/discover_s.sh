ALLOF=$(ifconfig | grep "192.168")
HOME=$(echo $ALLOF | cut -f 2 -d " " | cut -f 2 -d ":")
OFFSET=$(echo $HOME | cut -f 4 -d ".")

read -p "Please enter a name. " USERNAME

while true; do
	for i in {1..256}
	do
		DESTIP="192.168.1.$i"
		DISMSG="0;$HOME;$USERNAME;$DESTIP;"
		if [ $i != $OFFSET ]
		then
			echo $DESTIP
			echo $DISMSG | nc $DESTIP 5000
		fi
	done
	sleep 1m
done
