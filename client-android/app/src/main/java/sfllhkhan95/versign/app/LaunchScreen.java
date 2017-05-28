package sfllhkhan95.versign.app;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;

import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.LoaderCallbackInterface;

import sfllhkhan95.versign.R;

public class LaunchScreen extends AppCompatActivity {

    private BaseLoaderCallback openCVLoader = new BaseLoaderCallback(this) {
        @Override
        public void onManagerConnected(int status) {
            switch (status) {
                case LoaderCallbackInterface.SUCCESS: {
                    Log.i("OpenCV", "OpenCV loaded successfully");
                }
                break;
                default: {
                    super.onManagerConnected(status);
                }
                break;
            }
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_launch_screen);

        startActivity(new Intent(this, CameraActivity.class));
    }

    @Override
    public void onResume() {
        super.onResume();
        /*if (!OpenCVLoader.initDebug()) {
            Log.d("OpenCV", "Internal OpenCV library not found. Using OpenCV Manager for initialization");
            OpenCVLoader.initAsync(OpenCVLoader.OPENCV_VERSION_3_0_0, this, openCVLoader);
        } else {
            Log.d("OpenCV", "OpenCV library found inside package. Using it!");
            openCVLoader.onManagerConnected(LoaderCallbackInterface.SUCCESS);
        }*/
    }

}
