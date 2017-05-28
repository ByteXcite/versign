package sfllhkhan95.versign.util;

import android.util.Log;

import java.net.MalformedURLException;

import sfllhkhan95.android.rest.HttpServer;

/**
 *
 */
public class WebServer {
    private static final String SERVER_ADDRESS = "http://10.0.3.2/app/";
    private static WebServer ourInstance;
    private final HttpServer httpServer;

    private WebServer() throws MalformedURLException {
        httpServer = new HttpServer(SERVER_ADDRESS);
    }

    public static WebServer getInstance() {
        if (ourInstance == null) {
            try {
                ourInstance = new WebServer();
            } catch (MalformedURLException ex) {
                Log.e("WebServer", "Cannot establish connection with " + SERVER_ADDRESS);
                return null;
            }
        }
        return ourInstance;
    }

    public HttpServer getHttpServer() {
        return httpServer;
    }
}
