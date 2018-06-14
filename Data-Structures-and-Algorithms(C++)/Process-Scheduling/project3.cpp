/*
Student Name:Yaşar Alim Türkmen
Student Number:2014400165
Project Number:3
Operating System:Linux
Compile Status:Compiles correctly
Program Status:Gives output correctly
Notes: Anything you want to say about your code that will be helpful in the grading process.

*/

#include <iostream>
#include <queue>
#include <algorithm>
#include <fstream>
#include <iomanip>

using namespace std;


int main(int argc, char* argv[]){

    freopen(argv[1], "r", stdin);

    int N,M;

    cin >> N; // number of vertices
    cin >> M; // number of edges

    int indegree[N];
    double totalTimes[N]; // stores the entire time for each process
    double times[N]; // stores the time for the execution of each process
    vector<vector<int>> graph(N+1);
    int from, to;

    for(int i=0; i<N; i++){
        indegree[i] = 0;

    }
    for(int i=0; i<N; i++){
        double time;
        cin >> time;
        times[i] = time;
        totalTimes[i] = time;
    }

    for(int i=0; i<M; i++) {
        int from;
        int to;
        cin >> from;
        cin >> to;
        graph[from].push_back(to);
        indegree[to]++;
    }

    freopen(argv[2], "w", stdout);

    queue<int> zero_list; //the processes with 0 indegree

    for(int i=0; i<N; i++){
        if(indegree[i]==0){
          zero_list.push(i);
        }
    }

    int cnt = 0;

    while(!zero_list.empty()){
        int node = zero_list.front();
        zero_list.pop();
        cnt++;
        for(int i=0; i<graph[node].size(); i++){
            indegree[graph[node][i]]--;
            if(indegree[graph[node][i]]==0){
                zero_list.push(graph[node][i]);
            }
            if(totalTimes[graph[node][i]]==times[graph[node][i]]){
                totalTimes[graph[node][i]] += totalTimes[node];
            }else{
                if(totalTimes[graph[node][i]]-times[graph[node][i]]<totalTimes[node]){
                    totalTimes[graph[node][i]] = totalTimes[node]+times[graph[node][i]];
                }
            }
        }
    }

    if (cnt<N) cout << -1 << endl; //circle
    else{
        double max=0; // the minimum time to finish all the processes
        for(int i=0; i<N; i++){
            if(totalTimes[i]>max){
                max = totalTimes[i];
            }
        }
        cout<< fixed << std::setprecision(6);
        cout << max << endl;
    }
}
