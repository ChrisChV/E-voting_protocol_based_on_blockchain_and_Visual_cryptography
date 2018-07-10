#ifndef ELGAMALAPI_H
#define ELGAMALAPI_H

#include <iostream>
#include <crypto++/osrng.h>
#include <crypto++/integer.h>
#include <crypto++/elgamal.h>
#include <crypto++/files.h>
#include "../Utils/Utils.h"

using namespace std;

class ElGamalAPI{
	public:
		ElGamalAPI(){};
		ElGamalAPI(int bitsOfKey);
		void generateKeys(int bitsOfKey);
		void savePrivateKey(string fileName);
		void loadPrivateKey(string fileName);
		void savePublicKey(string fileName);
		void loadPublicKey(string fileName);
		void encrypt(Integer & plainText, Integer & cypherText, size_t & plainTextSize);
		void decrypt(Integer & cypherText, Integer & plainText, size_t & plainTextSize);

	private:
		CryptoPP::ElGamalKeys::PrivateKey privateKey;
		CryptoPP::ElGamalKeys::PublicKey publicKey;
		CryptoPP::ElGamal::Decryptor decryptor;
		CryptoPP::ElGamal::Encryptor encryptor;


};

ElGamalAPI::ElGamalAPI(int bitsOfKey){
	generateKeys(bitsOfKey);
	cout<<encryptor.FixedMaxPlaintextLength()<<endl;
}

void ElGamalAPI::generateKeys(int bitsOfKey){
	CryptoPP::AutoSeededRandomPool rng;
	decryptor.AccessKey().GenerateRandomWithKeySize(rng, bitsOfKey);
	privateKey = decryptor.AccessKey();
	encryptor = CryptoPP::ElGamal::Encryptor(decryptor);
	publicKey = encryptor.AccessKey();
}

void ElGamalAPI::savePrivateKey(string fileName){
	privateKey.Save(CryptoPP::FileSink(fileName.c_str(), true).Ref());
}

void ElGamalAPI::loadPrivateKey(string fileName){
	privateKey.Load(CryptoPP::FileSource(fileName.c_str(), true).Ref());
}

void ElGamalAPI::savePublicKey(string fileName){
	publicKey.Save(CryptoPP::FileSink(fileName.c_str(), true).Ref());
}

void ElGamalAPI::loadPublicKey(string fileName){
	publicKey.Load(CryptoPP::FileSource(fileName.c_str(), true).Ref());
}

void ElGamalAPI::encrypt(Integer & plainText, Integer & cypherText, size_t & plainTextSize){
	CryptoPP::AutoSeededRandomPool rng;
	SecByteBlock bytePlainText;	
	Utils::UnsignedIntegerToByteBlock(plainText, bytePlainText);

	if(bytePlainText.size() > encryptor.FixedMaxPlaintextLength()){
		cout<<"El plain text es muy grande "<<bytePlainText.size()<<" "<<encryptor.FixedMaxPlaintextLength()<<endl;
		return;
		//throw("El plainText es muy pequeño"); 
	}
	
	size_t ecl = encryptor.CiphertextLength(bytePlainText.size());
	plainTextSize = bytePlainText.size();
	SecByteBlock byteCypherText(ecl);
	encryptor.Encrypt(rng, bytePlainText, bytePlainText.size(), byteCypherText);

	Utils::ByteBlockToUnsignedInteger(byteCypherText, cypherText);
}

void ElGamalAPI::decrypt(Integer & cypherText, Integer & plainText, size_t & plainTextSize){
	CryptoPP::AutoSeededRandomPool rng;
	SecByteBlock byteCypherText;
	Utils::UnsignedIntegerToByteBlock(cypherText, byteCypherText);
	if(byteCypherText.size() > decryptor.FixedCiphertextLength()){
		cout<<"El cypher text es muy grande "<<byteCypherText.size()<<" "<<encryptor.FixedCiphertextLength()<<endl;
		return;
	}
	SecByteBlock bytePlainText(plainTextSize);
	decryptor.Decrypt(rng, byteCypherText, byteCypherText.size(), bytePlainText);
	Utils::ByteBlockToUnsignedInteger(bytePlainText, plainText);
}

#endif