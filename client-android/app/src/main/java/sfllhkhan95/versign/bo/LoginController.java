package sfllhkhan95.versign.bo;

import android.support.annotation.Nullable;
import android.view.View;

import java.math.BigInteger;
import java.nio.charset.Charset;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

import sfllhkhan95.android.rest.ResponseHandler;
import sfllhkhan95.versign.app.LoginActivity;
import sfllhkhan95.versign.dao.StaffDao;
import sfllhkhan95.versign.entity.Staff;

/**
 * Controller class for LoginActivity view.
 */
public class LoginController extends Controller implements ResponseHandler<Staff> {
    private final StaffDao dao;

    public LoginController(LoginActivity activity) throws RuntimeException {
        super(activity);
        try {
            dao = new StaffDao();
        } catch (NullPointerException ex) {
            activity.connectionError();
            throw new RuntimeException();
        }
    }

    @Override
    public void onClick(View v) {
        LoginActivity ctx = (LoginActivity) activity;
        String u = ctx.getUsername();
        String p = ctx.getPassword();

        if (isValid(u) && isValid(p)) {
            dao.getFetchRequest(ctx.getUsername(), md5(ctx.getPassword()), this)
                    .showStatus(ctx.getLayoutInflater(), ctx.getRootView())
                    .sendRequest();
        } else {
            ctx.invalidArguments();
        }
    }

    @Override
    public void onResponseReceived(@Nullable Staff staff) {
        LoginActivity ctx = (LoginActivity) activity;
        if (staff != null /*&& !staff.isAdmin()*/) {    // Uncomment to make logins by non-admins only
            ctx.loginSuccess(staff);
        } else {
            ctx.loginFailure();
        }
    }

    private static String md5(String s) {
        MessageDigest digest;
        try {
            digest = MessageDigest.getInstance("MD5");
            digest.update(s.getBytes(Charset.forName("US-ASCII")), 0, s.length());
            byte[] magnitude = digest.digest();
            BigInteger bi = new BigInteger(1, magnitude);
            return String.format("%0" + (magnitude.length << 1) + "x", bi);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
        return "";
    }

    private boolean isValid(String string) {
        return string != null && !string.trim().equals("");
    }
}
