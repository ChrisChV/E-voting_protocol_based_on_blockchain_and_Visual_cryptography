#include <iostream>
#include <fstream>

using namespace std;

int main(int argc, char ** argv){
    string user = argv[1];
    string command = "rm /home/" + user + "/src/Blockchain/TestBC/*";
    system(command.c_str());
    ofstream conf("/home/" + user + "/src/Blockchain/TestBC/blockchainConf");
    conf<<"init"<<endl;
    conf<<"init"<<endl;
    conf<<"0"<<endl;
    conf<<"0"<<endl;
    conf.close();
}
