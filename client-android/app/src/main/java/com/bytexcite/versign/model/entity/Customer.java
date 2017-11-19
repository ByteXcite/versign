package com.bytexcite.versign.model.entity;

import java.io.Serializable;

/**
 * Customer entity represents a customer of the bank.
 *
 * @author saifkhichi96
 * @version 1.0
 */
public class Customer implements Serializable {

    /**
     * NIC number of the bank customer.
     */
    private String NIC;

    /**
     * First name of the bank customer.
     */
    private String firstName;

    /**
     * Last name of the bank custormer.
     */
    private String lastName;

    /**
     * Getter method of NIC.
     *
     * @return NIC number of the bank customer
     */
    public String getNIC() {
        return NIC;
    }

    /**
     * Sets customer's NIC number.
     *
     * @param NIC NIC number of the bank customer
     */
    public void setNIC(String NIC) throws IllegalArgumentException {
        if (NIC.trim().length() != 13)
            throw new IllegalArgumentException();

        this.NIC = NIC.trim();
    }

    /**
     * Gets customer's first name.
     *
     * @return first name of the bank customer
     */
    public String getFirstName() {
        return firstName;
    }

    /**
     * Sets customer's first name.
     *
     * @param firstName first name of the bank customer
     * @throws IllegalArgumentException exception thrown if name is empty string
     */
    public void setFirstName(String firstName) {
        if (firstName.trim().equals(""))
            throw new IllegalArgumentException();

        this.firstName = firstName.trim();
    }

    /**
     * Gets customer's last name.
     *
     * @return last name of the bank customer
     */
    public String getLastName() {
        return lastName;
    }

    /**
     * Sets customers last name.
     *
     * @param lastName last names of the bank customer
     * @throws IllegalArgumentException exception thrown if name is empty string
     */
    public void setLastName(String lastName) throws IllegalArgumentException {
        if (lastName.trim().equals(""))
            throw new IllegalArgumentException();

        this.lastName = lastName.trim();
    }

}
