#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

typedef int TypeVal;

int main(){
	TypeVal orden = 10000;
	TypeVal k = orden - 1;
	TypeVal val = 0;
	vector<TypeVal> generators;
	vector<TypeVal> ord;
	int numOfGenerators = 2;
	for(TypeVal i = 1; i < orden; i++){
		for(TypeVal j = 1; j < orden; j++){
			val = pow(i,j);
			if(val % orden == 1 and j == k){
				generators.push_back(i);
				if(generators.size() == numOfGenerators) break;
			}
			else if(val % orden == 1) break;
		}
	}
	if(generators.size() == 0) cout<<"No es ciclico"<<endl;
	else{
		for(TypeVal g : generators){
			cout<<g<<endl;
		}	
	}
}