#include <iostream>
#include <sstream>
#include <stdlib.h>
#include <numeric>
#include <functional>
#include <vector>
#include <cstdlib>

using namespace std;

#define debug(message) \
          if (DEBUG) { std::cout << #message << std::endl; }

const bool DEBUG = true;

void abort(string error);

int gcd(int a, int b){
  for (;;){
    if (a == 0) return b;
      b %= a;
    if (b == 0) return a;
      a %= b;
    }
}

int lcm(int a, int b){
  // int temp = gcd(a, b);
  // return temp ? (a / temp * b) : 0;
  return (a * b) / gcd(a, b);
}

int gcdAll(const vector<int> params){
  int ans = 0;
  for(auto i:params){
    ans = gcd(ans, i);
  }
  return ans;

  accumulate(params.begin(), params.end(), 0, gcd);
}

int lcmAll(const vector<int> params){
  return accumulate(params.begin(), params.end(), 0, std::multiplies<int>()) / gcdAll(params);
}

void displayVectors(vector<vector<unsigned int>> vector){
  cout << "\n---------------------\n";
  for(auto firstLayer:vector){
    if(firstLayer.size()){
      for(auto secondLayer:firstLayer){
        cout << secondLayer << ' ';
      }
      cout << endl;
    }
  }
  cout << "---------------------\n";
}

void displayVectors(vector<vector<string>> vector){
  cout << "\n---------------------\n";
  for(auto firstLayer:vector){
    if(firstLayer.size()){
      for(auto secondLayer:firstLayer){
        cout << secondLayer << ' ';
      }
      cout << endl;
    }
  }
  cout << "---------------------\n";
}


int main(void){
  string equation;

  cout << "Welcome to Copeland's equation balancer! Enter your equation below (case sensitive, use \"->\" to seperate sides) (press q to quit):\n";
  // getline(cin, equation);
  equation = "C8H18 + O2 -> CO2 + H2O";
  // C8H18 + O2 -> CO2 + H2O
  cout << equation << endl;

  if ((equation.size() == 1) and (tolower(equation.front()) == 'q')){
    cout << "Goodbye.\n";
    exit(0);
  }

  if(not isupper(equation.front()) or not isalpha(equation.front()))
    abort("Invalid equation (first character is incorrect).");

  // parse the equation

  vector<vector<string>> elementsLeft(64);
  vector<vector<unsigned int>> amountsLeft(64);

  vector<vector<string>> elementsRight(64);
  vector<vector<unsigned int>> amountsRight(64);

  bool isRight = false;
  int i = 0;

  // initialize the amounts (the first number of each compound is it's multiple)
  for(auto compounds:amountsLeft){
    compounds.push_back(1);
  }

  for(auto compounds:amountsRight){
    compounds.push_back(1);
  }

  // equation += "\0";

  for(auto it = equation.begin(); it != equation.end();){

    // ...\0... (you're at the end)
    if(not *it){
      break;
    }
    // ...+...
    else if(*it == '+'){
      ++i;
      ++it;
    }
    // ...CP... or ...C ... or ...C+...
    else if(isupper(*it) and (isupper(*(it + 1)) or (*(it + 1) == ' ') or (*(it + 1) == '+') or (*(it + 1) == '\0'))){
      if (isRight){
        string tmp;
        tmp += *it;
        elementsRight[i].push_back(tmp);
        amountsRight[i].push_back(1);
      }
      else{
        string tmp;
        tmp += *it;
        elementsLeft[i].push_back(tmp);
        amountsLeft[i].push_back(1);
      }
      ++it;
    }
    // ...CoP...
    else if(isupper(*it) and islower(*(it + 1)) and isupper(*(it + 2))){
      if (isRight){
        // string tmp;
        // tmp += *it;
        string tmp2;
        tmp2 += *it + *(it + 1);
        elementsRight[i].push_back(tmp2);
        amountsRight[i].push_back(1);
      }
      else{
        // string tmp;
        // tmp += *it;
        string tmp2;
        tmp2 += *it + *(it + 1);
        elementsLeft[i].push_back(tmp2);
        amountsLeft[i].push_back(1);
      }
      it += 2;
    }
    // ...C6...
    else if(isupper(*it) and isdigit(*(it + 1)) and not isdigit(*(it + 2))){
      if (isRight){
        string tmp;
        tmp += *it;
        elementsRight[i].push_back(tmp);
        amountsRight[i].push_back(atoi(&(*(it + 1))));
      }
      else{
        string tmp;
        tmp += *it;
        elementsLeft[i].push_back(tmp);
        amountsLeft[i].push_back(atoi(&(*(it + 1))));
      }
      it += 2;
    }
    // ...Cg6...
    else if(isupper(*it) and islower(*(it + 1)) and isdigit(*(it + 2)) and not isdigit(*(it + 3))){
      if (isRight){
        string tmp;
        tmp += *it + *(it + 1);
        elementsRight[i].push_back(tmp);
        amountsRight[i].push_back(atoi(&*(it + 2)));
      }
      else{
        string tmp;
        tmp += *it + *(it + 1);
        elementsLeft[i].push_back(tmp);
        amountsLeft[i].push_back(atoi(&*(it + 2)));
      }
      it += 3;
    }
    // ...C12...
    else if(isupper(*it) and isdigit(*(it + 1)) and isdigit(*(it + 2))){
      if (isRight){
        string tmp;
        tmp += *it;
        string num;
        num += *(it + 1);
        num += *(it + 2);
        elementsRight[i].push_back(tmp);
        amountsRight[i].push_back(atoi(num.c_str()));
      }
      else{
        string tmp;
        tmp += *it;
        string num;
        num += *(it + 1);
        num += *(it + 2);
        elementsLeft[i].push_back(tmp);
        amountsLeft[i].push_back(atoi(num.c_str()));
      }
      it += 3;
    }
    // ...Cg12...
    else if(isupper(*it) and islower(*(it + 1)) and isdigit(*(it + 2)) and isdigit(*(it + 3))){
      if (isRight){
        string tmp;
        tmp += *it + *(it + 1);
        string num;
        num += *(it + 2);
        num += *(it + 3);
        elementsRight[i].push_back(tmp);
        amountsRight[i].push_back(atoi(num.c_str()));
      }
      else{
        string tmp;
        tmp += *it + *(it + 1);
        string num;
        num += *(it + 2);
        num += *(it + 3);
        elementsLeft[i].push_back(tmp);
        amountsLeft[i].push_back(atoi(num.c_str()));
      }
      it += 4;
    }
    //
    else if(*it == '('){
      abort("Hold up. I haven't finished that feature yet.");
      ++it;
    }
    //
    else if(*it == ')'){
      abort("Hold up. I haven't finished that feature yet.");
      ++it;
    }
    // ...->...
    else if((*it == '-') and (*(it + 1) == '>')){
      isRight = true;
      it += 2;
    }
    // ... ...
    else if(*it == ' '){
      ++it;
    }
    // ...6...
    else if(isdigit(*it)){
      abort("Sorry, we haven't implemented that feature yet.");
      ++it;
    }
    // garbage
    else{
      cout << *it << " is here when it's not supposed to be\n";
      // abort("Unrecognized symbols in the equation!");
      break;
    }
  }


  for(auto compounds:amountsLeft){
    if(compounds.size())
      // compounds.insert(compounds.begin(), 1);
    compounds.front() = 1;
  }
  for(auto compounds:amountsRight){
    if(compounds.size())
      // compounds.insert(compounds.begin(), 1);
    compounds.front() = 1;
  }

  // do math

  debug(amountsLeft)
  displayVectors(amountsLeft);
  debug(amountsRight)
  displayVectors(amountsRight);

  debug(\n\n\n)

  // loop through the left side, and if you see a match to the element you're looking at,
  //  get the lowest common multiple of the amounds of each of them, and assign the
  //  compound multiplier of the compound it's in to that lowest common multiple.

  // check all occurences of a given element on both sides, then set the multiplier of
  //  each compound it's in to the least common multiple of the 2 current multipliers
  for(int lc = 0; lc < elementsLeft.size(); ++lc){
    for(int lce = 0; lce < elementsLeft[lc].size(); ++lce){
      for(int rc = 0; rc < elementsRight.size(); ++rc){
        for(int rce = 0; rce < elementsRight[rc].size(); ++rce){
          if(elementsLeft[lc][lce] == elementsRight[rc][rce]){
            int tmp = lcm(amountsLeft[lc][lce], amountsRight[rc][rce]);
            amountsLeft[lc].front()  = tmp;
            amountsRight[rc].front() = tmp;
          }
        }
      }
    }
  }

  // then get the lowest common multiple of the compound multipliers
  vector<int> multipliers(64);
  for(auto current:amountsLeft)
    if(current.size())
      multipliers.push_back(current.front());

  for(auto current:amountsRight)
    if(current.size())
      multipliers.push_back(current.front());


  // ...and divide each by it
  int tmp = lcmAll(multipliers);
  for(auto adj:amountsLeft)
    if(adj.size())
      adj.front() = tmp / adj.front();

  for(auto adj:amountsRight)
    if(adj.size())
      adj.front() = tmp / adj.front();

  string ss;

  // reconstruct the formula into something human readable again
  //  (deparse, if you will)

  debug(amountsLeft)
  displayVectors(amountsLeft);
  debug(amountsRight)
  displayVectors(amountsRight);

  for(int lc = 0; lc < elementsLeft.size(); ++lc){
    if(amountsLeft[lc].size()){
      // if(amountsLeft[lc].front() != 1)
        ss += to_string(amountsLeft[lc].front());
        ss += '(';
    }
    for(int lce = 0; lce < elementsLeft[lc].size(); ++lce){
      ss += elementsLeft[lc][lce];

      if(amountsLeft[lc][lce] != 1)
        ss += to_string(amountsLeft[lc][lce]);
    }
    if(elementsLeft[lc].size())
      ss += ") + ";
  }

  ss.erase(ss.end() - 3, ss.end());
  ss += " -> ";

for(int rc = 0; rc < elementsRight.size(); ++rc){
  if(amountsRight[rc].size()){
    // if(amountsRight[rc].front() != 1)
      ss += to_string(amountsRight[rc].front());
      ss += '(';
  }
    for(int rce = 0; rce < elementsRight[rc].size(); ++rce){
      ss += elementsRight[rc][rce];

      if(amountsRight[rc][rce] != 1)
        ss += to_string(amountsRight[rc][rce]);
    }
  if(elementsRight[rc].size())
    ss += ") + ";
}


  ss.erase(ss.end() - 3, ss.end());
  cout << endl << ss << endl;

  return 0;
}

void abort(string error){
  cout << endl << error << endl;
  exit(0);
}