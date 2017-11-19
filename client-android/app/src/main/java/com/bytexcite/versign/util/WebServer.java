package com.bytexcite.versign.util;

import java.net.MalformedURLException;

import sfllhkhan95.android.rest.HttpServer;


public class WebServer extends HttpServer {
    private static final String SERVER_ADDRESS = "https://versign.azurewebsites.net/app/";

    public WebServer() throws MalformedURLException {
        super(SERVER_ADDRESS);
    }
}