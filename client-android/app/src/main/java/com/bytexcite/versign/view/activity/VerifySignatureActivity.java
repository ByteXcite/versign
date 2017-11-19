package com.bytexcite.versign.view.activity;

import android.app.AlertDialog;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.ImageView;

import com.bytexcite.versign.R;
import com.bytexcite.versign.controller.VerificationController;
import com.bytexcite.versign.model.entity.SignatureImage;
import com.bytexcite.versign.model.entity.VerificationResponse;

import java.net.MalformedURLException;

import sfllhkhan95.android.rest.ResponseHandler;

public class VerifySignatureActivity extends AppCompatActivity
        implements View.OnClickListener, ResponseHandler<VerificationResponse> {

    private static int RESULT_LOAD_IMAGE = 1;

    private SignatureImage signature = null;
    private boolean isLoading = false;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_verify_signature);

        findViewById(R.id.buttonChoosePicture).setOnClickListener(this);
        findViewById(R.id.buttonTakePicture).setOnClickListener(this);
        findViewById(R.id.verifySignature).setOnClickListener(this);
        findViewById(R.id.reset).setOnClickListener(this);

        findViewById(R.id.loadingSign).setVisibility(View.GONE);
        findViewById(R.id.loadingComplete).setVisibility(View.GONE);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == RESULT_LOAD_IMAGE && resultCode == RESULT_OK && null != data) {
            findViewById(R.id.loadingSign).setVisibility(View.VISIBLE);
            findViewById(R.id.loadingComplete).setVisibility(View.GONE);
            signature = null;

            // Show selected image
            ImageView signatureView = (ImageView) findViewById(R.id.sigantureImage);

            Uri selectedImageUri = data.getData();
            signatureView.setImageURI(selectedImageUri);

            // Get bitmap
            Drawable drawable = signatureView.getDrawable();
            final Bitmap bitmap = ((BitmapDrawable) drawable).getBitmap();

            // Extract pixel data from bitmap
            isLoading = true;
            new Thread(new Runnable() {
                @Override
                public void run() {
                    signature = new SignatureImage(bitmap);
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            findViewById(R.id.loadingSign).setVisibility(View.GONE);
                            findViewById(R.id.loadingComplete).setVisibility(View.VISIBLE);

                            isLoading = false;

                            findViewById(R.id.verify).setVisibility(View.VISIBLE);

                            findViewById(R.id.buttonTakePicture).setVisibility(View.GONE);
                            findViewById(R.id.buttonChoosePicture).setVisibility(View.GONE);
                        }
                    });
                }
            }).start();
        }
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.buttonChoosePicture:
                if (!isLoading) {
                    Intent i = new Intent(
                            Intent.ACTION_PICK,
                            MediaStore.Images.Media.EXTERNAL_CONTENT_URI);

                    startActivityForResult(i, RESULT_LOAD_IMAGE);
                }
                break;

            case R.id.buttonTakePicture:
                if (!isLoading) {
                    Intent i = new Intent(
                            getApplicationContext(),
                            CameraActivity.class);

                    startActivityForResult(i, RESULT_LOAD_IMAGE);
                }
                break;

            case R.id.verifySignature:
                if (signature == null) {
                    // Show 'select signature image' dialog
                    new AlertDialog.Builder(VerifySignatureActivity.this)
                            .setTitle("Signature Not Selected")
                            .setMessage("Please select a signature image to verify.")
                            .create()
                            .show();
                } else {
                    // Initiate verification request
                    try {
                        VerificationController verificationController = new VerificationController();
                        findViewById(R.id.loadingSign).setVisibility(View.VISIBLE);

                        // Send verification request
                        verificationController
                                .getVerificationRequest("", signature)
                                .sendRequest(VerifySignatureActivity.this);
                    } catch (MalformedURLException e) {
                        e.printStackTrace();
                    }
                }
                break;

            case R.id.reset:
                ((ImageView) findViewById(R.id.sigantureImage)).setImageResource(R.drawable.placeholder);
                findViewById(R.id.loadingSign).setVisibility(View.INVISIBLE);
                findViewById(R.id.loadingComplete).setVisibility(View.INVISIBLE);

                findViewById(R.id.buttonChoosePicture).setVisibility(View.VISIBLE);
                findViewById(R.id.buttonTakePicture).setVisibility(View.VISIBLE);
                findViewById(R.id.verify).setVisibility(View.GONE);
                break;
        }
    }

    @Override
    public void onResponseReceived(@Nullable VerificationResponse verificationResponse) {
        findViewById(R.id.loadingSign).setVisibility(View.GONE);

        if (verificationResponse != null) {
            if (!verificationResponse.isGenuine()) {
                new AlertDialog.Builder(VerifySignatureActivity.this)
                        .setTitle("NOT GENUINE")
                        .setMessage("The signature does not match with the saved model of this user.")
                        .create()
                        .show();
            } else {
                new AlertDialog.Builder(VerifySignatureActivity.this)
                        .setTitle("GENUINE")
                        .setMessage("Signature belongs to claimant '" + verificationResponse.getBelongsTo().getNIC() + "'")
                        .create()
                        .show();
            }
        } else {
            new AlertDialog.Builder(VerifySignatureActivity.this)
                    .setMessage("Signature verification failed. Please try again.")
                    .create()
                    .show();
        }
    }

}
