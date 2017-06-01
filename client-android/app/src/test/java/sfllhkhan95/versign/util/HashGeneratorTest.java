package sfllhkhan95.versign.util;

import org.junit.Assert;
import org.junit.Test;

/**
 * Unit tests of HashGenerator utility.
 *
 * @author saifkhichi96
 * @version 1.0
 */
public class HashGeneratorTest {
    @Test
    public void md5() throws Exception {
        Assert.assertEquals("5f4dcc3b5aa765d61d8327deb882cf99", HashGenerator.md5("password"));
    }

}