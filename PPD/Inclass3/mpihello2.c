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

void run_mpi_hello_world_async(){
    // Get the rank of the process
    int my_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);

        // Get the total number of processes
    int num_processes;
    MPI_Comm_size(MPI_COMM_WORLD, &num_processes);

    if(my_rank == 0){
        // Process 0  : Receive message from all other processes
        int num_ohter_processes = num_processes - 1;
        vector<char[256]> buffers(num_ohter_processes);
        vector<MPI_Request> requests(num_ohter_processes);
        vector<int> flag(num_ohter_processes,0);

        for(int i = 0; i < num_ohter_processes; i++){
            MPI_Irecv(buffers[i], 256, MPI_CHAR, i+1, 0, MPI_COMM_WORLD, &requests[i]);
        }

        int received_count = 0;
        while (received_count < num_ohter_processes)
        {
            for(int i = 0; i < num_ohter_processes; i++){
                if(flag[i] == 0){//if not received yet{
                    MPI_Test(&requests[i], &flag[i], MPI_STATUS_IGNORE);
                    if(flag[i]){
                        //message received
                        received_count++;
                    }
                }
            }
        }

        //build the final string
        string result = "";
        for(int i = 0; i < num_ohter_processes; i++){
            result += buffers[i];
            if (i < num_ohter_processes - 1) {
                result += "\n";
            }
        }
    
        cout << "Process 0 received all messages:\n" << result << endl;

    }
    else{
        //Other processes send message to processes 0
        char message[256];
        sprintf(message,"Hello from id %d",my_rank);
        
        MPI_Request request;
        MPI_Isend(message, strlen(message) + 1, MPI_CHAR, 0, 0, MPI_COMM_WORLD, &request);
    }
}

void run_vector_addition_collective() {
    // Get the rank of the process
    int my_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
   
    // Get the total number of processes
    int num_processes;
    MPI_Comm_size(MPI_COMM_WORLD, &num_processes);
   
    const int VECTOR_SIZE = 100;
    int segment_size = VECTOR_SIZE / num_processes;
   
    // All processes need their own segment buffers
    std::vector<int> segment_A(segment_size);
    std::vector<int> segment_B(segment_size);
    std::vector<int> segment_C(segment_size);
   
    std::vector<int> A, B, C;
   
    if (my_rank == 0) {
        // Process 0: Initialize vectors A and B
        A.resize(VECTOR_SIZE);
        B.resize(VECTOR_SIZE);
        C.resize(VECTOR_SIZE);
       
        // Initialize vectors with some values
        for (int i = 0; i < VECTOR_SIZE; i++) {
            A[i] = i;
            B[i] = i * 2;
        }
    }
 
    // Scatter A and B from process 0 to all processes
    MPI_Scatter(my_rank == 0 ? A.data() : nullptr, segment_size, MPI_INT,
                segment_A.data(), segment_size, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Scatter(my_rank == 0 ? B.data() : nullptr, segment_size, MPI_INT,
                segment_B.data(), segment_size, MPI_INT, 0, MPI_COMM_WORLD);
   
    // All processes compute their segment: C = A + B
    for (int i = 0; i < segment_size; i++) {
        segment_C[i] = segment_A[i] + segment_B[i];
    }
   
    // Gather all computed segments back to process 0
    MPI_Gather(segment_C.data(), segment_size, MPI_INT,
               my_rank == 0 ? C.data() : nullptr, segment_size, MPI_INT, 0, MPI_COMM_WORLD);
   
    if (my_rank == 0) {
        // Display the result
        std::cout << "Vector addition (collective) completed. First 10 elements of C:\n";
        for (int i = 0; i < 10; i++) {
            std::cout << "C[" << i << "] = " << C[i] << " (A[" << i << "] + B[" << i << "] = " << A[i] << " + " << B[i] << ")\n";
        }
        std::cout << "...\n";
        std::cout << "Last 10 elements of C:\n";
        for (int i = VECTOR_SIZE - 10; i < VECTOR_SIZE; i++) {
            std::cout << "C[" << i << "] = " << C[i] << " (A[" << i << "] + B[" << i << "] = " << A[i] << " + " << B[i] << ")\n";
        }
    }
}

void run_vector_addition(){
    // Get the rank of the process
    int my_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);

        // Get the total number of processes
    int num_processes;
    MPI_Comm_size(MPI_COMM_WORLD, &num_processes);

    const int VECTOR_SIZE = 100;;
    int segment_size = VECTOR_SIZE / num_processes;

    if(my_rank == 0){
        // Process 0  : Initialize vectors and distribute segments
        vector<int> A(VECTOR_SIZE);
        vector<int> B(VECTOR_SIZE);
        vector<int> C(VECTOR_SIZE);

        for (int i=0; i<VECTOR_SIZE; i++){
            A[i] = i;
            B[i] = i*2;
        }

        // Send segments to other processes
        for(int i = 1; i < num_processes; i++){
            int start_index = i * segment_size;
            MPI_Send(&A[start_index], segment_size, MPI_INT, i, 0, MPI_COMM_WORLD);
            MPI_Send(&B[start_index], segment_size, MPI_INT, i, 1, MPI_COMM_WORLD);
        }

        //Process 0 computes compute its own segment
        for(int i = 0; i < segment_size; i++){
            C[i] = A[i] + B[i];
        }

        //Receive computed segments from other processes
        for(int i = 1; i < num_processes; i++){
            int start_index = i * segment_size;
            MPI_Recv(&C[start_index], segment_size, MPI_INT, i, 2, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }

        //Display the result
        cout << "Vector addition completed. First 10 elements of result vector C:";
        for(int i = 0; i < 10; i++){
            cout << C[i]  << " ";
        }
        cout << "..."   << endl;
        cout << "Last 10 elements of result vector C:";
        for(int i = VECTOR_SIZE - 10; i < VECTOR_SIZE; i++){
            cout << C[i] << " ";
        }
    }
    else{
        //Other processes receive segments, compute and send back
        vector<int> A_segment(segment_size);
        vector<int> B_segment(segment_size);
        vector<int> C_segment(segment_size);

        MPI_Recv(A_segment.data(), segment_size, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        MPI_Recv(B_segment.data(), segment_size, MPI_INT, 0, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        //Compute segment
        for(int i = 0; i < segment_size; i++){
            C_segment[i] = A_segment[i] + B_segment[i];
        }

        //Send computed segment back to process 0
        MPI_Send(&C_segment[0], segment_size, MPI_INT, 0, 2, MPI_COMM_WORLD);
    }
}

int main(int argc, char** argv) {
    MPI_Init(NULL, NULL);

    //run_mpi_hello_world();
    //run_mpi_hello_world_async();
    //run_vector_addition();
    run_vector_addition_collective();

    MPI_Finalize();
    return 0;
}
