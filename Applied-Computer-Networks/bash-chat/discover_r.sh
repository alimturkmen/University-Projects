ALLOF=$(ifconfig | grep "192.168")
HOME=$(echo $ALLOF | cut -f 2 -d " " | cut -f 2 -d ":")

read -p "Please enter a name. " USERNAME
while true; do

	MSG=$(nc -l $HOME 5000)
	TYPE=$(echo $MSG | cut -f 1 -d ";")

	if [ "$TYPE" == 0 ]
	then

		
		IP=$(echo $MSG | cut -f 2 -d ";")
		NAME=$(echo $MSG | cut -f 3 -d ";")

		DISMSG="1;$HOME;$USERNAME;$IP;$NAME"
		echo $DISMSG | nc $IP 5000

		if ! [ -e ip_name_list ]
		then
			touch ip_name_list
		fi

		if grep -q $IP ip_name_list
		then
			echo "already exists"
		else
			echo "$NAME:$IP" >> ip_name_list
		fi

	fi

done