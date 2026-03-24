#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define STB_IMAGE_IMPLEMENTATION
#include "../include/stb_image.h"

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "../include/stb_image_write.h"


int main(int argc, char *argv[]){
    int w = 2048;
    int h = 2048;
    int maxIterations = 1000;
    int threads = 0; // 0 = OpenMP entscheidet selbst
    float min_x = -2.0f;
    float min_y = -1.0f;
    float max_x = 1.0f;
    float max_y = 1.0f;

    if (argc == 3) {
        w = atoi(argv[1]);
        h = atoi(argv[2]);
    } else if (argc == 4) {
        w = atoi(argv[1]);
        h = atoi(argv[2]);
        maxIterations = atoi(argv[3]);
    } else if (argc == 5) {
        w = atoi(argv[1]);
        h = atoi(argv[2]);
        maxIterations = atoi(argv[3]);
        threads = atoi(argv[4]);
    } else if (argc == 8) {
        w = atoi(argv[1]);
        h = atoi(argv[2]);
        maxIterations = atoi(argv[3]);
        min_x = atof(argv[4]);
        min_y = atof(argv[5]);
        max_x = atof(argv[6]);
        max_y = atof(argv[7]);
    } else if (argc == 9) {
        w = atoi(argv[1]);
        h = atoi(argv[2]);
        maxIterations = atoi(argv[3]);
        min_x = atof(argv[4]);
        min_y = atof(argv[5]);
        max_x = atof(argv[6]);
        max_y = atof(argv[7]);
        threads = atoi(argv[8]);
    } else if (argc > 1) {
        printf("Verwendung: %s <Breite> <Hoehe> [maxIterations] [threads] [min_x min_y max_x max_y] [threads]\n", argv[0]);
        printf("Beispiel: %s 1024 1024 500 4\n", argv[0]);
        printf("Starte stattdessen mit Standardwerten...\n\n");
    }

    // Thread-Anzahl setzen falls angegeben
    if (threads > 0) {
        omp_set_num_threads(threads);
    }

    // Sicherheitscheck
    if (w <= 0 || h <= 0) {
        printf("Fehler: Breite und Hoehe muessen groesser als 0 sein!\n");
        return 1;
    }

    // Bild-Array anlegen (RGB = 3 Bytes pro Pixel)
    unsigned char *image = (unsigned char *)malloc(w * h * 3);
    if (image == NULL) {
        printf("Fehler: Nicht genug Speicher!\n");
        return 1;
    }

    printf("Einstellungen: %dx%d, maxIter=%d, Threads=%d, Viewport=(%.2f, %.2f, %.2f, %.2f)\n",
           w, h, maxIterations, omp_get_max_threads(), min_x, min_y, max_x, max_y);
    printf("Starte Mandelbrot Berechnung...\n");

    double start_time = omp_get_wtime();

    // Parallele Berechnung - dynamic weil manche Pixel viel mehr Iterationen brauchen als andere
    #pragma omp parallel for schedule(dynamic)
    for (int py = 0; py < h; py++) {
        for (int px = 0; px < w; px++) {

            // Pixel-Position in komplexe Zahl umrechnen
            float cx = min_x + ((float)px / (w - 1)) * (max_x - min_x);
            float cy = min_y + ((float)py / (h - 1)) * (max_y - min_y);

            // Startwerte setzen
            float zx = cx;
            float zy = cy;

            int n;
            // Mandelbrot Iteration
            for (n = 0; n < maxIterations; n++) {
                // z = z^2 + c
                float x = (zx * zx - zy * zy) + cx;
                float y = (zy * zx + zx * zy) + cy;

                // Divergiert?
                if ((x * x + y * y) > 4.0f) {
                    break;
                }

                // Naechste Runde
                zx = x;
                zy = y;
            }

            // Farbe setzen
            int pixel_index = (py * w + px) * 3;

            if (n == maxIterations) {
                // In der Menge -> Schwarz
                image[pixel_index + 0] = 0;   // Rot
                image[pixel_index + 1] = 0;   // Grün
                image[pixel_index + 2] = 0;   // Blau
            } else {
                // Ausserhalb -> Farbe basierend auf Iterationen
                image[pixel_index + 0] = (n * 5) % 256;       // Rot
                image[pixel_index + 1] = (n * 2) % 256;       // Grün
                image[pixel_index + 2] = (n * 10) % 256;      // Blau
            }
        }
    }

    double end_time = omp_get_wtime();
    double time_spent = end_time - start_time;

    printf("Berechnung fertig!\n\n");
    
    printf("--------------------------------------------------\n");
    printf(" BENÖTIGTE RECHENZEIT: %.4f Sekunden\n", time_spent);
    printf("--------------------------------------------------\n\n");

    printf("Speichere Bild...\n");
    // Bild speichern
    stbi_write_png("mandelbrot_parallel.png", w, h, 3, image, w * 3);

    // Speicher freigeben (Threads sind nach der Schleife schon fertig)
    free(image);

    printf("Erledigt. Bild als 'mandelbrot_parallel.png' gespeichert.\n");
    return 0;
}