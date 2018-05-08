#include <boost/mpi.hpp>
#include <iostream>
#include <fstream>
#include <string>
#include <boost/serialization/string.hpp>
#include <algorithm>

namespace mpi = boost::mpi;
using namespace mpi;
using namespace std;
int main() {
    environment env;
    communicator world;

    //the process with pid number =0 is selected as the master
    if(world.rank()==0) {
        ifstream file;
        file.open("speech_tokenized.txt");
        /*-speechTokenized is the vector of vector of strings. Each vector of strings is
        going to be sent to the slave processes.
        -token is the string that is read from the file
        -final is the vector that stores all the words in a sorted manner */
        vector<vector<string>> speechTokenized;
        string token;
        vector<string> final;
        /* If there is only master process, it doesn't send anything, does the job by itself. */
        if(world.size()==1){
            while(file >> token) {
                final.push_back(token);
            }
            sort(final.begin(), final.end());
        }
        else{/*
            -procNum is the number of slave processes
            -wordNum is for equally distributing the words to the slave processes*/
            int procNum = world.size() - 1;
            int wordNum = 0;
            /* This part reads the words from the file. Each word is sent to a vector*/
            while (file >> token) {
                int n = wordNum % procNum;
                vector<string> vTemp;
                speechTokenized.push_back(vTemp);
                speechTokenized[n].push_back(token);
                wordNum++;
            }
            /* Each vector of words sent to corresponding process */
            for (int i = 0; i < procNum; i++) {
                world.send(i + 1, 0, speechTokenized[i]);
            }

            /* Sorted word groups are taken from slave processes one by one and combined in final vector */
            for (int i = 0; i < procNum; i++) {
                vector<string> tempV;
                vector<string> sortedTokens;
                world.recv(i + 1, i + 1, sortedTokens);
                merge(sortedTokens.begin(), sortedTokens.end(), final.begin(), final.end(), back_inserter(tempV));
                final = tempV;
            }
        }
        /*Name of the output file is "output.txt" */
        freopen("output.txt", "w", stdout);
        /*size is the total number of words in the speech*/
        int size = final.size();
        /*reducedMap is the map stores all the words with their number of occurences in the speech */
        vector<pair<string, int> > reducedMap;
        /* This loop counts the number of occurences each words.
           All words are stored in final in ascending order. Takes one of the words and increases counter
           by one until it meets another word. Hence, counter becomes the frequency of that word.
           Then the word and its frequency is stored in reducedMap.
           Each word is printed with its frequnecy. */
        for (int i = 0; i < size; i++) {
            string token = final[i];
            int counter = 1;
            int ind = i;
            for (int j = i + 1; token.compare(final[j]) == 0; j++) {
                counter++;
                ind = j;
                if (j + 1 == size) break;
            }
            i = ind;
            reducedMap.push_back(make_pair(token, counter));
            cout << token << ", " << counter << endl;
        }
    }
    //other processes are slave processes
    else{
        /*id is the rank of the process. tokens is the vector of words that is going to be sorted
         tokens is sorted and sent to the master process*/
        int id= world.rank();
        vector<string> tokens;
        world.recv(0, 0, tokens);
        sort(tokens.begin(), tokens.end());
        world.send(0, id, tokens);
    }

    return 0;
}
