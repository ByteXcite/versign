package sfllhkhan95.versign.dao;

import sfllhkhan95.android.rest.HttpRequest;
import sfllhkhan95.android.rest.HttpServer;
import sfllhkhan95.android.rest.ResponseHandler;
import sfllhkhan95.versign.entity.Credentials;
import sfllhkhan95.versign.entity.Staff;
import sfllhkhan95.versign.util.WebServer;

/**
 * StaffDao is a data-access class for Staff entity which allows retrieval
 * of Staff objects from the web server.
 *
 * @author saifkhichi96
 * @version 1.0
 */
public class StaffDao {

    private final HttpServer server;

    public StaffDao() throws NullPointerException {
        server = WebServer.getInstance().getHttpServer();
    }

    public HttpRequest<Staff> getFetchRequest(String username, String password, ResponseHandler<Staff> handler) {
        HttpRequest<Staff> request = new HttpRequest<>(
                server,
                "LoginController.php",
                Staff.class
        );
        request.setPayload(new Credentials(username, password));
        request.setResponseHandler(handler);
        return request;
    }

}