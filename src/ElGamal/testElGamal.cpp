#include <iostream>
#include "crypto++/elgamal.h"
#include "crypto++/dh2.h"
#include <crypto++/osrng.h>
#include <crypto++/integer.h>
#include <crypto++/nbtheory.h>
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

	cout<<"Test Completado con exito"<<endl;

}