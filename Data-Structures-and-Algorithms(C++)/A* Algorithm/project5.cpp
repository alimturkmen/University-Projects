/*
Student Name: Yaşar Alim Türkmen
Student Number: 2014400165
Project Number: 5
Operating System: Xubuntu
Compile Status: compiles correctly
Program Status: gives output correctly
Notes: Anything you want to say about your code that will be helpful in the grading process.

*/

#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
#include <queue>

using namespace std;

struct Vertex{
    int id;
    vector<pair<int, int>> adj;
    int h, distance;
    Vertex(int h, int id){
        this->id = id;
        this->h = h;
        distance = INT32_MAX;
    }
};

struct vertexComparator {
    bool operator()(Vertex i, Vertex j) {
        return i.distance + i.h > j.distance+j.h;
    }
};

int main(int argc, char* argv[]) {

    freopen (argv[1],"r+",stdin);

    int V,E;
    scanf ("%d %d", &V, &E);
    vector<Vertex> vertices;
    for(int i=0; i<V; i++){
        int h;
        scanf ("%d", &h);
        vertices.push_back(Vertex(h,i));
    }

    for(int i=0; i<E; i++){
        int n1,n2,w;
        scanf ("%d %d %d", &n1, &n2, &w);
        vertices[n1].adj.push_back(make_pair(n2,w));
        vertices[n2].adj.push_back(make_pair(n1,w));
    }

    int startPoint;
    int endPoint;
    scanf ("%d %d", &startPoint, &endPoint);

    if(vertices[endPoint].h < vertices[startPoint].h) {
        int temp = endPoint;
        endPoint = startPoint;
        startPoint = temp;
    }

    priority_queue<Vertex, vector<Vertex>, vertexComparator> v;

    vertices[endPoint].distance = 0;
    v.push(vertices[endPoint]);
    while(endPoint != startPoint){
        v.pop();

        for(int i=0; i<vertices[endPoint].adj.size(); i++){
            int j=vertices[endPoint].adj[i].first;
            if(vertices[j].distance > vertices[endPoint].distance+vertices[endPoint].adj[i].second){
                vertices[j].distance = vertices[endPoint].distance+vertices[endPoint].adj[i].second;
                v.push(vertices[j]);
            }
        }

        endPoint = v.top().id;
    }
    freopen(argv[2], "w", stdout);
    cout<<vertices[endPoint].distance<<endl;
    return 0;
}
