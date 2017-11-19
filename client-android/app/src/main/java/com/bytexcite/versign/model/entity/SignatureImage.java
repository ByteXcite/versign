package com.bytexcite.versign.model.entity;

import android.graphics.Bitmap;

import java.io.Serializable;

public class SignatureImage implements Serializable {

    private int[][] pixelData;
    private int width;
    private int height;

    public SignatureImage() {
        // No-arg constructor for serialisation
    }

    public SignatureImage(final Bitmap bitmap) {
        this.width = bitmap.getWidth();
        this.height = bitmap.getHeight();

        this.pixelData = extractPixels(bitmap);
    }

    private int[][] extractPixels(Bitmap bitmap) {
        int[][] pixels = new int[this.width][this.height];
        for (int x = 0; x < this.width; x++) {
            for (int y = 0; y < this.height; y++) {
                pixels[x][y] = bitmap.getPixel(x, y);
            }
        }
        return pixels;
    }

    public int[][] getPixelData() {
        return pixelData;
    }

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return height;
    }

}