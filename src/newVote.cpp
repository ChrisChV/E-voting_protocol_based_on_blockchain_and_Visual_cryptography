#include <iostream>
#include <fstream>
#include <cstdlib>
#include "ElGamal/ElGamalAPI.h"
#include "VisualCryptography/VS.h"

using namespace std;

string CANDIDATES_FILE_PATH = "Conf/candidates";
string SERVER_HOSTS_FIlE_PATH = "Conf/serverHosts";
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

int getNumberOfShares(){
    ifstream hostsFiles(SERVER_HOSTS_FIlE_PATH);
    string user = "";
    string ip = "";
    string pass = "";
    string groupId = "";
    int max = -1;
    while(hostsFiles >> user){
        hostsFiles >> ip;
        hostsFiles >> pass;
        hostsFiles >> groupId;
        if(max == -1 || stoi(groupId) > max){
            max = stoi(groupId);
        }
    }
    hostsFiles.close();
    return max;
}

int main(int argc, char ** argv){
    if(argc != 2){
        cout<<"Faltan argumentos <numOfVotes>"<<endl;
        return 0;   
    }
    cout<<"-------Creador de Voto------"<<endl;
    srand(time(NULL));
    string s_votes = argv[1];
    int votes = stoi(s_votes);
    ElGamalAPI elGamalInstance(800);
    PrimeAndGenerator pg;
	AutoSeededRandomPool prng;
    Integer credential;
    vector<Integer> keys;
    VS::generateKeys(1,500,keys);
    cout<<"Obteniendo credenciales..."<<endl;
    pg.Generate(1, prng, 500, 450);
    credential = pg.Prime();
    vector<Integer> candidates;
    cout<<"Obteniendo candidatos..."<<endl;
    getCandidates(candidates);

    for(int i = 0; i < votes; i++){
        cout<<"Voto al azar"<<endl;
        int index = rand() % candidates.size();
        int numOfShares = getNumberOfShares() + 1;
        size_t sizeCredentials;
        size_t sizeVote;
        Integer cypherCredential;
        Integer cypherVote;
        cout<<"Cifrando credenciales..."<<endl;
        elGamalInstance.encrypt(credential,cypherCredential,sizeCredentials);
        cout<<"Cifrando voto...."<<endl;
        elGamalInstance.encrypt(candidates[index], cypherVote, sizeVote);
        vector<Integer> sharesCredential;
        vector<Integer> sharesVote;
        cout<<"Creacndo shares para credenciales..."<<endl;
        VS::encrypt(cypherCredential, keys, numOfShares, 500, sharesCredential);
        cout<<"Creando shares para voto..."<<endl;
        VS::encrypt(cypherVote, keys, numOfShares, 500, sharesVote);
        for(int j = 0; j < numOfShares; j++){
            ofstream file(".newVotes/Shares" + to_string(i) + "_" + to_string(j));
            file<<sharesCredential[j]<<" -> ";
            file<<sharesVote[j];
            file.close();
        }
    }
    string command = "python ./Blockchain/sendVote.py " + to_string(votes);
    system(command.c_str());    

    
}
