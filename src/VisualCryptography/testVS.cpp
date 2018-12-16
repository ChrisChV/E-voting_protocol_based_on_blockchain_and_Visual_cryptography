#include <iostream>
#include <cassert>
#include "VS.h"

using namespace std;

int main(){	
	CryptoPP::AutoSeededRandomPool rng;
	int numOfKeys = 2;
	int numOfShares = 3;
	cout<<palabraSecreta<<endl<<endl;
	vector<Integer> keys;
	VS::generateKeys(numOfKeys, tamPalabra, keys);
	assert(keys.size() == numOfKeys);
	for(Integer i : keys){
		cout<<i<<endl;
	}
	cout<<endl;
	vector<Integer> shares;
	VS::encrypt(palabraSecreta, keys, numOfShares, tamPalabra, shares);
	assert(shares.size() == numOfShares);
	for(Integer i : shares){
		cout<<i<<endl;
	}
	cout<<endl;
	Integer res;
	VS::decrypt(keys, shares, res);
	assert(res.Compare(palabraSecreta) == 0);
	cout<<res<<endl;
	cout<<endl;
	cout<<"Test ejecutado correctamente"<<endl;
}