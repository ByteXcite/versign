package com.bytexcite.verisign.view;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;

import com.bytexcite.verisign.R;
import com.bytexcite.verisign.model.entity.SessionData;

import java.util.Timer;
import java.util.TimerTask;

/**
 * LaunchScreen is the Launcher Activity, which is the entry point of application. The application
 * starts with this screen which is displayed for a few seconds.
 */
public class LaunchScreen extends AppCompatActivity {

    private final long delay = 1500L;
    private final int CAMERA_PERMISSION_TAG = 200;
    private final int STORAGE_PERMISSION_TAG = 400;


    /**
     * SessionData object containing data of currently signed in user
     */
    private SessionData sessionData;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_launch_screen);
        sessionData = SessionData.getInstance(this);

        if (checkPermissions()) {
            LaunchScreenController controller = new LaunchScreenController(delay);
            controller.startTimer();
        }
    }

    private boolean checkPermissions() {
        if (!isGranted(Manifest.permission.CAMERA) || !isGranted(Manifest.permission.WRITE_EXTERNAL_STORAGE)) {
            if (!isGranted(Manifest.permission.CAMERA)) {
                requestPermission(Manifest.permission.CAMERA, CAMERA_PERMISSION_TAG);
            }

            if (!isGranted(Manifest.permission.WRITE_EXTERNAL_STORAGE)) {
                requestPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE, STORAGE_PERMISSION_TAG);
            }
            return false;
        }

        return true;
    }

    private boolean isGranted(String permission) {
        return ContextCompat.checkSelfPermission(this, permission) == PackageManager.PERMISSION_GRANTED;
    }

    private void requestPermission(String permission, int tag) {
        ActivityCompat.requestPermissions(this, new String[]{permission}, tag);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String permissions[], @NonNull int[] grantResults) {
        switch (requestCode) {
            case CAMERA_PERMISSION_TAG:
            case STORAGE_PERMISSION_TAG:
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    LaunchScreenController controller = new LaunchScreenController(delay);
                    controller.startTimer();
                } else {
                    finish();
                }
                break;
        }
    }

    private class LaunchScreenController {

        private final long delay;

        private Intent showLoginForm;
        private Intent launchCameraActivity;

        LaunchScreenController(long delay) {
            this.delay = delay;
            showLoginForm = new Intent(LaunchScreen.this, LoginActivity.class);
            launchCameraActivity = new Intent(LaunchScreen.this, MenuMainActivity.class);
        }

        private void startNextActivity(Intent intent) {
            startActivity(intent);
            overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
            finish();
        }

        void startTimer() {
            new Timer().schedule(new TimerTask() {
                @Override
                public void run() {
                    startNextActivity(
                            sessionData.getActiveUser() == null
                                    ? showLoginForm
                                    : launchCameraActivity
                    );
                }
            }, delay);
        }
    }

}