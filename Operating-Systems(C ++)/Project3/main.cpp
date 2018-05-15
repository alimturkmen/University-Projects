#include <iostream>
#include <algorithm>
#include <fstream>
#include <queue>
#include <string>

using namespace std;

// These two global variables are the caches. Both of them start with -1 which indicates they are empty
// at the beginning. cache1 stores the most recently used block.
int cache1 = -1;
int cache2 = -1;

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

// This function updates caches. The most recently used block is stored in cache1 and the other is stored in
// cache2. When a new block arrives the cache contents are updated accordingly.
void cacheUpdate(int block){
    if(cache1 == -1){
        cache1 = block;
    }else if(cache1 != block){
        cache2 = cache1;
        cache1 = block;
    }
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

    // outputFile is a string that contains the output file's contents.
    string outputFile, outputFile10, outputFile11, outputFile12;

    // printerQueue0 is the queue of the first printer
    // printerQueue1 is the queue of the second printer
    queue<Process> printerQueue0;
    queue<Process> printerQueue1;
    //ptQueue0 is the queue that stores the execution time and the arrival time of the process that
    // goes to printerQueue0. First pair is the execution time and the second is the arrival time to
    // the queue of the first printer. ptQueue1 is same as ptQueue0.
    queue<pair<int, int> > ptQueue0;
    queue<pair<int, int> > ptQueue1;

    //blockQueue is the queue that stores the block number that misses the cache.
    queue<int> blockQueue;

    //hdQueue is the queue of the hard driver
    //hd is the queue that stores the execution time and the arrival time of the process that goes to hdQueue.
    //First pair is the execution time and the second is the arrival time to the queue of the hard driver
    queue<Process> hdQueue;
    queue<pair<int, int> >hd;

    //io is true for the io instructions which indicates the process either goes to printQueue0,1 or hdQueue.
    bool io;


    // Main loop of the project. It resumes until there is no process waiting for
    // the CPU. When a process switches, we have to write the ready queue. Thus at each switch time
    // current ready queue is added to outputFile.
    // Because the process which is being executed is temporary, as I mentioned above,
    // variable 'p' is used.
    // Each instruction of the process is executed one by one. If the following instruction is
    // dispm then the process is sent to either printQueue0 or printQueue1. The execution time of the
    // instruction and the time it is sent to printer queue is stored in ptQueue also.
    // If the following instruction is readm then the contents of the caches are checked.
    // If we have that block in our cache then nothing is done, just the cache is updated. Otherwise, the
    // block is sent to the hard driver queue. Again the execution time of the instruction and arrival time
    // to the hard drive queue is stored in hd.

    
    // For detailed information, see readme file.
    while(!procQueue.empty()){
        io = false;
        outputFile += writeQueue(procQueue, time);
        // p is the process which is being executed
        p = procQueue.front();
        time2 = time;
        while (time-time2 < 100){
            if(p.instructions.empty()){ break;}
            p.instLine++;
            string inst = p.instructions.front().first;
            int duration = p.instructions.front().second;
            p.instructions.pop();

            if(inst.at(0)=='d'){
                io = true;
                if(( inst.at(inst.size()-1)-48 )==0){
                    ptQueue0.push(make_pair(duration, time));
                    printerQueue0.push(p);
                    outputFile10 += writeQueue(printerQueue0, time);

                }else{
                    ptQueue1.push(make_pair(duration, time));
                    printerQueue1.push(p);
                    outputFile11 += writeQueue(printerQueue1, time);
                }
                break;


            }else if(inst.at(0) == 'r'){
                string blockstr = inst.substr(6, inst.size());
                int block = stoi(blockstr);
                if(cache1 == block || cache2 == block){
                    cacheUpdate(block);
                }else{
                    io = true;
                    hdQueue.push(p);
                    outputFile12 += writeQueue(hdQueue, time);
                    hd.push(make_pair(duration,time));
                    blockQueue.push(block);
                    break;
                }


            }else{
                time += duration;
                while(!printerQueue0.empty() && ptQueue0.front().first <= time-ptQueue0.front().second){
                    Process p2 = printerQueue0.front();
                    procQueue.push(p2);
                    printerQueue0.pop();
                    outputFile10 += writeQueue(printerQueue0, time);
                    ptQueue0.pop();
                    if(!printerQueue0.empty()){
                        ptQueue0.front().second = time;
                    }
                }
                while(!printerQueue1.empty() && ptQueue1.front().first <= time-ptQueue1.front().second){
                    Process p2 = printerQueue1.front();
                    procQueue.push(p2);
                    printerQueue1.pop();
                    outputFile11 += writeQueue(printerQueue1, time);
                    ptQueue1.pop();
                    if(!printerQueue1.empty()){
                        ptQueue1.front().second = time;
                    }
                }
                while(!hdQueue.empty() && hd.front().first <= time-hd.front().second){
                    Process p2 = hdQueue.front();
                    procQueue.push(p2);
                    hdQueue.pop();
                    outputFile12 += writeQueue(hdQueue, time);
                    hd.pop();
                    int block = blockQueue.front();
                    cacheUpdate(block);
                    blockQueue.pop();
                    if(!hdQueue.empty()){
                        hd.front().second = time;
                    }
                }
                while(!processes.empty() && processes.front().arrivalTime <= time){
                    Process p2 = processes.front();
                    procQueue.push(p2);
                    processes.pop();
                }
            }


        }
        if(!p.instructions.empty() && !io){
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

    //This part writes the content evolution of the each queue.
    if(!outputFile.empty()){
        freopen("output.txt", "w", stdout);
        cout << outputFile;
    }
    if(!outputFile10.empty()){
        freopen("output_10.txt", "w", stdout);
        cout << outputFile10;
    }
    if(!outputFile11.empty()){
        freopen("output_11.txt", "w", stdout);
        cout << outputFile11;
    }
    if(!outputFile12.empty()){
        freopen("output_12.txt", "w", stdout);
        cout << outputFile12;
    }
    return 0;
}