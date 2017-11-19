package com.bytexcite.versign.model.entity;

import android.graphics.Bitmap;

public class SignatureImage {

    private final int width;
    private final int height;
    public Bitmap bitmap;
    private String pixelData;

    public SignatureImage(final Bitmap bitmap) {
        this.width = bitmap.getWidth();
        this.height = bitmap.getHeight();
        this.pixelData = "";
        this.bitmap = bitmap;
    }

    public String getPixelData() {
        return pixelData;
    }

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return height;
    }

}