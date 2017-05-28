package sfllhkhan95.android.rest;

import android.support.annotation.Nullable;

/**
 * ResponseHandler defines an interface for handling responses received from the remote web server.
 *
 * @author MuhammadSaifullah
 * @version 1.0
 */
public interface ResponseHandler<Entity> {
    void onResponseReceived(@Nullable Entity entity);
}