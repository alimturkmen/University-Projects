	Problem Description and Solution

	We are asked to write a program that finds duplicate files and directories in a given directories. The program also should perform what the command says and search a pattern among the duplicates. 

	The main idea behind the solution is finding the hash of files and directories and if there are files or directories with the same hash, putting those in a list.

	The first challenging part was parsing and reading the arguments. In this part, I benefited from a library called 'argparse'. First, you should say what kind of arguments, the program will receive. After creating an argparse object, you can simply add arguments. 'c' stores one argument, 'p', 'f' and 'd' stores only true if they are given, and 'pandd' stores the rest.
	'pandd' has pattern and directory inside. Hence, first we have to split them. Pattern and directory list do not has to be given, we have to check whether 'pandd' is empty or not. If not, then we have to look whether a pattern is given. 

	If there is a given directory list, it traverses those directories otherwise it traverses the current working directory. While traversing, it appends the directories to 'dirstack' and 'dirlist', and appends the files to 'filelist'. Hence, the directory in the deepest is the one at the top in the stack. In other words, we get a directory tree.

	If -d is given as an argument we have to look for the duplicate directories. I used two dictionaries for this purpose: 'dirs' and 'dirmap'. 'dirs' just stores each of directories' hashes whereas 'dirmap' stores hashes and lists that contains directories with the same hash. So, it is possible to get a directory's hash from 'dirs' and get duplicate directories from 'dirmap'. There is a main while loop, that traverses the directories in 'dirstack'. In each turn, gets a directory, if it is an empty directory calculates the hash of empty string. If it is not, adds hashes of the all content and find the hash of the sum. Then, it stores the hash and directory both in 'dirs' and 'dirmap'. By this way, when the parrent directories try to acces the hash of the child directories, they will just look 'dirs', and 'dirmap' will contain all of the duplicate directories.

	If -f is given or nothing is given, then we have to look for duplicate files. Looking for duplicate files is easier, since we have already a list that contains all of the files. We just have to find the hash values of the files in that list, and put them into a dictionary, 'filemap'.

	At the end, we have duplicate files in 'filemap' or duplicate directories in 'dirmap'. The idea is the same for 'filemap' and 'dirmap'. Each hash value has a list, if there is more than one element in that list means we have duplicate files. After sorting, if -c is given just carries out the command or commands, otherwise prints the duplicates. It also checks whether they match with the pattern.