package com.bytexcite.verisign.db;

import com.bytexcite.verisign.model.entity.Customer;

import java.io.Serializable;
import java.util.List;

public class CustomerInfo implements Serializable {

    public Customer customer;
    public List<List<Integer>> refSigns;

}