import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

public class Convolutie {
    private final int[][] C;
    private final int[][] matrice;
    private final int n;
    private final int m;
    private final int k;

    public Convolutie(String input) throws IOException {
        try (BufferedReader br = new BufferedReader(new FileReader(input))) {
            k = Integer.parseInt(br.readLine().trim());
            List<Integer> values = new ArrayList<>();
            while (values.size() < k * k) {
                String[] parts = br.readLine().trim().split("\\s+");
                for (String p : parts) values.add(Integer.parseInt(p));
            }
            C = new int[k][k];
            for (int i = 0, idx = 0; i < k; i++) {
                for (int j = 0; j < k; j++, idx++) {
                    C[i][j] = values.get(idx);
                }
            }

            String[] dimensions = br.readLine().trim().split("\\s+");
            n = Integer.parseInt(dimensions[0]);
            m = Integer.parseInt(dimensions[1]);

            matrice = new int[n + 1][m + 1];
            values = new ArrayList<>();
            while (values.size() < n * m) {
                String[] parts = br.readLine().trim().split("\\s+");
                for (String p : parts) values.add(Integer.parseInt(p));
            }

            for (int i = 1, idx = 0; i <= n; i++) {
                for (int j = 1; j <= m; j++, idx++) {
                    matrice[i][j] = values.get(idx);
                }
            }
        }
    }

    private int claim(int x, int y) {
        return matrice[Math.min(n, Math.max(x, 1))][Math.min(m, Math.max(y, 1))];
    }

    private int convVec(int j, int[] a, int[] b, int[] c) {
        int sum = 0;
        for (int x = -1; x <= 1; x++) {
            for (int y = -1; y <= 1; y++) {
                int coeff = C[x + 1][y + 1];
                int xVal = (x == -1) ? a[j + y] : (x == 0) ? b[j + y] : c[j + y];
                sum += xVal * coeff;
            }
        }
        return sum;
    }

    private void initVec(int[] a, int[] b, int[] c, int i) {
        for (int j = 0; j <= m + 1; j++) {
            a[j] = claim(i - 1, j);
            b[j] = claim(i, j);
            c[j] = claim(i + 1, j);
        }
    }

    private void nextVec(int[] a, int[] b, int[] c, int i) {
        for (int j = 0; j <= m + 1; j++) {
            a[j] = b[j];
            b[j] = c[j];
            c[j] = claim(i + 1, j);
        }
    }

    public void sequential() throws IOException {
        long start = System.nanoTime();

        int[] a = new int[m + 2];
        int[] b = new int[m + 2];
        int[] c = new int[m + 2];
        initVec(a, b, c, 1);

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                matrice[i][j] = convVec(j, a, b, c);
            }
            nextVec(a, b, c, i + 1);
        }

        long end = System.nanoTime();
        System.out.println(end - start);

        writeOutput("output/sec/outputJ_" + k + "_" + n + "_" + m + ".txt");
    }

    public void parallel(int threads) throws IOException {
        long start = System.nanoTime();

        Thread[] threadPool = new Thread[threads];
        int rowsPerThread = n / threads;
        int maxRows = n - (threads - 1) * rowsPerThread; // Max rows for last thread

        // Create safe vectors for boundary rows between thread regions
        int[][] safeVec = new int[threads - 1][m + 2];
        for (int t = 1; t < threads; t++) {
            for (int j = 0; j <= m + 1; j++) {
                safeVec[t - 1][j] = claim(t * rowsPerThread + 1, j);
            }
        }

        // Create a CyclicBarrier that waits for all threads before proceeding to next row
        CyclicBarrier syncBarrier = new CyclicBarrier(threads);

        for (int t = 0; t < threads; t++) {
            int startRow = t * rowsPerThread + 1;
            int endRow = (t == threads - 1) ? n : (t + 1) * rowsPerThread;
            int threadId = t;

            threadPool[t] = new Thread(() -> {
                int[] a = new int[m + 2];
                int[] b = new int[m + 2];
                int[] c = new int[m + 2];
                initVec(a, b, c, startRow);

                // All threads must iterate the same number of times for barrier synchronization
                for (int iter = 0; iter < maxRows; iter++) {
                    int i = startRow + iter;
                    
                    // Only process if within this thread's range
                    if (i <= endRow) {
                        for (int j = 1; j <= m; j++) {
                            matrice[i][j] = convVec(j, a, b, c);
                        }
                    }

                    // Wait for all threads to finish their current row
                    try {
                        syncBarrier.await();
                    } catch (InterruptedException | BrokenBarrierException e) {
                        Thread.currentThread().interrupt();
                        return;
                    }

                    // Only advance vectors if within range
                    if (i <= endRow) {
                        nextVec(a, b, c, i + 1);
                        
                        // Use safe vector for the last row calculation to avoid race condition
                        if (threadId < threads - 1 && i == endRow - 1) {
                            c = safeVec[threadId];
                        }
                    }
                }
            });
            threadPool[t].start();
        }

        for (Thread thread : threadPool) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        long end = System.nanoTime();
        System.out.println(end - start);

        writeOutput("output/p/outputJ_" + k + "_" + n + "_" + m + ".txt");
    }

    private void writeOutput(String fileName) throws IOException {
        String filePath = "C:\\Users\\redis\\Desktop\\Projects\\Semestrul-5-Ubb\\PPD\\Lab2\\" + fileName;
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {
            for (int i = 1; i <= n; i++) {
                for (int j = 1; j <= m; j++) {
                    writer.write(matrice[i][j] + " ");
                }
                writer.newLine();
            }
        }
    }

    public void run(int mode, int threads) throws IOException {
        switch (mode) {
            case 1 -> sequential();
            case 2 -> parallel(threads);
            default -> throw new IllegalArgumentException("Invalid mode: " + mode);
        }
    }

    public static void main(String[] args) {
        if (args.length < 3) {
            System.err.println("Usage: java Convolutie <input_file> <threads> <mode>");
            return;
        }

        try {
            int threads = Integer.parseInt(args[1]);
            int mode = Integer.parseInt(args[2]);
            Convolutie conv = new Convolutie(args[0]);
            conv.run(mode, threads);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}