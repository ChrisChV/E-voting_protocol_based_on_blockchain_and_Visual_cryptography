#include <iostream>
#include <fstream>

using namespace std;

string SERVER_HOSTS_FIlE_PATH = "Conf/serverHosts";
string RESET_BLOCKCHAIN_BIN_PATH = "/src/Blockchain/runResetBlockchain";

int main(){
    cout<<"------Reiniciando Blockchains-----"<<endl;
    ifstream hostsFiles(SERVER_HOSTS_FIlE_PATH);
    string ip = "";
    string user = "";
    string pass = "";
    string groupId = "";
    while(hostsFiles >> user){
        hostsFiles >> ip;
        hostsFiles >> pass;
        hostsFiles >> groupId;
        string command = "sshpass -p '" + pass + "' ssh "+  user + "@" + ip + " /home/" + user  + RESET_BLOCKCHAIN_BIN_PATH + " " + user;
        cout<<command<<endl;
        system(command.c_str());
    }
    hostsFiles.close();
    cout<<"Done"<<endl;
}
