// CPSC 3383: Language Structure
// Fall 2015
// Project 2: Interpreting a Subset of XLisp
// Due Date: 11/24/2015
// Name: Adam Crider
// T-number (Last 4 Digits): 6390
// Description of the Program (2-3 sentences): Small Lisp interpreter with basic functionality.
// Date Written: 11/24/2015
// Date Revised: 11/24/2015
#include <cstdlib>
#include <map>
#include <iostream>
#include <stack>
#include <string>
#include <sstream>
#include <vector>
#include <list>

using namespace std;

//Global variable for storing variables
map<char, string> vars;

//Linked List class for keeping track of statements
struct node {
	vector<node> list;
	string val = "";
	node() {
	}
	node(string v) {
		val = v;
	}
};
/*
Parse the input to get nested lists for easier parsing
*/
node parse(std::list<std::string> & tokens)
{
	const std::string token(tokens.front());
	tokens.pop_front();
	if (token == "(") {
		node c;
		while (tokens.front() != ")")
			c.list.push_back(parse(tokens));
		tokens.pop_front();
		return c;
	}
	else
		return node(token);
}
bool symbol(char C)
{
	if (C >= 'a' && C <= 'z') return true;
	return false;
}
//Recursive eval function to parse lists
string eval(node n) {
	if (n.val == "") {
		if (n.list[0].val == "setq") {
			vars[n.list[1].val.at(0)] = n.list[2].val;
			return n.list[2].val;
		}
		else if (n.list[0].val == "+") {
			return to_string(atoi(eval(n.list[1]).c_str()) + atoi(eval(n.list[2]).c_str()));
		}
		else if (n.list[0].val == "-") {
			return to_string(atoi(eval(n.list[1]).c_str()) - atoi(eval(n.list[2]).c_str()));
		}

		else if (n.list[0].val == "/") {
			return to_string(atoi(eval(n.list[1]).c_str()) / atoi(eval(n.list[2]).c_str()));

		}
		else if (n.list[0].val == "*") {
			return to_string(atoi(eval(n.list[1]).c_str()) * atoi(eval(n.list[2]).c_str()));
		}
		else {
			return n.list[0].val;
		}
	}
	else {
		if (symbol(n.val.at(0))) {
			return vars[n.val.at(0)];
		}
		else {
			return n.val;
		}
	}
	return "";
}


int main() {

	//Setup look to constantly wait for new input.
	while (true) {
		cout << "> ";
		list<string> v;
		string in;
		getline(cin, in);
		istringstream iss(in);
		while (iss)
		{
			string sub;
			iss >> sub;
			if (sub == "exit") {
				return 0;
			}
			else {
				//Tokenize input so it's in the format: ['(','setq','x,'12',')']
				if (sub.length() > 0) {
					if (sub == "(" || sub == ")") {
						v.push_back(sub);
					}
					else {
						int s = 0;
						int f = sub.length();
						for (int i = 0; sub.at(i) == '('; i++) {
							v.push_back("(");
							s = i + 1;
						}
						for (int i = sub.length() - 1; sub.at(i) == ')'; i--) {
							f = i;
						}
						v.push_back(sub.substr(s, f));
						for (int i = sub.length() - 1; i >= f; i--) {
							v.push_back(")");
						}
					}
				}
			}

		}
		cout << endl;
		//parse & print final value
		node n = parse(v);
		cout << eval(n) << endl;
	}
	return 0;
}
