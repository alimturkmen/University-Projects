/*
Student Name: Yaşar Alim Türkmen
Student Number: 2014400165
Project Number: 4
Operating System: Linux
Compile Status: It compiles correctly
Program Status: It give output correctly
Notes: Anything you want to say about your code that will be helpful in the grading process.

*/

#include <iostream>
#include <string>
#include <algorithm>
#include <fstream>
#include <queue>

using namespace std;

class DisjointSet;
struct Edge;
int N, D;
priority_queue<Edge> edges;
vector<int> districts;

class DisjointSet{
public:

    int* arr;
    DisjointSet(int size){

        arr = new int[size];
        // Make each node a root.
        for (int i = 0; i < size; ++i) {
            arr[i] = -1;
        }
        for(int i=0; i<D; i++) {
            arr[districts[i]] = INT16_MAX;
        }
    }
    int find(int set){

        if(arr[set] == INT16_MAX || arr[set]<0){
            return set;
        }
        else{
            // Call find with its root.
            return find(arr[set]);
        }
    }
    void Union(int set1,int set2) {
//        set1 = find(set1);
//        set2 = find(set2);
        if (arr[set1] == INT16_MAX) {
            arr[set2] = INT16_MAX;
        }else if(arr[set2] == INT16_MAX){
            arr[set1] = INT16_MAX;
        }
         else if(arr[set1] > arr[set2]){
                    // First one is less deep, so make its root second.
                    arr[set1] = set2;
                }else if(arr[set1] < arr[set2]){
                    // Vice versa
                    arr[set2] = set1;
                }
         else{
            // They are equal in depth. Set first one as second one's root. (Arbitrarily chosen)
            // And increase the depth.
            arr[set1]--;
            arr[set2] = set1;
        }
    }
    ~DisjointSet(){
        delete []arr;
    }
//
};

struct Edge {
    int n1;
    int n2;
    long long w;
    Edge(int n1_, int n2_, long long w_) {
        n1 = n1_;
        n2 = n2_;
        w = w_;
    }
};

bool operator<(const Edge& e1, const Edge& e2) {
    return e1.w < e2.w;
}

long long kruskal(long long min) {

   // sort(edges.begin(), edges.end());

    DisjointSet ds(N);
    //int k=0;
    for(int i=0; i<N-1; i++){

        int root1 = ds.find(edges.top().n1);
        int root2 = ds.find(edges.top().n2);

        if (ds.arr[root1]==INT16_MAX && ds.arr[root2]==INT16_MAX){
            min = min+ edges.top().w;
//            k++;
//            if(k==D-1)
//                return min;
        }
        else{
            ds.Union(root1,root2);
        }
        edges.pop();

    }
    return min;
}


int main(int argc, char* argv[]) {

    long long min = 0;
    freopen(argv[1], "r", stdin);

    cin >> N;
    cin >> D;

    int n1,n2;
    int w;
    for(int i=0; i<N-1; i++) {
        cin >> n1;
        cin >> n2;
        cin >> w;
        edges.push(Edge(n1,n2,w));
    }

    for(int i=0; i<D; i++) {
        int district;
        cin >> district;
        districts.push_back(district);
    }


    freopen(argv[2], "w", stdout);
    cout <<  kruskal(min);


    return 0;

}






