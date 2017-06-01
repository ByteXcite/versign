package sfllhkhan95.versign.model.entity;

import org.junit.Assert;
import org.junit.Test;

/**
 * Unit tests of Staff entity class.
 *
 * @author saifkhichi96
 * @version 1.0
 */
public class StaffTest {
    @Test
    public void testCanCreateFromString() throws Exception {
        String string = "NIC, username, password, firstName, lastName, email, 0";
        Staff staff = Staff.fromString(string);

        Assert.assertEquals("NIC", staff.getNic());
        Assert.assertEquals("username", staff.getUsername());
        Assert.assertEquals("password", staff.getPassword());
        Assert.assertEquals("firstName", staff.getFirstName());
        Assert.assertEquals("lastName", staff.getLastName());
        Assert.assertEquals("email", staff.getEmail());
        Assert.assertFalse(staff.isAdmin());
    }

    @Test
    public void testCanCastToString() throws Exception {
        Staff staff = new Staff();
        staff.setNic("NIC");
        staff.setUsername("username");
        staff.setPassword("password");
        staff.setFirstName("firstName");
        staff.setLastName("lastName");
        staff.setEmail("email");
        staff.setAdmin("1");

        String string = "NIC, username, password, firstName, lastName, email, 1";
        Assert.assertEquals(string, staff.toString());
    }

    @Test
    public void testCanSetAdminWithStrings() {
        Staff staff = new Staff();

        staff.setAdmin("0");
        Assert.assertFalse(staff.isAdmin());

        staff.setAdmin("1");
        Assert.assertTrue(staff.isAdmin());

        staff.setAdmin("100");
        Assert.assertTrue(staff.isAdmin());

        staff.setAdmin("-100");
        Assert.assertTrue(staff.isAdmin());

        staff.setAdmin("true");
        Assert.assertTrue(staff.isAdmin());

        staff.setAdmin("FALSE");
        Assert.assertFalse(staff.isAdmin());
    }

}