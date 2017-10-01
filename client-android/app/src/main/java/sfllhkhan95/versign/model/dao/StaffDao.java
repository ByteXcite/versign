package sfllhkhan95.versign.model.dao;

import java.net.MalformedURLException;

import sfllhkhan95.android.rest.HttpRequest;
import sfllhkhan95.versign.model.entity.Credentials;
import sfllhkhan95.versign.model.entity.Staff;
import sfllhkhan95.versign.util.WebServer;

/**
 * StaffDao is a data-access class for Staff entity which allows retrieval
 * of Staff objects from the web server.
 *
 * @author saifkhichi96
 * @version 1.0
 */
public class StaffDao {

    private WebServer server = new WebServer();

    public StaffDao() throws MalformedURLException {
    }

    public HttpRequest<Staff> getFetchRequest(String username, String password) {
        HttpRequest<Staff> request = new HttpRequest<>(
                server,
                "LoginController.php",
                Staff.class
        );
        request.setPayload(new Credentials(username, password));
        return request;
    }

}