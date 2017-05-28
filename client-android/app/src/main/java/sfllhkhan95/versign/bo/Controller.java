package sfllhkhan95.versign.bo;

import android.app.Activity;
import android.view.View;

/**
 *
 */
public abstract class Controller implements View.OnClickListener {
    protected final Activity activity;

    public Controller(Activity activity) {
        this.activity = activity;
    }
}
