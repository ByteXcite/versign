package com.bytexcite.versign.view.activity;

import android.app.AlertDialog;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.ImageView;

import com.bytexcite.versign.R;
import com.bytexcite.versign.model.entity.SignatureImage;

public class RegisterUserActivity extends AppCompatActivity implements View.OnClickListener {


    private static int RESULT_LOAD_IMAGE = 1;

    private int activeSignature = 1;
    private SignatureImage[] signatures = new SignatureImage[4];
    private boolean[] loaded = new boolean[]{false, false, false, false};

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register_user);

        findViewById(R.id.buttonChoosePicture).setOnClickListener(this);
        findViewById(R.id.buttonTakePicture).setOnClickListener(this);
        findViewById(R.id.registerUser).setOnClickListener(this);

        findViewById(R.id.sigantureImage1).setOnClickListener(this);
        findViewById(R.id.sigantureImage2).setOnClickListener(this);
        findViewById(R.id.sigantureImage3).setOnClickListener(this);
        findViewById(R.id.sigantureImage4).setOnClickListener(this);

        findViewById(R.id.loadingSign1).setVisibility(View.GONE);
        findViewById(R.id.loadingSign2).setVisibility(View.GONE);
        findViewById(R.id.loadingSign3).setVisibility(View.GONE);
        findViewById(R.id.loadingSign4).setVisibility(View.GONE);

        findViewById(R.id.loadingComplete1).setVisibility(View.GONE);
        findViewById(R.id.loadingComplete2).setVisibility(View.GONE);
        findViewById(R.id.loadingComplete3).setVisibility(View.GONE);
        findViewById(R.id.loadingComplete4).setVisibility(View.GONE);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == RESULT_LOAD_IMAGE && resultCode == RESULT_OK && null != data) {

            // Show selected image
            ImageView signatureView;
            switch (activeSignature) {
                case 2:
                    signatureView = (ImageView) findViewById(R.id.sigantureImage2);
                    findViewById(R.id.loadingSign2).setVisibility(View.VISIBLE);
                    findViewById(R.id.loadingComplete2).setVisibility(View.GONE);
                    break;

                case 3:
                    signatureView = (ImageView) findViewById(R.id.sigantureImage3);
                    findViewById(R.id.loadingSign3).setVisibility(View.VISIBLE);
                    findViewById(R.id.loadingComplete3).setVisibility(View.GONE);
                    break;

                case 4:
                    signatureView = (ImageView) findViewById(R.id.sigantureImage4);
                    findViewById(R.id.loadingSign4).setVisibility(View.VISIBLE);
                    findViewById(R.id.loadingComplete4).setVisibility(View.GONE);
                    break;

                default:
                    signatureView = (ImageView) findViewById(R.id.sigantureImage1);
                    findViewById(R.id.loadingSign1).setVisibility(View.VISIBLE);
                    findViewById(R.id.loadingComplete1).setVisibility(View.GONE);
                    break;
            }
            Uri selectedImageUri = data.getData();
            signatureView.setImageURI(selectedImageUri);

            // Get bitmap
            Drawable drawable = signatureView.getDrawable();
            final Bitmap bitmap = ((BitmapDrawable) drawable).getBitmap();

            // Extract pixel data from bitmap
            final int index = activeSignature;
            new Thread(new Runnable() {
                @Override
                public void run() {
                    signatures[index - 1] = new SignatureImage(bitmap);
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            switch (index) {
                                case 2:
                                    findViewById(R.id.loadingSign2).setVisibility(View.GONE);
                                    findViewById(R.id.loadingComplete2).setVisibility(View.VISIBLE);
                                    loaded[1] = true;
                                    break;
                                case 3:
                                    findViewById(R.id.loadingSign3).setVisibility(View.GONE);
                                    findViewById(R.id.loadingComplete3).setVisibility(View.VISIBLE);
                                    loaded[2] = true;
                                    break;
                                case 4:
                                    findViewById(R.id.loadingSign4).setVisibility(View.GONE);
                                    findViewById(R.id.loadingComplete4).setVisibility(View.VISIBLE);
                                    loaded[3] = true;
                                    break;
                                default:
                                    findViewById(R.id.loadingSign1).setVisibility(View.GONE);
                                    findViewById(R.id.loadingComplete1).setVisibility(View.VISIBLE);
                                    loaded[0] = true;
                                    break;
                            }
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
                Intent i = new Intent(
                        Intent.ACTION_PICK,
                        android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);

                startActivityForResult(i, RESULT_LOAD_IMAGE);
                break;

            case R.id.sigantureImage1:
                activeSignature = 1;
                updateUI();
                break;

            case R.id.sigantureImage2:
                activeSignature = 2;
                updateUI();
                break;

            case R.id.sigantureImage3:
                activeSignature = 3;
                updateUI();
                break;

            case R.id.sigantureImage4:
                activeSignature = 4;
                updateUI();
                break;

            case R.id.registerUser:
                if (loaded[0] && loaded[1] && loaded[2] && loaded[3]) {
                    // TODO: Initiate verification request
                    // UploadFileAsync task = new UploadFileAsync();
                    // new UploadFileAsync().execute(selectedImageUri.toString());
                    // task.execute(new String[]{"http://www.vogella.com/index.html"});
                } else {
                    // Show 'select signature image' dialog
                    new AlertDialog.Builder(RegisterUserActivity.this)
                            .setTitle("Signatures Not Selected")
                            .setMessage("Please select all four signature images to register new user.")
                            .create()
                            .show();
                }
                break;
        }
    }

    private void updateUI() {
        findViewById(R.id.sigantureImage1).setBackgroundResource(R.drawable.btn_default);
        findViewById(R.id.sigantureImage2).setBackgroundResource(R.drawable.btn_default);
        findViewById(R.id.sigantureImage3).setBackgroundResource(R.drawable.btn_default);
        findViewById(R.id.sigantureImage4).setBackgroundResource(R.drawable.btn_default);

        switch (activeSignature) {
            case 2:
                findViewById(R.id.sigantureImage2).setBackgroundResource(R.drawable.btn_pressed);
                break;

            case 3:
                findViewById(R.id.sigantureImage3).setBackgroundResource(R.drawable.btn_pressed);
                break;

            case 4:
                findViewById(R.id.sigantureImage4).setBackgroundResource(R.drawable.btn_pressed);
                break;

            default:
                findViewById(R.id.sigantureImage1).setBackgroundResource(R.drawable.btn_pressed);
                break;
        }
    }
}
