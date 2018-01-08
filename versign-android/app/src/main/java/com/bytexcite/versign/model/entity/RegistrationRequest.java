package com.bytexcite.versign.model.entity;


import java.io.Serializable;

/**
 * RegistrationRequest is sent to the server with a customer's identifier and reference signatures.
 *
 * @author saifkhichi96
 * @version 1.0
 */
public class RegistrationRequest implements Serializable {

    private final String customerID;
    private final SignatureImage refSignA;
    private final SignatureImage refSignB;
    private final SignatureImage refSignC;
    private final SignatureImage refSignD;

    public RegistrationRequest(String customerID, SignatureImage refSignA, SignatureImage refSignB,
                               SignatureImage refSignC, SignatureImage refSignD) {
        this.customerID = customerID;
        this.refSignA = refSignA;
        this.refSignB = refSignB;
        this.refSignC = refSignC;
        this.refSignD = refSignD;
    }

    public String getCustomerID() {
        return customerID;
    }

    public SignatureImage getRefSignA() {
        return refSignA;
    }

    public SignatureImage getRefSignB() {
        return refSignB;
    }

    public SignatureImage getRefSignC() {
        return refSignC;
    }

    public SignatureImage getRefSignD() {
        return refSignD;
    }

}