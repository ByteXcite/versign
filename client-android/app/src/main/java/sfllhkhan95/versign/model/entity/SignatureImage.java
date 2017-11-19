package sfllhkhan95.versign.model.entity;

import android.graphics.Bitmap;

import org.opencv.android.Utils;
import org.opencv.core.Mat;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;


public class SignatureImage {

    private String pixelData;
    private final int width;
    private final int height;
    public Bitmap bitmap;

    public SignatureImage(final Bitmap bitmap) {
        this.width = bitmap.getWidth();
        this.height = bitmap.getHeight();
        this.pixelData = "";
        this.bitmap = bitmap;

        Mat imageMat = new Mat();
        Utils.bitmapToMat(bitmap, imageMat);
        Imgproc.cvtColor(imageMat, imageMat, Imgproc.COLOR_BGR2GRAY);
        Imgproc.GaussianBlur(imageMat, imageMat, new Size(3, 3), 0);
        Imgproc.threshold(imageMat, imageMat, 0, 255, Imgproc.THRESH_OTSU);
        Utils.matToBitmap(imageMat, this.bitmap);
        //Mat mat = new Mat();
        //Utils.bitmapToMat(bitmap, mat);
        //for (int row = 0; row < mat.rows(); row++) {
        //    for (int col = 0; col < mat.cols(); col++) {
        //        pixelData += Arrays.toString(mat.get(row, col)) + ", ";
        //    }
        //    pixelData += "\n";
        //}
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