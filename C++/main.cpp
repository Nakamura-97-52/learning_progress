#include <iostream>
#include <vector>
#include <string>

using namespace std;

int addSum(int first_num, int second_num){
    int result = first_num + second_num;
    return result;
}

int notmanin()
{
    int first_num {3};
    int second_num {7};

    std::cout << "first number" << first_num << std::endl;
    std::cout << "second number" << second_num << std::endl;

    int sum = addSum(6, 9);
    std::cout << "sum:" << sum << std::endl; 

    return 0;
}