#include <iostream>
#include <algorithm>
#include <queue>
#include <thread>
#include <fstream>
using namespace std;


struct Task{
    int id;
    double arrivingTime;
    double cpuWork;
    double odWork;
    double waitingTime=0;

    Task(int id, double arrivingTime, double cpuWork, double odWork){
        this->id = id;
        this->arrivingTime = arrivingTime;
        this->cpuWork = cpuWork;
        this->odWork = odWork;
    }
    Task(){ };
};

struct comparatorArrival {
    bool operator() ( Task t1, Task t2) {
        if(t1.arrivingTime==t2.arrivingTime)
            return t1.id > t2.id;
        return t1.arrivingTime > t2.arrivingTime;
    }
};
struct comparatorCpuWork{
    bool operator() ( Task t1, Task t2) {
        if(t1.cpuWork == t2.cpuWork)
            return t1.id > t2.id;
        return t1.cpuWork > t2.cpuWork;
    }
};
struct Cpu {
    int id;
    double frequency;
    bool empty;
    double activeTime;
    Task task;
    Cpu(int id, double frequency){
        this->id = id;
        this->frequency = frequency;
        empty = true;
        activeTime = 0;
    }
};

struct OutputD {
    int id;
    double quantum;
    bool empty;
    double activeTime;
    Task task;
    OutputD(int id, double quantum){
        this->id = id;
        this->quantum = quantum;
        empty = true;
        activeTime = 0;
    }
};

struct Event {
    string type;
    double duration;
    Task task;
    Event(Task task, string type_, double duration_){
        this->task = task;
        type = type_;
        duration = duration_;
    }
};

ostream& operator<<(ostream& os, const Event& e) {
    os <<"event#" << e.task.id << "-" <<e.type<< " - "<<e.duration;
    return os;
}

struct comparatorEvent {
    bool operator() ( Event e1, Event e2) {
        if(e1.duration==e2.duration){
            if(e1.type==e2.type)
                return e1.task.id > e2.task.id;
            if(e1.type=="io")
                return false;
            if(e2.type=="io");
                return true;
        }
        return e1.duration > e2.duration;
    }
};


bool areCpusWorking (vector<Cpu> cpus){
    for(int i=0; i<cpus.size(); i++){
        if(!cpus[i].empty)
           return true;
    }
}
bool emptyCpu ( vector<Cpu> cpus){
    for(int i=0; i<cpus.size(); i++){
        if(cpus[i].empty){return true;}
    }
}
bool areOdsWorking (vector<OutputD> ods){
    bool b = false;
    for(int i=0; i<ods.size(); i++){
        if(!ods[i].empty)
            return true;
    }
}
bool emptyOd ( vector<OutputD> ods){
    for(int i=0; i<ods.size(); i++){
        if(ods[i].empty){return true;}
    }
}


