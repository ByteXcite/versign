package sfllhkhan95.versign.model.entity;

import org.junit.Test;

/**
 * Unit tests of Credentials entity.
 */
public class CredentialsTest {

    @Test
    public void testCanCreateInstanceWithValidArguments() {
        new Credentials("username", "5f4dcc3b5aa765d61d8327deb882cf99");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testCannotCreateInstanceWithNonHashedPassword() {
        new Credentials("username", "password");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testCannotCreateInstanceWithEmptyPassword() {
        new Credentials("username", "");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testCannotCreateInstanceWithEmptyUsername() {
        new Credentials("", "5f4dcc3b5aa765d61d8327deb882cf99");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testCannotCreateInstanceWithWhitespaceUsername() {
        new Credentials(" \t\n ", "5f4dcc3b5aa765d61d8327deb882cf99");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testCannotCreateInstanceWithWhitespacePassword() {
        new Credentials("username", " \t\n ");
    }

}