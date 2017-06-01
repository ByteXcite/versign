package sfllhkhan95.versign.model.entity;

import org.junit.Assert;
import org.junit.Test;

/**
 * Unit tests of Customer entity class.
 *
 * @author saifkhichi96
 * @version 1.0
 */
public class CustomerTest {
    @Test(expected = IllegalArgumentException.class)
    public void setNIC() {
        Customer customer = new Customer();

        customer.setNIC("  1234567890987  ");
        Assert.assertEquals("1234567890987", customer.getNIC());

        customer.setNIC("12345");
    }

    @Test(expected = IllegalArgumentException.class)
    public void setFirstName() {
        Customer customer = new Customer();

        customer.setFirstName("Albus");
        Assert.assertEquals("Albus", customer.getFirstName());

        customer.setFirstName("    ");

    }

    @Test(expected = IllegalArgumentException.class)
    public void setLastName() {
        Customer customer = new Customer();

        customer.setLastName("Dumbledore");
        Assert.assertEquals("Dumbledore", customer.getLastName());

        customer.setLastName("    ");

    }

}