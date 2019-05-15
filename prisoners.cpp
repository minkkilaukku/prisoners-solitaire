#include <iostream>
#include <cstdlib>
#include <algorithm>
#include <vector>
#include <random>
//#include <chrono>       // std::chrono::system_clock

using namespace std;


int simuARound(vector<int> &deck, int toTable, int k)
{
    //unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    //shuffle(deck.begin(), deck.end(), std::default_random_engine(seed));
    random_shuffle(deck.begin(), deck.end());
    //TODO
    vector<int> table;
    for (int i=0; i<toTable; i++) {
        table.push_back(deck[i]);
    }
    for (unsigned int i=toTable; i<deck.size(); i+=k) {
        int x = deck[i];
        table.erase(remove(table.begin(), table.end(), x), table.end());
    }
    return table.size();
}

vector<double> simu(int simuN)
{
    int suits = 4;
    int vals = 13;
    int n = suits*vals;

    int toTable = 13;
    int k = 3;

    vector<int> deck;
    for (int i=0; i<n; i++) deck.push_back(i%vals);
    vector<int> counts;
    for (int i=0; i<toTable+1; i++) counts.push_back(0);
    for (int i=0; i<simuN; i++) {
        int x = simuARound(deck, toTable, k);
        counts[x]++;
    }
    vector<double> ret;
    for (unsigned int i=0; i<counts.size(); i++) ret.push_back(float(counts[i])/simuN);
    return ret;
}

int main()
{
    vector<double> a = simu(1e7);
    for (unsigned int i=0; i<a.size(); i++) {
        cout << a[i] << endl;
    }
}
