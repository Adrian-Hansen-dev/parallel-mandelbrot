#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define STB_IMAGE_IMPLEMENTATION
#include "../include/stb_image.h"

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "../include/stb_image_write.h"

int main() {
    int width = 800, height = 600, channels = 3;
    int total_pixels = width * height;
    unsigned char *img = (unsigned char *)malloc(total_pixels * channels);
    
    // Fill with a gray color
    for (int i = 0; i < total_pixels * channels; i++) {
        img[i] = 150; 
    }

    printf("Processing %dx%d image using %d OpenMP threads...\n", width, height, omp_get_max_threads());

    // Parallel processing with OpenMP
    #pragma omp parallel for
    for (int i = 0; i < total_pixels; i++) {
        int idx = i * channels;
        // Invert the colors
        img[idx + 0] = 255 - img[idx + 0]; // R
        img[idx + 1] = 255 - img[idx + 1]; // G
        img[idx + 2] = 255 - img[idx + 2]; // B
    }

    stbi_write_png("output.png", width, height, channels, img, width * channels);
    printf("Image saved as output.png\n");

    free(img);
    return 0;
}