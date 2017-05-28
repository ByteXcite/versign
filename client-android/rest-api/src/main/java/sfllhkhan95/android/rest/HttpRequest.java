package sfllhkhan95.android.rest;


import android.os.AsyncTask;
import android.support.annotation.Nullable;
import android.view.LayoutInflater;
import android.view.ViewGroup;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import org.jetbrains.annotations.Contract;
import org.jetbrains.annotations.NotNull;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;

import java.io.IOException;

public class HttpRequest<Entity> extends AsyncTask<Void, Void, Entity> {
    private final HttpServer httpServer;
    private final String targetUrl;
    private final Class<Entity> dataType;

    private ResponseHandler<Entity> responseHandler;
    private String payload;
    private ViewGroup statusContainer;

    public HttpRequest(@NotNull HttpServer httpServer, String targetUrl, @NotNull Class<Entity> type) {
        this.httpServer = httpServer;
        this.targetUrl = targetUrl;
        this.dataType = type;
    }

    public HttpRequest<Entity> setPayload(@NotNull Object payload) {
        try {
            ObjectMapper mapper = new MappingJackson2HttpMessageConverter().getObjectMapper();
            this.payload = mapper.writeValueAsString(payload);

            this.payload = this.payload
                    .replace("%", "%25")
                    .replace("=", "3D")
                    .replace(" ", "%20")
                    .replace("\n", "%0A")
                    .replace("+", "%2B")
                    .replace("-", "%2D")
                    .replace("#", "%23")
                    .replace("&", "%26");
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }
        return this;
    }

    public HttpRequest<Entity> showStatus(@NotNull LayoutInflater inflater, @NotNull ViewGroup parent) {
        this.statusContainer = parent;
        inflater.inflate(R.layout.status, parent, true);
        return this;
    }

    public HttpRequest<Entity> setResponseHandler(ResponseHandler<Entity> responseHandler) {
        this.responseHandler = responseHandler;
        return this;
    }

    public void sendRequest() {
        this.execute();
    }

    @Nullable
    @Override
    protected final Entity doInBackground(Void... params) {
        Entity entity = null;
        try {
            entity = (Entity) httpServer.getObject(buildUrl(), this.dataType);
        } catch (IOException ignored) {

        }

        return entity;
    }

    @Override
    protected final void onPostExecute(@Nullable Entity entity) {
        try {
            statusContainer.removeView(statusContainer.getChildAt(statusContainer.getChildCount() - 1));
        } catch (NullPointerException ignored) {

        } finally {
            if (responseHandler != null) {
                responseHandler.onResponseReceived(entity);
            }
        }
    }

    @Contract(pure = true)
    private String buildUrl() {
        if (this.payload == null) {
            return this.targetUrl;
        } else {
            return this.targetUrl + "?payload=" + this.payload;
        }
    }

}