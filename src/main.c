#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define STB_IMAGE_IMPLEMENTATION
#include "../include/stb_image.h"

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "../include/stb_image_write.h"


int main() {
    // 1. Inputs und Parameter definieren [cite: 38]
    // Wir nutzen hier direkt die 2048x2048 Auflösung, die du für das Benchmarking in deinem Bericht brauchst[cite: 54].
    int w = 4048; 
    int h = 4048; 
    int maxIterations = 1000; // Typischer Wert für gute Details [cite: 45]

    // Der Standard-Viewport (Sichtfenster) aus dem Dokument [cite: 42]
    float min_x = -2.0f;
    float min_y = -1.0f;
    float max_x = 1.0f;
    float max_y = 1.0f;

    // Speicher für das Bild reservieren (Breite * Höhe * 3 Farbkanäle für RGB)
    // Das Array liegt flach im Speicher, wir berechnen den Index für jedes Pixel manuell.
    unsigned char *image = (unsigned char *)malloc(w * h * 3);
    if (image == NULL) {
        printf("Fehler: Nicht genug Speicher!\n");
        return 1;
    }

    printf("Starte Mandelbrot Berechnung...\n");

    // 2. Die parallele Schleife mit OpenMP [cite: 5, 6]
    // 'schedule(dynamic)' ist hier extrem wichtig, da manche Pixel nach 2 Iterationen abbrechen, 
    // andere aber die vollen 1000 brauchen. So werden die CPU-Kerne gleichmäßig ausgelastet.
    #pragma omp parallel for schedule(dynamic)
    for (int py = 0; py < h; py++) {
        for (int px = 0; px < w; px++) {
            
            // Umrechnung der Pixelkoordinaten in das Sichtfenster (normalizeToViewRectangle) [cite: 21, 43]
            float cx = min_x + ((float)px / (w - 1)) * (max_x - min_x);
            float cy = min_y + ((float)py / (h - 1)) * (max_y - min_y);

            // Startwerte setzen [cite: 22, 23]
            float zx = cx;
            float zy = cy;
            
            int n;
            // Die mathematische Iteration [cite: 24]
            for (n = 0; n < maxIterations; n++) {
                // Formel berechnen: z_{n+1} = c + z_n^2 aufgeteilt in x und y [cite: 25, 26]
                float x = (zx * zx - zy * zy) + cx;
                float y = (zy * zx + zx * zy) + cy;

                // Abbruchbedingung prüfen: divergiert der Wert? [cite: 27]
                if ((x * x + y * y) > 4.0f) {
                    break; // Raus aus der Schleife!
                }
                
                // Werte für die nächste Runde speichern [cite: 32, 33]
                zx = x;
                zy = y;
            }

            // 3. Farbe berechnen und ins Array schreiben [cite: 29, 34]
            // Der Index im 1D-Array für ein 2D-Bild mit 3 Farbkanälen (RGB)
            int pixel_index = (py * w + px) * 3; 

            if (n == maxIterations) {
                // Punkt ist IN der Menge (nicht divergiert) -> Schwarz [cite: 34]
                image[pixel_index + 0] = 0;   // Rot
                image[pixel_index + 1] = 0;   // Grün
                image[pixel_index + 2] = 0;   // Blau
            } else {
                // Punkt divergiert -> Bunt machen (simpler Farbverlauf basierend auf n) [cite: 28, 29]
                // Wir nutzen den Modulo-Operator (%), um schöne, sich wiederholende Farben zu erzeugen.
                image[pixel_index + 0] = (n * 5) % 256;       // Rot
                image[pixel_index + 1] = (n * 2) % 256;       // Grün
                image[pixel_index + 2] = (n * 10) % 256;      // Blau
            }
        }
    }

    printf("Berechnung fertig! Speichere Bild...\n");

    // 4. Bild auf die Festplatte schreiben [cite: 46]
    stbi_write_png("mandelbrot_parallel.png", w, h, 3, image, w * 3);

    // 5. Speicher freigeben (Proper cooperative shutdown) [cite: 57]
    free(image);

    printf("Erledigt. Bild als 'mandelbrot_parallel.png' gespeichert.\n");
    return 0;
}