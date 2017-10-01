package sfllhkhan95.versign.controller;

import java.net.MalformedURLException;

import sfllhkhan95.android.rest.HttpRequest;
import sfllhkhan95.versign.model.entity.SignatureImage;
import sfllhkhan95.versign.model.entity.VerificationRequest;
import sfllhkhan95.versign.model.entity.VerificationResponse;
import sfllhkhan95.versign.util.WebServer;


/**
 * VerificationController allows sending a VerificationRequest to the web server and receiving
 * an VerificationResponse in response.
 *
 * @author saifkhichi96
 * @version 1.0
 * @see VerificationRequest
 * @see VerificationResponse
 */
public class VerificationController {

    private WebServer server = new WebServer();

    public VerificationController() throws MalformedURLException {
    }

    public HttpRequest<VerificationResponse> getVerificationRequest(
            String customerID, SignatureImage signatureImage)
    {
        HttpRequest<VerificationResponse> request = new HttpRequest<>(
                server,
                "VerificationController.php",
                VerificationResponse.class
        );
        request.setPayload(new VerificationRequest(customerID, signatureImage));
        return request;
    }
}