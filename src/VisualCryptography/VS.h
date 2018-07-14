#ifndef VS_H
#define VS_H

#include <iostream>
#include <vector>
#include <cryptopp/integer.h>
#include <cryptopp/osrng.h>

using namespace std;

using namespace CryptoPP;

namespace VS{
	void generateKeys(int numOfKeys, size_t sizeOfKeys, vector<Integer> & outKeys){
		CryptoPP::AutoSeededRandomPool rng;
		outKeys.clear();
		outKeys.shrink_to_fit();
		for(int i = 0; i < numOfKeys; i++){
			outKeys.push_back(Integer(rng, sizeOfKeys));
		}
	}

	//NumOfShares es el número de shares generados a parte de los keys.
	void encrypt(Integer & input, vector<Integer> & keys, int numOfShares, size_t sizeOfShares, vector<Integer> & shares){
		CryptoPP::AutoSeededRandomPool rng;
		shares.clear();
		shares.shrink_to_fit();
		if(numOfShares <= 0) return;
		shares.insert(shares.begin(), keys.begin(), keys.end());
		Integer lastShare;
		for(int i = 0; i < numOfShares - 1; i++){
			shares.push_back(Integer(rng, sizeOfShares));
		}
		for(auto iter = shares.begin(); iter != shares.end(); ++iter){
			if(iter == shares.begin()){
				lastShare = input;
			}
			lastShare ^= (*iter);
		}
		shares.erase(shares.begin(), shares.begin() + keys.size());
		shares.push_back(lastShare);
	}

	void decrypt(vector<Integer> & keys, vector<Integer> shares, Integer & output){
		shares.insert(shares.begin(), keys.begin(), keys.end());
		for(auto iter = shares.begin(); iter != shares.end(); ++iter){
			if(iter == shares.begin()){
				output = (*iter);
				continue;
			}
			output ^= (*iter);
		}
	}
}



#endif