import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

public class Convolutie {
    private final int[][] C;
    private final int[][] matrice;
    private int[][] matriceRez;
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
            matriceRez = new int[n + 1][m + 1];
        }
    }

    private int claim(int x, int y) {
        return matrice[Math.min(n, Math.max(x, 1))][Math.min(m, Math.max(y, 1))];
    }

    private int conv(int i, int j) {
        int sum = 0;
        int lim = k / 2;
        for (int x = -lim; x <= lim; x++) {
            for (int y = -lim; y <= lim; y++) {
                sum += claim(i + x, j + y) * C[x + lim][y + lim];
            }
        }
        return sum;
    }

    public void sequential() throws IOException {
        long start = System.nanoTime();

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                matriceRez[i][j] = conv(i, j);
            }
        }

        long end = System.nanoTime();
        System.out.println(end - start);

        writeOutput("output/sec/outputJ_" + k + "_" + n + "_" + m + ".txt");
    }

    public void parallelRows(int threads) throws IOException {
        long start = System.nanoTime();

        Thread[] threadPool = new Thread[threads];
        int rowsPerThread = n / threads;

        for (int t = 0; t < threads; t++) {
            int startRow = t * rowsPerThread + 1;
            int endRow = (t == threads - 1) ? n : (t + 1) * rowsPerThread;

            threadPool[t] = new Thread(() -> {
                for (int i = startRow; i <= endRow; i++) {
                    for (int j = 1; j <= m; j++) {
                        matriceRez[i][j] = conv(i, j);
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

        writeOutput("output/po/outputJ_" + k + "_" + n + "_" + m + ".txt");
    }

    public void parallelColumns(int threads) throws IOException {
        long start = System.nanoTime();

        Thread[] threadPool = new Thread[threads];
        int colsPerThread = m / threads;

        for (int t = 0; t < threads; t++) {
            int startCol = t * colsPerThread + 1;
            int endCol = (t == threads - 1) ? m : (t + 1) * colsPerThread;

            threadPool[t] = new Thread(() -> {
                for (int i = 1; i <= n; i++) {
                    for (int j = startCol; j <= endCol; j++) {
                        matriceRez[i][j] = conv(i, j);
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

        writeOutput("output/pv/outputJ_" + k + "_" + n + "_" + m + ".txt");
    }

    private void writeOutput(String fileName) throws IOException {
        String filePath = "C:\\Users\\redis\\Desktop\\Projects\\Semestrul-5-Ubb\\PPD\\Lab1\\" + fileName;
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {
            for (int i = 1; i <= n; i++) {
                for (int j = 1; j <= m; j++) {
                    writer.write(matriceRez[i][j] + " ");
                }
                writer.newLine();
            }
        }
    }

    public void run(int mode, int threads) throws IOException {
        switch (mode) {
            case 1 -> sequential();
            case 2 -> parallelRows(threads);
            case 3 -> parallelColumns(threads);
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