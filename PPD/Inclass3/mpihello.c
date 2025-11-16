#include <stdio.h>
#include <iostream>
#include <string.h>
#include <vector>
#include <mpi.h>

using namespace std;

void run_mpi_hello_world(){
    // Get the rank of the process
    int my_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);

    // Get the total number of processes
    int num_processes;
    MPI_Comm_size(MPI_COMM_WORLD, &num_processes);

    if(my_rank == 0){
        // Process 0  : Receive message from all other processes
        string result = "";
        char buffer[256];
        for(int i = 1; i < num_processes; i++){
            MPI_Recv(buffer, 256, MPI_CHAR, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            result += buffer;
            if (i < num_processes - 1) {
                result += "\n";
            }
        }

        cout << "Procces 0 receivedd all messages:\n" << result << endl;
    }
    else{
        //Other processes send message to processes 0
        char message[256];
        sprintf(message,"Hello from id %d",my_rank);
        MPI_Send(message, strlen(message) + 1, MPI_CHAR, 0, 0, MPI_COMM_WORLD);
    }
}

int main(int argc, char** argv) {
    MPI_Init(NULL, NULL);

    run_mpi_hello_world();

    MPI_Finalize();
    return 0;
}
