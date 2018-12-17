package com.bytexcite.verisign.db;

import com.bytexcite.verisign.model.entity.Customer;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by saifkhichi96 on 13/02/2018.
 */

public class CustomerDatabase {

    private static CustomerDatabase ourInstance = new CustomerDatabase();

    private final DatabaseReference remoteDb = FirebaseDatabase.getInstance().getReference().child("users");
    private final Map<String, CustomerInfo> customerInfoMap = new HashMap<>();

    private CustomerDatabase() {
        remoteDb.setValue("123");
    }

    public static CustomerDatabase getInstance() {
        return ourInstance;
    }

    public void addCustomer(Customer customer, List<List<Integer>> refSigns) {
        CustomerInfo info = new CustomerInfo();
        info.customer = customer;
        info.refSigns = refSigns;

        customerInfoMap.put(customer.getId(), info);
        updateRemote();
    }

    public void asyncGetCustomerInfo(String customerId, final CustomerInfoCallback callback) {
        remoteDb.child(customerId).addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                callback.onCustomerInfoReceived(dataSnapshot.getValue(CustomerInfo.class));
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {

            }
        });
    }

    private void updateRemote() {
        remoteDb.setValue(customerInfoMap);
    }

}