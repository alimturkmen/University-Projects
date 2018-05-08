/*
Student Name: Yaşar Alim Türkmen
Student Number: 2014400165
Project Number: 1
Operating System: Linux
Compile Status: Compiles correctly
Program Status: Gives output correctly
Notes: Anything you want to say about your code that will be helpful in the grading process.

*/

#include "BigInteger.h"
#include <algorithm>

BigInteger::BigInteger(int number){
    num = new LinkedList;
    while(number>0) {
        int i = number % 10; //digit number
        num->pushTail(i);
        number = number / 10;
    }
}

BigInteger::BigInteger(const string& bigInteger){
    num = new LinkedList;
    string s = bigInteger;
    int size = s.size();
    for(int i=0; i<size; i++) {
        string temp = s.substr(s.size()-1,1); //the number in the last digit
        num->pushTail(stoi(temp));
        s = s.substr(0,s.size()-1);
    }

}

BigInteger BigInteger::operator+(const BigInteger &list){

    BigInteger ret; // will be equal to sum of the bigintegers.

    LinkedList *list1 = num;
    LinkedList *list2 = list.num;

    LinkedList list3 = *list1 + *list2; // the linkedlist which biginteger's linkedlist pointer points
    Node *node = list3.head; //the iterating node

    while(node){
        if(node->data>=10){
            int remain = node->data % 10; // remaining number after refreshing the digit on the left
            if(node->next) {
                int k = node->data/10;
                node->data = remain;
                node->next->data = node->next->data + k;
            }
            else{
                node->data = remain;
                list3.pushTail(1);
            }
        }
        node = node->next;
    }
    *ret.num=list3;
    return ret;
}

BigInteger BigInteger::operator*(const BigInteger &list){

    BigInteger ret;

    LinkedList* list1 = num;
    LinkedList* list2 = list.num;
    LinkedList list3;

    Node* node1 = list1->head;
    Node* node2 = list2->head;

    Node *node3 = list3.head;
    int j=0; // to go to next digit in the multiplying process
    while(node1) {
        while (node2) {
            int temp = node1->data * node2->data; // the product
            if (node3){
                node3->data += temp;
            }else{
                list3.pushTail(temp);
                node3=list3.tail;
            }
            node2 = node2->next;
            node3 = node3->next;
        }
        node3 = list3.head;
        j++;
        for(int i=0; i<j; i++)
            node3 = node3->next;

        node2 = list2->head;
        node1 = node1->next;
    }
    // same process above
    Node *node = list3.head;

    while(node){
        if(node->data>=10){
            int remain = node->data % 10;
            int k = node->data/10;
            if(node->next) {
                node->data = remain;
                node->next->data = node->next->data + k;
            }
            else{
                node->data = remain;
                list3.pushTail(k);
            }
        }
        node = node->next;
    }
    *ret.num=list3;
    return ret;
}

BigInteger BigInteger::operator*(int i){

    BigInteger big = BigInteger(i);
    return *this*big;

}

BigInteger::BigInteger(const BigInteger &other){
    num = new LinkedList;
    *num=*other.num;
    cout<<"called"<<endl;
}
BigInteger &BigInteger::operator=(const BigInteger &list){
    *num = *list.num ;
    return *this;
}
BigInteger::~BigInteger(){
    if(num){delete num;}

}


/*ostream &operator<<(ostream &out, const BigInteger &bigInteger)  {
    string str = "";
    Node *head = bigInteger.num->head;
    while (head) {
        str += to_string(head->data);
        head = head->next;
    }
    reverse(str.begin(), str.end());
    if (str == "")
        str = "0";
    out << str;
    return out;
}*/
