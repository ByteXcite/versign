package sfllhkhan95.versign.app;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.Toast;

import sfllhkhan95.versign.R;
import sfllhkhan95.versign.bo.LoginController;
import sfllhkhan95.versign.entity.Staff;

public class LoginActivity extends AppCompatActivity {

    private EditText username;
    private EditText password;
    private ViewGroup rootView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        rootView = (ViewGroup) findViewById(R.id.activity_login);
        username = (EditText) findViewById(R.id.username);
        password = (EditText) findViewById(R.id.password);

        findViewById(R.id.loginButton).setOnClickListener(new LoginController(this));
    }

    public String getUsername() {
        return username.getText().toString();
    }

    public String getPassword() {
        return password.getText().toString();
    }

    public void loginSuccess(Staff staff) {
        Toast.makeText(this, "Hello, " + staff.getFirstName(), Toast.LENGTH_SHORT).show();
    }

    public void loginFailure() {
        Toast.makeText(this, "Invalid username/password combination.", Toast.LENGTH_SHORT).show();
    }

    public ViewGroup getRootView() {
        return rootView;
    }

    public void connectionError() {
        Toast.makeText(this, "Check your network connection.", Toast.LENGTH_SHORT).show();
    }

    public void invalidArguments() {
        Toast.makeText(this, "Username/password cannot be empty.", Toast.LENGTH_SHORT).show();
    }
}
