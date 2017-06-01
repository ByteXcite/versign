package sfllhkhan95.versign.view.activity;

import android.content.Intent;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.util.Log;

import com.google.inject.Inject;

import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.LoaderCallbackInterface;
import org.opencv.android.OpenCVLoader;

import roboguice.activity.RoboActivity;
import roboguice.inject.ContentView;
import sfllhkhan95.versign.R;
import sfllhkhan95.versign.model.entity.SessionData;

/**
 * LaunchScreen is the Launcher Activity, which is the entry point of application. The application
 * starts with this screen which is displayed for a few seconds.
 */
@ContentView(R.layout.activity_launch_screen)
public class LaunchScreen extends RoboActivity {

    /**
     * SessionData object containing data of currently signed in user
     */
    @Inject
    private SessionData sessionData;

    /**
     * Loader callback used for loading OpenCV.
     */
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
        LaunchScreenController controller = new LaunchScreenController();
        controller.startTimer();
    }

    /**
     * Overrider of onResume method of Activity class. Called when activity starts/resumes.
     * Loads OpenCV if it is not already loaded.
     */
    @Override
    public void onResume() {
        super.onResume();
        if (OpenCVLoader.initDebug()) {
            Log.d("OpenCV", "OpenCV library found inside package. Using it!");
            openCVLoader.onManagerConnected(LoaderCallbackInterface.SUCCESS);
        } else {
            Log.d("OpenCV", "Internal OpenCV library not found. Using OpenCV Manager for initialization");
            OpenCVLoader.initAsync(OpenCVLoader.OPENCV_VERSION_3_0_0, this, openCVLoader);
        }
    }

    private class LaunchScreenController {

        private Intent showLoginForm;
        private Intent launchCameraActivity;

        private CountDownTimer launchScreenTimer;

        LaunchScreenController() {
            showLoginForm = new Intent(LaunchScreen.this, LoginActivity.class);
            launchCameraActivity = new Intent(LaunchScreen.this, CameraActivity.class);

            launchScreenTimer = new CountDownTimer(3000, 3000) {
                @Override
                public void onTick(long millisUntilFinished) {

                }

                @Override
                public void onFinish() {
                    startNextActivity(
                            sessionData.getCurrentUser() == null
                                    ? showLoginForm
                                    : launchCameraActivity
                    );
                }
            };
        }

        private void startNextActivity(Intent intent) {
            startActivity(intent);
            overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
            finish();
        }

        void startTimer() {
            launchScreenTimer.start();
        }
    }

}