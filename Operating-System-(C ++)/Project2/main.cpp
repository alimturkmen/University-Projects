#include <iostream>
#include <algorithm>
#include <fstream>
#include <queue>
#include <string>

using namespace std;

// Process stores the name of the process, the arrival time of the process,
// the set of instructions and the line number of the last executed instruction.
struct Process{

    // Name of the process. Ex: P1, P2 etc.
    string name;
    // The arrival time of the process
    int arrivalTime;
    // The line number of the last executed instruction
    int instLine;
    // The set of instructions the process needs
    // It is designed as a pair, the first item is the name of the instruction
    // and the second one is the time required to execute the instruction
    queue<pair<string, int> > instructions;

    Process(string name, int arrivalTime){
        this->name = name;
        this->arrivalTime = arrivalTime;
        instLine = 0;
    }
    Process(){ };

     ~ Process(){

     }
};
// This function allows us to write the elements in the queue into a string
// with a given format. 
// p is the process queue whose elements will be written at given time
// time is the given time.
string writeQueue(queue<Process> p, int time){

    string s = to_string(time);
    s += "::";
    s += "HEAD-";
    if(p.empty()){ s+= "-TAIL \n"; return s;}
    while(!p.empty()){
        s += p.front().name;
        s += "-";
        p.pop();
    }

    s += "TAIL \n";
    return s;
}

int main() {

    //time is used as real time, and time2 is used to measure the passed time time.
    //time2 is the time that the process started being executed.
    //Therefore time-time2 will be used to measure how much time CPU executes a process
    int time=0; int time2;

    // processes is the queue that stores every processes whose arrival time is greater
    // than the real time. When the process comes to CPU, processes pops that process out.
    // In other words this queue looks like the waiting process queue
    queue<Process> processes;

    // procQueue is the queue that stores the arrived processes. In each quantum time
    // interval the first element of the queue is executed and others wait in the queue.
    // It works like a ready queue.
    queue<Process> procQueue;

    // file reads the "definition" file whereas file2 reads the code files.
    ifstream file, file2;
    file.open("definition.txt");

    // Definition file contains the name of the process, the code file of the process
    // and the arrival time of the process respectively.
    // name is the name of the process, code is the code file and arrivalTime is the
    // time that the process arrives as expected.
    string name, code;
    int arrivalTime;

    // This loop takes the necessary parameters from the definition file then creates
    // a Process object with those parameters.In order to form the instruction
    // set of the process, it reads the related code file. Finally, pushes that process to
    // "processes" queue.
    while(file >> name){
        file >> code >> arrivalTime;
        Process tempProc = Process(name, arrivalTime);
        file2.open(code.c_str());
        int inst;
        string name2;
        pair<string, int> tempPair;
        while(file2 >> name2){
            file2 >> inst;
            tempPair.first = name2; tempPair.second = inst;
            tempProc.instructions.push(tempPair);
        }
        processes.push(tempProc);
        file2.close();
    }
    file.close();

    // Pops the first process from the waiting queue, "processes", then ushes the
    // first process to the ready queue, procQueue, since the first one arrives at time=0.
    // this 'p' variable is used for every popped out process, also in the main loop.
    Process p = processes.front();
    processes.pop();
    procQueue.push(p);

    // The array of binary semaphores. Since there is up to 10 resources the array size is 10.
    // For each resource there is an assigned semaphore. All semaphore values are 0 by default
    int semaphores [10];
    for (int i=0; i<10; i++)  semaphores[i] = 0;

   	// For each resource we have a waiting queue. sQueues is the vector that stores these queues.
    vector < queue <Process> > sQueues;
    for(int i=0; i<10; i++) {queue<Process> q; sQueues.push_back(q);}

   	// outputFile is a string that contains the output file's contents.
    string outputFile;

	// Since for each semaphore queue we should have an output file, outputFiles stores the 
	// string parameters that contains those queues' contents.
    vector<string> outputFiles;
    for(int i=0; i<10; i++) {outputFiles.push_back("");}

    // Main loop of the project. It resumes until there is no process waiting for
    // the CPU. When a process switches, we have to write the ready queue. Thus I used
    // a temporary queue which copies the ready queue.
    // Because the process which is being executed is temporary, as I mentioned above,
    // variable 'p' is used. For detailed information, see readme file.
    while(!procQueue.empty()){

        outputFile += writeQueue(procQueue, time);
        time2 = time;
        // p is the process which is being executed 
        p = procQueue.front();

        // wait is the boolean variable which becomes true if the process goes to a semaphore waiting queue.
        bool wait = false;

        while (time-time2 < 100){
            if(p.instructions.empty()){ break;}

           // p.instLine++;
            if(p.instructions.front().second == 0){
            	// inst is the name of the instructor. instr_1, waitS_1 etc.
                string inst = p.instructions.front().first;
               	// sNo is the corresponding semaphore value.
                int sNo = inst.at(inst.size()-1);
                sNo -= 48; // sNo is the ascii value of the integer. This operation gives the integer value
                if(inst.at(0) == 'w'){
                    if(semaphores[sNo] == 1){
                        p.instructions.pop();
                        sQueues[sNo].push(p);
                        outputFiles[sNo] += writeQueue(sQueues[sNo], time);
                        wait = true;
                        break;
                    }
                    else semaphores[sNo] = 1;
                }else{
                    if(!sQueues[sNo].empty()){
                        Process q = sQueues[sNo].front();
                        sQueues[sNo].pop();
                        outputFiles[sNo] += writeQueue(sQueues[sNo], time);
                        procQueue.push(q);
                        semaphores[sNo] = 1;
                        outputFile += writeQueue(procQueue, time);

                    }else semaphores[sNo] = 0;
                }

            }
            time += p.instructions.front().second;
            p.instructions.pop();

            while(!processes.empty() && processes.front().arrivalTime <= time){
                Process p2 = processes.front();
                procQueue.push(p2);
                processes.pop();
            }

        }
        if(!p.instructions.empty() && !wait){
            procQueue.push(p);
        }

        if(!processes.empty() && procQueue.empty()){
            Process proc = processes.front(); processes.pop();
            time = proc.arrivalTime;
            procQueue.push(proc);
        }
        procQueue.pop();
        
    }

    outputFile += writeQueue(procQueue, time);
    // writes the output files.
    freopen("output.txt", "w", stdout);
    cout << outputFile;
    for(int i=0; i<10; i++){
        if(outputFiles[i].size() != 0){
            string title = "output_" + to_string(i) + ".txt";
            freopen(title.c_str(), "w", stdout);
            cout<< outputFiles[i];
        }
    }

    return 0;
}
