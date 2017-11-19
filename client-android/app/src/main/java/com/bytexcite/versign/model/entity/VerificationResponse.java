package com.bytexcite.versign.model.entity;

/**
 * VerificationResponse is received from the server in response to a VerificationRequest.
 * It contains results of verification and details of customer to whom the questioned
 * signture belonged.
 *
 * @author saifkhichi96
 * @version 1.0
 */
public class VerificationResponse {

    private boolean isGenuine;
    private Customer belongsTo;

    public boolean isGenuine() {
        return isGenuine;
    }

    public void setGenuine(boolean genuine) {
        isGenuine = genuine;
    }

    public Customer getBelongsTo() {
        return belongsTo;
    }

    public void setBelongsTo(Customer belongsTo) {
        this.belongsTo = belongsTo;
    }
}
