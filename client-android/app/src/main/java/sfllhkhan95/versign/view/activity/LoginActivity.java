package sfllhkhan95.versign.view.activity;

import android.content.Intent;
import android.support.annotation.Nullable;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.google.inject.Inject;

import roboguice.activity.RoboActivity;
import roboguice.context.event.OnCreateEvent;
import roboguice.event.Observes;
import roboguice.inject.ContentView;
import roboguice.inject.InjectResource;
import roboguice.inject.InjectView;
import sfllhkhan95.android.rest.HttpRequest;
import sfllhkhan95.android.rest.ResponseHandler;
import sfllhkhan95.versign.R;
import sfllhkhan95.versign.model.dao.StaffDao;
import sfllhkhan95.versign.model.entity.SessionData;
import sfllhkhan95.versign.model.entity.Staff;
import sfllhkhan95.versign.util.HashGenerator;

@ContentView(R.layout.activity_login)
public class LoginActivity extends RoboActivity {

    @InjectView(R.id.username)
    private EditText username;

    @InjectView(R.id.password)
    private EditText password;

    @InjectView(R.id.activity_login)
    private ViewGroup rootView;

    @InjectView(R.id.loginButton)
    private Button loginButton;

    @InjectResource(R.string.credentialsError)
    private String credentialsError;

    @InjectResource(R.string.signInFailure)
    private String signInFailure;

    @InjectResource(R.string.signInSuccess)
    private String signInSuccess;

    @Inject
    private StaffDao staffDao;

    private SessionData sessionData;

    public void initialize(@Observes OnCreateEvent e) {
        sessionData = new SessionData(this);

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
