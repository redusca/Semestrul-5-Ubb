package ro.mpp2024;
import java.util.Arrays;
import java.util.Random;

public class Main{

    //1. Ciclic : i = id , id + p, id + 2p ...
    public static class Cyclic extends Thread {
        //ip - indexul thread
        // p - nr de threaduri
        // n - dimensiunea vectorilor
        // A, B, C - vectori
        private int id ,p , n;
        private int[] A, B, C;

        public Cyclic (int id, int p, int n, int[] A, int[] B, int[] C) {
            this.id = id;
            this.p = p;
            this.n = n;
            this.A = A;
            this.B = B;
            this.C = C;
        }

        public void run(){
            for (int i = id; i < n; i += p) {
                C[i] = A[i] + B[i];
            }
        }
    }

    //2. Blocuri
    public static class Block extends Thread{
        private int start, end;
        private int[] A, B, C;

        public Block(int start, int end, int[] A, int[] B, int[] C) {
            this.start = start;
            this.end = end;
            this.A = A;
            this.B = B;
            this.C = C;
        }

        public void run() {
            for (int i = start; i < end; i++) {
                C[i] = A[i] + B[i];
            }
        }
    }

    public static int[] generator(int n, int max){
        int [] v = new int[n];
        Random rand = new Random();

        for(int i = 0; i < n; i++){
            v[i] = rand.nextInt(max);
        }

        return v;
    }

    static long Sequential (int[] A,int[] B, int[] C) {
        long t0 = System.nanoTime();

        for (int i = 0; i < A.length; i++) {
            C[i] = A[i] + B[i];
        }

        long t1 = System.nanoTime();
        return t1 - t0;
    }

    static long runCyclic (int[] A,int[] B,int[] C,int p) throws InterruptedException {
        Cyclic[] threads = new Cyclic[p];
        long t0 = System.nanoTime();

        for (int id = 0; id < p ; id++){
            threads[id] = new Cyclic(id,p , A.length, A,B,C);
            threads[id].start();
        }
        for (int id = 0; id < p ; id++){
            threads[id].join();
        }

        long t1 = System.nanoTime();
        return t1 - t0;
    }

    static long runBlock (int[] A,int[] B,int[] C,int p) throws InterruptedException {
        Block[] threads = new Block[p];
        long t0 = System.nanoTime();

        int n = A.length;

        for (int id = 0; id < p ; id++){

            int start = id * n / p;
            int end = Math.min(n , (id+1) * n / p);

            threads[id] = new Block(start,end,A,B,C);
            threads[id].start();
        }

        for (int id = 0; id < p ; id++){
            threads[id].join();
        }

        long t1 = System.nanoTime();
        return t1 - t0;
    }

    public  static void main(String[] args) throws InterruptedException {
        int n = 1_000_000;
        int max = 50_000;
        int p = 5;
        int[] A = generator(n,max);
        int[] B = generator(n,max);

        //1 Secvential
        int[] C1 = new int[n];
        long tSec = Sequential(A,B,C1);
        System.out.println("Sequential: " + tSec);

        //2 Cyclic
        int[] C2 = new int[n];
        long tSecCyclic = runCyclic(A,B,C2,p);
        System.out.println("Cyclic: " + tSecCyclic);

        //3 Block
        int[] C3 = new int[n];
        long tSecBlock = runBlock(A,B,C3,p);
        System.out.println("Block: " + tSecBlock);

        //Verificare corectitudine
        System.out.println("C1 == C2 ?" + Arrays.equals(C1, C2));
        System.out.println("C1 == C3 ?" + Arrays.equals(C1, C3));

    }
}