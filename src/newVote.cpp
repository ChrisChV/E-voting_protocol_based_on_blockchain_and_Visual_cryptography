#include <iostream>
#include <fstream>
#include <cstdlib>
#include "ElGamal/ElGamalAPI.h"

using namespace std;

string CANDIDATES_FILE_PATH = "Conf/candidates";
string NEW_VOTE_FILE_PATH = "newVote";

void getCandidates(vector<Integer> & candidates){
    ifstream candidatesFile(CANDIDATES_FILE_PATH);
    string name = "";
    string candidate = "";
    while(candidatesFile >> name){
        candidatesFile >> candidate;
        candidates.push_back(Integer(candidate.c_str()));
    }
    candidatesFile.close();
}

int main(){
    srand(time(NULL));
    ElGamalAPI elGamalInstance(800);
    PrimeAndGenerator pg;
	AutoSeededRandomPool prng;
    Integer credential;
    pg.Generate(1, prng, 500, 450);
    credential = pg.Prime();
    vector<Integer> candidates;
    getCandidates(candidates);
    int index = rand() % candidates.size();
    size_t sizeCredentials;
    size_t sizeVote;
    Integer cypherCredential;
    Integer cypherVote;
    elGamalInstance.encrypt(credential,cypherCredential,sizeCredentials);
    elGamalInstance.encrypt(candidates[index], cypherVote, sizeVote);
    ofstream voteFile(NEW_VOTE_FILE_PATH);
    voteFile<<cypherCredential<<endl;
    voteFile<<cypherVote<<endl;
    voteFile.close();
    string command = "python ./Blockchain/sendVote.py";
    system(command.c_str());
}
