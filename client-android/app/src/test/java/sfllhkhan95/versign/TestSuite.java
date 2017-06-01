package sfllhkhan95.versign;

import org.junit.runner.RunWith;
import org.junit.runners.Suite;

import sfllhkhan95.versign.model.entity.CredentialsTest;
import sfllhkhan95.versign.model.entity.CustomerTest;
import sfllhkhan95.versign.model.entity.StaffTest;

/**
 * TestSuite for local unit tests which execute on the development machine.
 *
 * @author saifkhichi96
 * @version 1.0
 */
@RunWith(Suite.class)
@Suite.SuiteClasses({
        CredentialsTest.class,
        StaffTest.class,
        CustomerTest.class
})
public class TestSuite {

}