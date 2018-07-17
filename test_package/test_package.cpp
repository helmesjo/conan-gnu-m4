#include <cstdlib>
#include <iostream>
#include <fstream>
#include <sstream>

int main()
{
    int result = std::system("m4 --version > m4-output.txt");

    if(result == 0){
        std::ifstream t("m4-output.txt");
        std::stringstream buffer;
        buffer << t.rdbuf();
        std::cout << "\nOutput from 'm4 --version': \n\n" << buffer.str() << "\n";
    }
    else
        std::cerr << "\nFailed to run command 'm4 --version'\n";
    
    return result == 0 ? EXIT_SUCCESS : EXIT_FAILURE;
}
