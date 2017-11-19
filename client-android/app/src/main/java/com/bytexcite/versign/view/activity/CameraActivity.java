package com.bytexcite.versign.view.activity;

import android.app.Dialog;
import android.content.DialogInterface;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.hardware.Camera;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.support.annotation.Nullable;
import android.support.annotation.UiThread;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.bytexcite.versign.R;
import com.bytexcite.versign.controller.VerificationController;
import com.bytexcite.versign.model.entity.Customer;
import com.bytexcite.versign.model.entity.SignatureImage;
import com.bytexcite.versign.model.entity.VerificationResponse;
import com.bytexcite.versign.view.CameraPreview;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.MalformedURLException;

import sfllhkhan95.android.rest.ResponseHandler;


public class CameraActivity extends AppCompatActivity implements View.OnClickListener,
        Camera.PictureCallback, ResponseHandler<VerificationResponse> {

    private FrameLayout cameraLayout;
    private Button captureButton;
    private EditText customerID;

    private String storageError;
    private String writeError;
    private String cameraError;
    private String appName;
    private String customerError;
    private String verificationSuccess;

    private Dialog preparingSignatureDialog;
    private Dialog verifyingSignatureDialog;
    private Dialog verificationSuccessDialog;
    private Dialog verificationFailureDialog;
    private Dialog verificationErrorDialog;

    private VerificationController verificationController;

    private Camera camera;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camera);

        cameraLayout = (FrameLayout) findViewById(R.id.cameraView);
        captureButton = (Button) findViewById(R.id.scanButton);
        customerID = (EditText) findViewById(R.id.customerID);

        storageError = getString(R.string.storageError);
        writeError = getString(R.string.writeError);
        cameraError = getString(R.string.cameraError);
        appName = getString(R.string.app_name);
        customerError = getString(R.string.customerError);
        verificationSuccess = getString(R.string.verificationSuccess);

        try {
            verificationController = new VerificationController();
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }

        captureButton.setOnClickListener(this);

        preparingSignatureDialog = new Dialog(CameraActivity.this);
        preparingSignatureDialog.setContentView(R.layout.dialog_preparing_signature);

        verifyingSignatureDialog = new Dialog(CameraActivity.this);
        verifyingSignatureDialog.setContentView(R.layout.dialog_verifying_signature);

        verificationSuccessDialog = new Dialog(CameraActivity.this);
        verificationSuccessDialog.setContentView(R.layout.dialog_signature_forged);

        verificationFailureDialog = new Dialog(CameraActivity.this);
        verificationFailureDialog.setContentView(R.layout.dialog_signature_forged);

        verificationErrorDialog = new Dialog(CameraActivity.this);
        verificationErrorDialog.setContentView(R.layout.dialog_verification_error);


        try {
            this.camera = Camera.open();

            CameraPreview cameraPreview = new CameraPreview(CameraActivity.this, camera);
            cameraLayout.addView(cameraPreview);
        } catch (Exception ex) {
            Toast.makeText(this, cameraError, Toast.LENGTH_SHORT).show();
        }
    }

    /**
     * Create output file where captured image will be written.
     *
     * @return output file
     * @throws RuntimeException execption thrown if output file cannot be created
     */
    @Nullable
    private File createImageFile() throws RuntimeException {
        // Create a directory name for image storage
        File mediaStorageDir = new File(
                Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES),
                appName
        );

        // If directory name does not exist, create required directories
        if (!mediaStorageDir.exists()) {
            if (!mediaStorageDir.mkdirs()) {
                throw new RuntimeException();
            }
        }

        // Create and return an image file name
        return new File(mediaStorageDir.getPath() + File.separator
                + "_TMP_VERSIGN_LAST_SCAN.jpg");
    }

    /**
     * Saves captured image to storage
     *
     * @param data image data
     * @return output file
     * @throws IOException if file cannot be created or written to
     */
    @Nullable
    private File saveImageData(byte[] data) throws IOException {
        File imageFile = null;
        try {
            imageFile = createImageFile();
            FileOutputStream fos = new FileOutputStream(imageFile);
            fos.write(data);
            fos.close();
        } catch (NullPointerException ex) {
            throw new IOException();
        }

        return imageFile;
    }

    /**
     * Reads image file from storage
     *
     * @param file image file path
     * @return bitmap of the image read
     */
    private Bitmap readCapturedImage(File file) {
        BitmapFactory.Options options = new BitmapFactory.Options();
        options.inPreferredConfig = Bitmap.Config.ARGB_8888;
        return BitmapFactory.decodeFile(file.getAbsolutePath(), options);
    }

    @Override
    public void onClick(View v) {
        if (v.getId() == R.id.scanButton) {
            String ID = customerID.getText().toString().trim();

            if (ID.equals("") || ID.length() != 13) {
                Toast.makeText(CameraActivity.this, customerError, Toast.LENGTH_SHORT).show();
            } else {
                try {
                    camera.takePicture(null, null, this);
                } catch (NullPointerException ex) {
                    Toast.makeText(CameraActivity.this, cameraError, Toast.LENGTH_SHORT).show();
                }
            }
        }
    }

    @Override
    public void onPictureTaken(byte[] data, Camera camera) {
        try {
            File pictureFile = saveImageData(data);
            final Bitmap bitmap = readCapturedImage(pictureFile);
            sendVerificationRequest(bitmap);
        } catch (RuntimeException e) {
            Toast.makeText(CameraActivity.this, storageError, Toast.LENGTH_SHORT).show();
        } catch (IOException e) {
            Toast.makeText(CameraActivity.this, writeError, Toast.LENGTH_SHORT).show();
        }
    }

    @UiThread
    private void sendVerificationRequest(Bitmap bitmap) {
        preparingSignatureDialog.show();
        new AsyncTask<Bitmap, Void, Void>() {
            SignatureImage signatureImage = null;

            @Override
            protected Void doInBackground(Bitmap... params) {
                signatureImage = new SignatureImage(params[0]);
                return null;
            }

            @Override
            public void onPostExecute(Void response) {
                preparingSignatureDialog.hide();

                ImageView sign = (ImageView) verifyingSignatureDialog.findViewById(R.id.signature);
                sign.setImageBitmap(signatureImage.bitmap);

                verifyingSignatureDialog.show();

                String ID = customerID.getText().toString().trim();

                // Send verification request
                verificationController
                        .getVerificationRequest(ID, signatureImage)
                        .sendRequest(CameraActivity.this);
            }
        }.execute(bitmap);
    }

    @Override
    public void onResponseReceived(@Nullable VerificationResponse verificationResponse) {
        verifyingSignatureDialog.hide();
        if (verificationResponse != null) {
            if (verificationResponse.isGenuine()) {
                verificationSuccessDialog.show();

                Customer belongsTo = verificationResponse.getBelongsTo();

                ((TextView) verificationSuccessDialog.findViewById(R.id.customerDetails))
                        .setText("Customer: " + belongsTo.getFirstName());
            } else {
                verificationFailureDialog.show();
            }
        } else {
            verificationErrorDialog.show();
            verificationErrorDialog.setOnDismissListener(new DialogInterface.OnDismissListener() {
                @Override
                public void onDismiss(DialogInterface dialog) {
                    recreate();
                }
            });
        }
    }

}