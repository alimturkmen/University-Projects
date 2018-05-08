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
    queue<int> instructions;

    Process(string name, int arrivalTime){
        this->name = name;
        this->arrivalTime = arrivalTime;
        instLine = 0;
    }
    Process(){ };
};

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
        while(file2 >> name2){
            file2 >> inst;
            tempProc.instructions.push(inst);
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

    freopen("output.txt", "w", stdout);

    // Main loop of the project. It resumes until there is no process waiting for
    // the CPU. When a process switches, we have to write the ready queue. Thus I used
    // a temporary queue which copies the ready queue.
    // Because the process which is being executed is temporary, as I mentioned above,
    // variable 'p' is used. For detailed information, see readme file.
    queue<Process> tempQueue;
    while(!procQueue.empty()){

       cout << time << "::" << "HEAD-";
       tempQueue = procQueue;
       while(!tempQueue.empty()){
           cout << tempQueue.front().name << "-";
           tempQueue.pop();
       }
         cout << "TAIL" << endl;
        time2 = time;
        p = procQueue.front();
        procQueue.pop();
        while (time-time2 < 100){
            if(p.instructions.empty())
                break;
            p.instLine++;
            time += p.instructions.front();
            p.instructions.pop();
            while(processes.front().arrivalTime <= time && processes.size()>0){
                Process p2 = processes.front();
                procQueue.push(p2);
                processes.pop();
            }
        }
        if(!p.instructions.empty()){
            procQueue.push(p);
        }

        if(!processes.empty() && procQueue.empty()){
            Process proc = processes.front(); processes.pop();
            time = proc.arrivalTime;
            procQueue.push(proc);
        }
    }

    cout << time << "::" << "HEAD--TAIL" <<endl;
    return 0;
}