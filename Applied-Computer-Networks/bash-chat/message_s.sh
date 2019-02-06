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

read -p "To whom do you want to chat? " DESTNAME

DESTINATION=$(cat ip_name_list | grep "$DESTNAME")
DESTIP=$(echo "$DESTINATION" | cut -f 2 -d ":")

if ! [ -e cypher/$DESTIP ]
then
	CYPHER=$(echo -n 'alim' | openssl md5 | cut -f 2 -d " ")
	echo -n $CYPHER > "cypher/$DESTIP"
fi

while true; do

	read -p "Your message: " MSG
	CYPHER=$(cat "cypher/$DESTIP")
	CYPHER=$(echo -n "$CYPHER" | openssl md5 | cut -f 2 -d " ")
	echo "$HOME;$CYPHER;$MSG" | nc $DESTIP 5001	
	echo -n $CYPHER > "cypher/$DESTIP"
	echo "You:$MSG" >> "message/$DESTIP" 


done
