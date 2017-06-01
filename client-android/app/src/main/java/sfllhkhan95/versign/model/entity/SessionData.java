package sfllhkhan95.versign.model.entity;

import android.app.Activity;
import android.content.Context;
import android.content.SharedPreferences;

import com.google.inject.Singleton;


/**
 * SessionData is a Singleton containing information of active session.
 */
@Singleton
public class SessionData {
    private static final String PREF_NAME = "_versignSession";
    private final SharedPreferences preferences;
    private Staff activeUser;

    public SessionData(Activity context) {
        preferences = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
        String currentUser = preferences.getString("currentUser", null);
        if (currentUser != null) {
            this.activeUser = Staff.fromString(currentUser);
        }
    }

    public void createSession(Staff loggedInStaff) {
        this.activeUser = loggedInStaff;
        preferences.edit()
                .putString("currentUser", loggedInStaff.toString())
                .apply();
    }

    public void destroySession() {
        activeUser = null;
        preferences.edit()
                .putString("currentUser", null)
                .apply();
    }

    public Staff getActiveUser() {
        return activeUser;
    }
}