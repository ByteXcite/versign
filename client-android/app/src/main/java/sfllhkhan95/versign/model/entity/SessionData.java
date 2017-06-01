package sfllhkhan95.versign.model.entity;

import com.google.inject.Singleton;


@Singleton
public class SessionData {
    private Staff currentUser;

    public Staff getCurrentUser() {
        return currentUser;
    }

    public void setCurrentUser(Staff currentUser) {
        this.currentUser = currentUser;
    }
}