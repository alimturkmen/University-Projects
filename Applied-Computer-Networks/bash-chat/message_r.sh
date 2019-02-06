ALLOF=$(ifconfig | grep "192.168")
HOME=$(echo $ALLOF | cut -f 2 -d " " | cut -f 2 -d ":")

if ! [ -d "cypher" ]
then
	mkdir cypher
fi

if ! [ -d "message" ]
then
	mkdir message
fi

while true; do
	
	MSG=$(nc -l $HOME 5001)

	SRC=$(echo $MSG | cut -f 1 -d ";")
	CYPHER=$(echo $MSG | cut -f 2 -d ";")
	MESSAGE=$(echo $MSG | cut -f 3 -d ";")

	NAME=$(cat ip_name_list | grep "$SRC" | cut -f 1 -d ":")

	if [ -e cypher/$SRC ]
	then
		CYPHER2=$(cat cypher/$SRC)
		CYPHER3=$(echo -n "$CYPHER2" | openssl md5 | cut -f 2 -d " ")
		if [ "$CYPHER2" == "$CYPHER" ] || [ "$CYPHER" == "$CYPHER3" ]
		then
			echo "$NAME:$MESSAGE"
			echo -n $CYPHER3 > cypher/$SRC

			echo "$NAME:$MESSAGE" >> message/$SRC
		else
			echo "ALERT, CYPHER MISMATCH !! "

		fi
	else
		echo -n $CYPHER > "cypher/$SRC"	
	fi
	
done
