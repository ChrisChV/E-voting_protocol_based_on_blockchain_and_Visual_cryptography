#ifndef UTILS_H
#define UTILS_H

#include <iostream>
#include <crypto++/integer.h>
#include <crypto++/secblock.h>

using namespace std;
using namespace CryptoPP;

namespace Utils{
	void UnsignedIntegerToByteBlock(const Integer& x, SecByteBlock& bytes){
    	size_t encodedSize = x.MinEncodedSize(Integer::UNSIGNED);
    	bytes.resize(encodedSize);
    	x.Encode(bytes.BytePtr(), encodedSize, Integer::UNSIGNED);
	}

	void ByteBlockToUnsignedInteger(SecByteBlock & bytes, Integer & x){
		x.Decode(bytes.BytePtr(), bytes.size(), Integer::UNSIGNED);
	}
}


#endif