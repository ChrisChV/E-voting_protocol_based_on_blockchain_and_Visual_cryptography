#include <iostream>
#include "cryptopp/dh2.h"
#include <cryptopp/osrng.h>
#include <cryptopp/integer.h>
#include <cryptopp/nbtheory.h>
#include "ElGamalAPI.h"

using namespace std;
using namespace CryptoPP;

int main(){

	assert(1 != 2);

	PrimeAndGenerator pg;
	AutoSeededRandomPool prng;
	Integer p, q, g;
	pg.Generate(1, prng, 500, 450); //delta (valor para sacar primos random), randomGenerator, bits in the prime p, bits in the prime q
	p = pg.Prime();
	q = pg.SubPrime();
	g = pg.Generator();

	cout<<p<<endl<<endl;
	cout<<q<<endl<<endl;
	cout<<g<<endl<<endl;

	//SecByteBlock bb;
	//Utils::UnsignedIntegerToByteBlock(p, bb);
	Integer pp;
	//Utils::ByteBlockToUnsignedInteger(bb, pp);
	//cout<<pp<<endl;

	ElGamalAPI egApi(800);

	cout<<"PT->"<<p<<endl;
	cout<<"Cifrado"<<endl;
	size_t si;
	egApi.encrypt(p, pp, si);
	cout<<"CT->"<<pp<<endl;
	cout<<"Descifrado"<<endl;
	Integer res;
	egApi.decrypt(pp, res, si);
	cout<<"PT->"<<res<<endl;

	assert(p.Compare(res) == 0);

	ElGamalAPI api1(800);

	api1.savePrivateKey("test_private");
	api1.savePublicKey("test_public");

	ElGamalAPI api2;
	ElGamalAPI api3;
	Integer rr = p;
	Integer rr2;
	Integer rr3;
	cout<<endl<<"PT->"<<rr<<endl;
	api2.loadPublicKey("test_public");
	api2.loadPrivateKey("test_private");
	size_t sr;
	api2.encrypt(rr, rr2, sr);
	api3.loadPrivateKey("test_private");
	api3.decrypt(rr2, rr3, sr);
	cout<<endl<<"PT->"<<rr3<<endl;

	assert(rr.Compare(rr3) == 0);


	cout<<"Test Completado con exito"<<endl;

}