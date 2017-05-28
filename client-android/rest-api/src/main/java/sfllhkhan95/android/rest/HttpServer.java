package sfllhkhan95.android.rest;

import com.fasterxml.jackson.databind.ObjectMapper;

import org.jetbrains.annotations.NotNull;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Scanner;

public class HttpServer {

    private final String address;

    public HttpServer(@NotNull String address) throws MalformedURLException {
        if (!address.endsWith("/")) {
            this.address = address + "/";
        } else {
            this.address = address;
        }

        new URL(address);
        if (address.equals("/")) {
            throw new MalformedURLException();
        }

    }

    /**
     * Returns content of the web document.
     *
     * @return content of the web document
     */
    synchronized Object getObject(String file, Class<?> dataType) throws IOException {
        // Establish a new HTTP connection with the remote web server
        HttpURLConnection connection = connect(this.address + file);

        // Read the remote file and create an input stream from the received data
        InputStream inputStream = new BufferedInputStream(connection.getInputStream());

        // Read the whole content of the remote file and save it locally
        Scanner s = new Scanner(inputStream).useDelimiter("\\A");
        String content = s.hasNext() ? s.next() : "";

        // Terminate the HTTP connection with the remote web server
        connection.disconnect();

        ObjectMapper mapper = new MappingJackson2HttpMessageConverter().getObjectMapper();
        Object o = mapper.readValue(content, dataType);
        return o;
    }

    /**
     * Establishes an HTTP connection with the remote web server and requests the a remote web
     * document at the given path.
     *
     * @return an instance of HttpURLConnection established with the requested web document
     * @throws IOException thrown if there is an error communicating with the web server
     */
    private HttpURLConnection connect(String file) throws IOException {
        // Create a URL
        URL url = new URL(file);

        // Connect to web page at given url and return connection
        return (HttpURLConnection) url.openConnection();
    }

}