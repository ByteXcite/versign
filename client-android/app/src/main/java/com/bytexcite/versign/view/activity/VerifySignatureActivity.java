package com.bytexcite.versign.view.activity;

import android.app.AlertDialog;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.ImageView;

import com.bytexcite.versign.R;
import com.bytexcite.versign.model.entity.SignatureImage;

import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class VerifySignatureActivity extends AppCompatActivity implements View.OnClickListener {

    private static int RESULT_LOAD_IMAGE = 1;
    private SignatureImage signature = null;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_verify_signature);

        findViewById(R.id.buttonChoosePicture).setOnClickListener(this);
        findViewById(R.id.buttonTakePicture).setOnClickListener(this);
        findViewById(R.id.verifySignature).setOnClickListener(this);

        findViewById(R.id.loadingSign).setVisibility(View.GONE);
        findViewById(R.id.loadingComplete).setVisibility(View.GONE);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == RESULT_LOAD_IMAGE && resultCode == RESULT_OK && null != data) {

            ImageView signatureView = (ImageView) findViewById(R.id.sigantureImage);
            findViewById(R.id.loadingSign).setVisibility(View.VISIBLE);
            findViewById(R.id.loadingComplete).setVisibility(View.GONE);

            // Show selected image
            Uri selectedImageUri = data.getData();
            signatureView.setImageURI(selectedImageUri);

            // Get bitmap
            Drawable drawable = signatureView.getDrawable();
            final Bitmap bitmap = ((BitmapDrawable) drawable).getBitmap();

            // Extract pixel data from bitmap
            new Thread(new Runnable() {
                @Override
                public void run() {
                    signature = new SignatureImage(bitmap);
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            findViewById(R.id.loadingSign).setVisibility(View.GONE);
                            findViewById(R.id.loadingComplete).setVisibility(View.VISIBLE);
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
                        MediaStore.Images.Media.EXTERNAL_CONTENT_URI);

                startActivityForResult(i, RESULT_LOAD_IMAGE);
                break;

            case R.id.buttonTakePicture:
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
                    // TODO: Initiate verification request
                    // UploadFileAsync task = new UploadFileAsync();
                    // new UploadFileAsync().execute(selectedImageUri.toString());
                    // task.execute(new String[]{"http://www.vogella.com/index.html"});
                }
                break;
        }
    }

    private class UploadFileAsync extends AsyncTask<String, Void, String> {

        @Override
        protected String doInBackground(String... params) {
            try {
                // String sourceFileUri = "/mnt/sdcard/abc.png";
                String sourceFileUri = params[0];

                HttpURLConnection conn = null;
                DataOutputStream dos = null;
                String lineEnd = "\r\n";
                String twoHyphens = "--";
                String boundary = "*****";
                int bytesRead, bytesAvailable, bufferSize;
                byte[] buffer;
                int maxBufferSize = 1 * 1024 * 1024;
                File sourceFile = new File(sourceFileUri);

                if (sourceFile.isFile()) {

                    try {
                        String upLoadServerUri = "http://website.com/abc.php?";

                        // open a URL connection to the Servlet
                        FileInputStream fileInputStream = new FileInputStream(
                                sourceFile);
                        URL url = new URL(upLoadServerUri);

                        // Open a HTTP connection to the URL
                        conn = (HttpURLConnection) url.openConnection();
                        conn.setDoInput(true); // Allow Inputs
                        conn.setDoOutput(true); // Allow Outputs
                        conn.setUseCaches(false); // Don't use a Cached Copy
                        conn.setRequestMethod("POST");
                        conn.setRequestProperty("Connection", "Keep-Alive");
                        conn.setRequestProperty("ENCTYPE",
                                "multipart/form-data");
                        conn.setRequestProperty("Content-Type",
                                "multipart/form-data;boundary=" + boundary);
                        conn.setRequestProperty("bill", sourceFileUri);

                        dos = new DataOutputStream(conn.getOutputStream());

                        dos.writeBytes(twoHyphens + boundary + lineEnd);
                        dos.writeBytes("Content-Disposition: form-data; name=\"bill\";filename=\""
                                + sourceFileUri + "\"" + lineEnd);

                        dos.writeBytes(lineEnd);

                        // create a buffer of maximum size
                        bytesAvailable = fileInputStream.available();

                        bufferSize = Math.min(bytesAvailable, maxBufferSize);
                        buffer = new byte[bufferSize];

                        // read file and write it into form...
                        bytesRead = fileInputStream.read(buffer, 0, bufferSize);

                        while (bytesRead > 0) {

                            dos.write(buffer, 0, bufferSize);
                            bytesAvailable = fileInputStream.available();
                            bufferSize = Math
                                    .min(bytesAvailable, maxBufferSize);
                            bytesRead = fileInputStream.read(buffer, 0,
                                    bufferSize);

                        }

                        // send multipart form data necesssary after file
                        // data...
                        dos.writeBytes(lineEnd);
                        dos.writeBytes(twoHyphens + boundary + twoHyphens
                                + lineEnd);

                        int serverResponseCode;

                        // Responses from the server (code and message)
                        serverResponseCode = conn.getResponseCode();
                        String serverResponseMessage = conn
                                .getResponseMessage();

                        if (serverResponseCode == 200) {

                            // messageText.setText(msg);
                            //Toast.makeText(ctx, "File Upload Complete.",
                            //      Toast.LENGTH_SHORT).show();

                            // recursiveDelete(mDirectory1);

                        }

                        // close the streams //
                        fileInputStream.close();
                        dos.flush();
                        dos.close();

                    } catch (Exception e) {

                        // dialog.dismiss();
                        e.printStackTrace();

                    }
                    // dialog.dismiss();

                } // End else block


            } catch (Exception ex) {
                // dialog.dismiss();

                ex.printStackTrace();
            }
            return "Executed";
        }

    }
}
