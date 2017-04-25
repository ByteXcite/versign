package sfllhkhan95.versign;

import android.graphics.Bitmap;
import android.graphics.Color;

/**
 * Created by saifkhichi96 on 25/04/2017.
 */

public class ImageProcessor {

    public Bitmap makeBinary(Bitmap bitmap) {
        Bitmap binary = bitmap.copy(Bitmap.Config.ARGB_8888, true);


        for (int x = 0; x < binary.getWidth(); x++) {
            for (int y = 0; y < binary.getHeight(); y++) {
                int color = binary.getPixel(x, y);
                int R = (color >> 16) & 0xff;
                int G = (color >>  8) & 0xff;
                int B = (color      ) & 0xff;
                color = (R + G + B)/3;
                System.out.printf("(%d, %d, %d) -> %d", R, G, B, color);

                if (color < 128) {
                    binary.setPixel(x, y, Color.parseColor("#000000"));
                } else {
                    binary.setPixel(x, y, Color.parseColor("#ffffff"));
                }
            }
        }
        return binary;
    }

}
