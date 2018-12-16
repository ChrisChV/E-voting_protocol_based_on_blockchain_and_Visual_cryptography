#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

string SERVER_HOSTS_FIlE_PATH = "Conf/serverHosts";
string LEADRES_FILE_PATH = "Conf/leaders";
string PORT_FILE_PATH = "Conf/port";
string SRC_FILE = "./";
string TEMP_FILE_PATH = "_tempfile";

void createTestServer(string user, string ip, string pass ,string leader, string puerto){
    ofstream tempFile(TEMP_FILE_PATH);
    tempFile<< "from nodo import *"<<endl;
    tempFile<< "import sys;"<<endl;
    tempFile<< "SERVER_HOSTS_FILE_PATH = \"../Conf/serverHosts\""<<endl;
    tempFile<< "myHost = \""<<ip<<"\""<<endl;
    tempFile<< "def getHostList(fileName):"<<endl;
    tempFile<< "\tmyIdGroup = 0"<<endl;
    tempFile<< "\tfile = open(fileName, 'r')"<<endl;
    tempFile<< "\tips = []"<<endl;
    tempFile<< "\tgroupsIDs = []"<<endl;
    tempFile<< "\tfor line in file:"<<endl;
    tempFile<< "\t\ttokens = line.split(" ")"<<endl;
    tempFile<< "\t\tips.append(tokens[1])"<<endl;
    tempFile<< "\t\tif(tokens[1] == myHost):"<<endl;
    tempFile<< "\t\t\t myIdGroup = int(tokens[3].rstrip('\\n'))"<<endl;
    tempFile<< "\t\tgroupsIDs.append(int(tokens[3].strip('\\n')))"<<endl;
    tempFile<< "\thosts_list = []"<<endl;
    tempFile<< "\tnumOfGroups = max(groupsIDs) + 1"<<endl;
    tempFile<< "\tfor i in range(0, numOfGroups):"<<endl;
    tempFile<< "\t\thosts_list.append([])"<<endl;
    tempFile<< "\tfor i in range(0, len(ips)):"<<endl;
    tempFile<< "\t\thosts_list[groupsIDs[i]].append(ips[i])"<<endl;
    tempFile<< "\tfile.close()"<<endl;
    tempFile<< "\treturn hosts_list, myIdGroup"<<endl;
    tempFile<< "hosts_list, myIdGroup = getHostList(SERVER_HOSTS_FILE_PATH)"<<endl;
    tempFile<< "myLeader = \"" + leader + "\""<<endl;
    tempFile<< "blockchainPath = \"./TestBC\""<<endl;
    tempFile<<"toleranceValue = 0.5"<<endl;
    tempFile<<"voteUmbral = 2"<<endl;
    tempFile<<"print(\"My group:\" + str(myIdGroup))"<<endl;
    tempFile<<"yo = NodoSufAndComis(myHost," + puerto + ", hosts_list, myIdGroup, myLeader, toleranceValue, voteUmbral, blockchainPath)"<<endl;
    tempFile.close();
    string command = "sshpass -p '" + pass + "' scp -r " + TEMP_FILE_PATH + " " + user + "@" + ip + ":~/src/Blockchain/testServer.py";
    system(command.c_str());
}


int main(int argc, char ** argv){
    cout<<"-------Creador de servidores-----"<<endl;
    ifstream hostsFiles(SERVER_HOSTS_FIlE_PATH);
    ifstream leadersFile(LEADRES_FILE_PATH);
    ifstream portFile(PORT_FILE_PATH);
    string leader = "";
    string user = "";
    string ip = "";
    string pass = "";
    string groupId = "";
    string port = "";
    vector<string> leaders;
    int acutalLeader = 0;
    cout<<"Obteniendo puerto..."<<endl;
    portFile >> port;
    cout<<"Puerto: "<<port<<endl;
    cout<<"Obteniendo líderes..."<<endl;
    while(leadersFile >> leader){
        leaders.push_back(leader);
    }
    cout<<"Obteniendo hosts..."<<endl;
    while(hostsFiles >> user){
        hostsFiles >> ip;
        hostsFiles >> pass;
        hostsFiles >> groupId;
        string command = "sshpass -p '" + pass + "' scp -r " + SRC_FILE + " " + user + "@" + ip + ":~/src";
        cout<<command<<endl;
        cout<<"Subiendo src/ a "<<user<<"@"<<ip<<endl;
        system(command.c_str());
        cout<<"Subiendo testServer.py..."<<endl;
        createTestServer(user, ip, pass, leaders[acutalLeader], port);
        acutalLeader++;
        cout<<"Done"<<endl;
    }
    
    hostsFiles.close();
    leadersFile.close();
    portFile.close();
    cout<<"Done"<<endl;
}

