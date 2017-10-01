package sfllhkhan95.versign.view.activity;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.net.MalformedURLException;

import sfllhkhan95.android.rest.HttpRequest;
import sfllhkhan95.android.rest.ResponseHandler;
import sfllhkhan95.versign.R;
import sfllhkhan95.versign.model.dao.StaffDao;
import sfllhkhan95.versign.model.entity.SessionData;
import sfllhkhan95.versign.model.entity.Staff;
import sfllhkhan95.versign.util.HashGenerator;

public class LoginActivity extends AppCompatActivity {

    private EditText username;
    private EditText password;
    private ViewGroup rootView;
    private Button loginButton;

    private String credentialsError;
    private String signInFailure;
    private String signInSuccess;

    private StaffDao staffDao;

    private SessionData sessionData;

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        sessionData = SessionData.getInstance(this);

        username = (EditText) findViewById(R.id.username);
        password = (EditText) findViewById(R.id.password);
        rootView = (ViewGroup) findViewById(R.id.activity_login);
        loginButton = (Button) findViewById(R.id.loginButton);

        credentialsError = getString(R.string.credentialsError);
        signInFailure = getString(R.string.signInFailure);
        signInSuccess = getString(R.string.signInSuccess);

        try {
            staffDao = new StaffDao();
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }

        LoginController loginController = new LoginController(this);
        loginButton.setOnClickListener(loginController);
    }

    public String getUsername() {
        return username.getText().toString();
    }

    public String getPassword() {
        return password.getText().toString();
    }

    public ViewGroup getRootView() {
        return rootView;
    }

    public void signInSuccess() {
        Toast.makeText(this, signInSuccess, Toast.LENGTH_SHORT).show();

        Intent launchCameraActivity = new Intent(LoginActivity.this, CameraActivity.class);
        startActivity(launchCameraActivity);
    }

    public void signInFailure() {
        Toast.makeText(this, signInFailure, Toast.LENGTH_SHORT).show();
    }

    public void credentialsError() {
        Toast.makeText(this, credentialsError, Toast.LENGTH_SHORT).show();
    }

    private class LoginController implements View.OnClickListener, ResponseHandler<Staff> {

        private final LoginActivity loginActivity;

        LoginController(LoginActivity loginActivity) {
            this.loginActivity = loginActivity;
        }

        @Override
        public void onClick(View v) {
            String u = loginActivity.getUsername();
            String p = loginActivity.getPassword();

            if (isValid(u) && isValid(p)) {
                HttpRequest<Staff> request = staffDao.getFetchRequest(
                        loginActivity.getUsername(),
                        HashGenerator.md5(loginActivity.getPassword())
                );
                request.showStatus(loginActivity.getRootView());
                request.sendRequest(this);
            } else {
                loginActivity.credentialsError();
            }
        }

        @Override
        public void onResponseReceived(@Nullable Staff staff) {
            if (staff != null && !staff.isAdmin()) {
                sessionData.createSession(staff);
                loginActivity.signInSuccess();
            } else {
                loginActivity.signInFailure();
            }
        }

        private boolean isValid(String string) {
            return string != null && !string.trim().equals("");
        }
    }

}
