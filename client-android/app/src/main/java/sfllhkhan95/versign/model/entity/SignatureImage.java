package sfllhkhan95.versign.model.entity;

import android.graphics.Bitmap;

import org.opencv.android.Utils;
import org.opencv.core.Mat;

import java.util.Arrays;


public class SignatureImage {

    private String pixelData;
    private final int width;
    private final int height;

    public SignatureImage(final Bitmap bitmap) {
        this.width = bitmap.getWidth();
        this.height = bitmap.getHeight();
        this.pixelData = "";

        Mat mat = new Mat();
        Utils.bitmapToMat(bitmap, mat);
        for (int row = 0; row < mat.rows(); row++) {
            for (int col = 0; col < mat.cols(); col++) {
                pixelData += Arrays.toString(mat.get(row, col)) + ", ";
            }
            pixelData += "\n";
        }
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