int main(int argc, char* argv[]) {
//    for(int i = 0;i<10;i++) {
//        Event e(i, "cpu", uniRand());
//        events.push_back(e);
//    }
//    0 10 5
//    1 22 20
//    252
//    3 3 50
    freopen(argv[1], "r", stdin);
    int nofCpus;
    cin >> nofCpus;
//    nofCpus = 2;
    vector<Cpu> cpus;
//    cpus.push_back(Cpu(1, 1));
//    cpus.push_back(Cpu(2, 2));
    for (int i = 0; i < nofCpus; i++) {
        double t;
        cin >> t;
        cpus.push_back(Cpu(i+1, t));
    }

    vector<OutputD> ods;
    int nofIos;
    cin >> nofIos;

//    ods.push_back(OutputD(1,5));
//    ods.push_back(OutputD(2,10));
    for(int i=0; i<nofIos; i++){
        double t;
        cin >> t;
        ods.push_back(OutputD(i+1, t));
    }

    priority_queue<Task, vector<Task>, comparatorArrival> tasks;

    int nofTasks;
    cin >> nofTasks;
//    nofTasks = 4;

    for(int i=0; i<nofTasks; i++){
        double arrv;
        double cpuW;
        double oW;
        cin >> arrv;
        cin >> cpuW;
        cin >> oW;
        tasks.push(Task(i+1, arrv, cpuW, oW));
    }
//    for(int i=0; i<10; i++){
//        cout<< tasks.top(). arrivingTime<< "    " << tasks.top().cpuWork << "   " <<
//        tasks.top().odWork<<"   " << endl;
//        tasks.pop();
//    }

//    tasks.push(Task(1,0,10,5));
//    tasks.push(Task(2,1,22,20));
//    tasks.push(Task(3,2,5,2));
//    tasks.push(Task(4,3,3,50));



    priority_queue<Event, vector<Event>, comparatorEvent> events;
//    Event ee (Task(4, 2, 3, 4), "io", 5);
//
//    Event ee2 (Task(2, 2, 3, 4), "io", 5 );
//    events.push(ee2);
//    events.push(ee);
//    cout<< events.top();
//    cout<<endl;
//    for(int i = 1;i<5;i++) {
//        Event e(tasks.top(), "cpu", tasks.top().cpuWork);
//        events.push(e);
//        tasks.pop();
//    }
    queue<Task> odQueue;
    int queue1 = 0;
    int queue2 = 0;

    double now  =0;

    double totalTimes[tasks.size()];
    double waitingTimes[tasks.size()];
    priority_queue<Task, vector<Task>, comparatorCpuWork> cpuQueue;

            Task t1 = tasks.top();
            cpus[0].task = t1;
            cpus[0].empty = false;
            Event efirst(t1, "cpu", t1.cpuWork/cpus[0].frequency+t1.arrivingTime);
            now = t1.cpuWork/cpus[0].frequency+t1.arrivingTime;
            cpus[0].activeTime += t1.cpuWork/cpus[0].frequency;
            waitingTimes[t1.id-1] = (-1)*(t1.cpuWork / cpus[0].frequency)-t1.odWork;
            events.push(efirst);
            tasks.pop();

            int j=tasks.size();
            for(int i=0; i<j; i++){
                if(tasks.top().arrivingTime<now){
                    for(int k=1; k<cpus.size(); k++) {
                        if(cpus[k].empty==true){
                            Event ee (tasks.top(), "cpu", (tasks.top().arrivingTime+tasks.top().cpuWork/cpus[k].frequency));
                            events.push(ee);
                            cpus[k].task = tasks.top();
                            cpus[k].empty= false;
                            cpus[k].activeTime+= tasks.top().cpuWork/cpus[k].frequency;
                            waitingTimes[tasks.top().id-1] = (-1)*(tasks.top().cpuWork / cpus[k].frequency)-tasks.top().odWork;

                           // now = min(now,tasks.top().arrivingTime+tasks.top().cpuWork/cpus[k].frequency);
                        }else{
                            cpuQueue.push(tasks.top());
                            if(cpuQueue.size()>queue1)
                                queue1 = cpuQueue.size();
                            cout<<"queue1 added -- "<< tasks.top().id<<endl;
                        }
                        tasks.pop();
                    }
                }else break;

            }


//


    vector<Task> overQuantum;
    for(int i=0; i<=nofTasks; i++)
        overQuantum.push_back(Task(-1,0,0,0));

    while(!events.empty()) {
        //cout<<"size " << odQueue.size();

        Event top = events.top();
        cout << top << endl;
        now = top.duration;   // declaring seconds.

        totalTimes[top.task.id-1]=now-top.task.arrivingTime;
//        if(top.type=="cpu"){
//            for(int i=0; i<cpus.size(); i++){
//                if (cpus[i].task.id == top.task.id) {
//                    Task t = cpuQueue.top();
//                    cpus[i].empty=true;
//                }
//            }
//        }
        if(top.type=="cpu"){
            for(int i=0; i<cpus.size(); i++){
                if(cpus[i].task.id==top.task.id){
                    cpus[i].empty = true;
                    break;
                }
            }
        }


        if(!tasks.empty()){
            int j= tasks.size();
            for(int i=0; i<j; i++){
                if(tasks.top().arrivingTime<now){
                    if(emptyCpu(cpus) && cpuQueue.empty()) {
                        for(int k =0; k<cpus.size(); k++){
                            if(cpus[k].empty==true) {
                                cpus[k].task=tasks.top();
                                cpus[k].empty=false;
                                Event e(tasks.top(), "cpu", tasks.top().arrivingTime+tasks.top().cpuWork / cpus[k].frequency);
                                events.push(e);
                               // now = min(now,tasks.top().arrivingTime+tasks.top().cpuWork / cpus[k].frequency);
                                // cout<<"added"<<tasks.top().id;
                                waitingTimes[tasks.top().id-1] = (-1)*(tasks.top().cpuWork / cpus[k].frequency)-tasks.top().odWork;
                                break;
                            }
                        }
                    }else{
                        cout<<"queue1 added**"<<tasks.top().id<<endl;
                        cpuQueue.push(tasks.top());
                        if(cpuQueue.size()>queue1)
                            queue1 = cpuQueue.size();
                    }
                    tasks.pop();
                }
                else {break;}
            }
        }
//

        if (top.type == "cpu") {
            if(emptyOd(ods) && odQueue.empty()){
                for(int i=0; i<ods.size(); i++) {
                    if (ods[i].empty) {
                        Task t = top.task;
                        ods[i].task = t;
                        ods[i].empty = false;
                        if(t.odWork<ods[i].quantum || (odQueue.empty() && !areCpusWorking(cpus) && tasks.empty())){
                            Event io_event(t, "io", now+t.odWork);
                            events.push(io_event);
                            ods[i].activeTime += t.odWork;
                        }else{
                            Event io_event(t, "io", now+ods[i].quantum);
                            events.push(io_event);
                            ods[i].activeTime += ods[i].quantum;
                            t.odWork = t.odWork-ods[i].quantum;
                            //     cout<<t.id<< " odwork = " << t.odWork<<endl;
                            overQuantum[io_event.task.id] = t;

                        }
                        break;
                    }
                }
            }else{
                odQueue.push(top.task);
                cout<<"queue 2 added"<< top.task.id<<endl;
                if(odQueue.size()>queue2)
                    queue2 = odQueue.size();
            }

            if(!cpuQueue.empty() && emptyCpu(cpus)){
                for (int i = 0; i < cpus.size(); i++) {
                    if (cpus[i].task.id == top.task.id) {
                        Task t = cpuQueue.top();
                        cpus[i].task = t;
                        cpus[i].empty=false;
                        Event e(t, "cpu", now + t.cpuWork / cpus[i].frequency );
                        cpus[i].activeTime += t.cpuWork / cpus[i].frequency;
                        waitingTimes[cpuQueue.top().id-1] = (-1)*(cpuQueue.top().cpuWork / cpus[i].frequency)-cpuQueue.top().odWork;
                        events.push(e);
                        cpuQueue.pop();
                        break;
                    }
                }
            }else{
                for(int i=0; i<cpus.size(); i++){
                    if(cpus[i].task.id == top.task.id){
                        cpus[i].empty = true;
                        break;
                    }
                }
            }
        }

        else if(!odQueue.empty()){
            if(!overQuantum.empty()){
                for(int i=0; i<overQuantum.size()+1; i++){
                    if(overQuantum[top.task.id].id!=-1){
                        cout<< "queue2 added " << overQuantum[top.task.id].id<<endl;
                        odQueue.push(overQuantum[top.task.id]);
                        overQuantum[top.task.id].id = -1;
                        break;
                    }
                }
            }


            for(int i=0; i<ods.size(); i++){
                if(ods[i].task.id == top.task.id) {
                    Task t = odQueue.front();
                    ods[i].task=t;
                    ods[i].empty = false;
                    odQueue.pop();
                    if(t.odWork<ods[i].quantum || (odQueue.empty() && !areCpusWorking(cpus) && tasks.empty())){
                        Event io_event(t, "io", now+t.odWork);
                        events.push(io_event);
                        ods[i].activeTime += t.odWork;
                    }else{
                        Event io_event(t, "io", now+ods[i].quantum);
                        events.push(io_event);
                        ods[i].activeTime += ods[i].quantum;
                        t.odWork = t.odWork-ods[i].quantum;
                        //     cout<<t.id<< " odwork = " << t.odWork<<endl;

                        overQuantum[io_event.task.id] = t;
                    }
                    break;
                }
            }
        }
        else{
            for(int i=0; i<ods.size(); i++){
                if(ods[i].task.id==top.task.id){
                    ods[i].empty = true;
                }
            }
        }

        events.pop();
    }


    double avgTime;
    for(int i=0; i<nofTasks; i++){
        //cout<<totalTimes[i]<<  " ";
        avgTime+=totalTimes[i];
        waitingTimes[i] += totalTimes[i];
    }
    cout<<endl;

    cout<<avgTime/nofTasks;
    cout<<endl;
    double max=0;
    int odId;
    double max2=0;
    int cpuId;
    for(int i=0; i<ods.size(); i++){
        if(ods[i].activeTime>max){
            max=ods[i].activeTime;
            odId = ods[i].id;
        }
        if(cpus[i].activeTime>max2){
            max2=cpus[i].activeTime;
            cpuId = cpus[i].id;
        }
    }
    cout<<"max cpu Id = "<<cpuId<<endl;
    cout<<"max io Id = "<<odId<<endl;
    cout<<"max queue1 = "<<queue1<<endl;
    cout<<"max queue2 = "<<queue2<<endl;
    cout<<endl;
    double maxWaiting=0;
    double totalWaiting = 0;
    for(int i=0; i<nofTasks; i++){
        //cout<<waitingTimes[i];
        if(waitingTimes[i]>maxWaiting)
            maxWaiting = waitingTimes[i];
        totalWaiting += waitingTimes[i];
//        cout<<endl;
    }
    cout<<"maximum waiting"<< maxWaiting << endl;
    cout<< "average waiting" << totalWaiting/nofTasks ;
    freopen(argv[2], "w", stdout);
    cout<< queue1 <<endl;
    cout<< queue2 << endl;
    cout<< cpuId << endl;
    cout<< odId << endl;
    cout<< totalWaiting/nofTasks <<endl;
    cout<< maxWaiting <<endl;
    cout<< avgTime/nofTasks <<endl;

//    vector<OutputD> temp;
//
//    for(int i=0;i<ods.size(); i++){
//        if(i!=odId-1)
//            temp.push_back(ods[i]);
//    }
//    ods.clear();
//    ods = temp;

//    sort(events.begin(), events.end());
}