#
# Test DAF support for warning data
#
#     SOFTWARE HISTORY
#
#    Date            Ticket#       Engineer       Description
#    ------------    ----------    -----------    --------------------------
#    01/19/16        4795          mapeters       Initial Creation.
#    04/11/16        5548          tgurney        Cleanup
#    04/18/16        5548          tgurney        More cleanup
#    04/26/16        5587          tgurney        Add identifier values tests
#    06/08/16        5574          tgurney        Add advanced query tests
#    06/10/16        5548          tgurney        Clean up references to name
#                                                 of data type
#    06/13/16        5574          tgurney        Fix checks for None
#    06/21/16        5548          tgurney        Skip tests that cause errors
#    06/30/16        5725          tgurney        Add test for NOT IN
#    12/12/16        5981          tgurney        Improve test performance
#
#

from __future__ import print_function
from awips.dataaccess import DataAccessLayer as DAL
from dynamicserialize.dstypes.com.raytheon.uf.common.dataquery.requests import RequestConstraint

from awips.test.dafTests import baseDafTestCase
import unittest


class WarningTestCase(baseDafTestCase.DafTestCase):
    """Test DAF support for warning data"""

    datatype = "warning"

    def _getLocationNames(self):
        req = DAL.newDataRequest()
        req.setDatatype(self.datatype)
        return DAL.getAvailableLocationNames(req)

    def _getAllRecords(self):
        req = DAL.newDataRequest()
        req.setDatatype(self.datatype)
        req.setParameters('id')
        return DAL.getGeometryData(req)

    def testGetAvailableParameters(self):
        req = DAL.newDataRequest(self.datatype)
        self.runParametersTest(req)

    def testGetAvailableLocations(self):
        req = DAL.newDataRequest(self.datatype)
        self.runLocationsTest(req)

    def testGetAvailableTimes(self):
        req = DAL.newDataRequest(self.datatype)
        req.setParameters("etn", "wmoid")
        self.runTimesTest(req)

    def testGetGeometryData(self):
        req = DAL.newDataRequest(self.datatype)
        req.setParameters("etn", "wmoid")
        self.runGeometryDataTest(req)

    def testFilterOnLocationName(self):
        allLocationNames = self._getLocationNames()
        if len(allLocationNames) == 0:
            errmsg = "No {0} data exists on {1}. Try again with {0} data."
            raise unittest.SkipTest(errmsg.format(self.datatype, DAL.THRIFT_HOST))
        testCount = 3  # number of different location names to test
        for locationName in allLocationNames[:testCount]:
            req = DAL.newDataRequest()
            req.setDatatype(self.datatype)
            req.setParameters('id')
            req.setLocationNames(locationName)
            geomData = DAL.getGeometryData(req)
            for geom in geomData:
                self.assertEqual(geom.getLocationName(), locationName)

    def testFilterOnNonexistentLocationReturnsEmpty(self):
        req = DAL.newDataRequest()
        req.setDatatype(self.datatype)
        req.setParameters('id')
        req.setLocationNames('ZZZZ')
        self.assertEqual(len(DAL.getGeometryData(req)), 0)

    def testFilterOnInvalidLocationThrowsIncompatibleRequestException(self):
        req = DAL.newDataRequest()
        req.setDatatype(self.datatype)
        req.setParameters('id')
        req.setLocationNames(') and 0=1')
        with self.assertRaises(Exception) as cm:
            DAL.getGeometryData(req)
        self.assertIn('IncompatibleRequestException', str(cm.exception))

    def testGetColumnIdentifierValues(self):
        self.runGetIdValuesTest(['act'])

    @unittest.skip('avoid EDEX error')
    def testGetInvalidIdentifierValuesThrowsException(self):
        self.runInvalidIdValuesTest()

    @unittest.skip('avoid EDEX error')
    def testGetNonexistentIdentifierValuesThrowsException(self):
        self.runNonexistentIdValuesTest()

    def _runConstraintTest(self, key, operator, value):
        req = DAL.newDataRequest(self.datatype)
        constraint = RequestConstraint.new(operator, value)
        req.addIdentifier(key, constraint)
        req.setParameters("etn", "wmoid", "sig")
        return self.runGeometryDataTest(req)

    def testGetDataWithEqualsString(self):
        geometryData = self._runConstraintTest('sig', '=', 'Y')
        for record in geometryData:
            self.assertEqual(record.getString('sig'), 'Y')

    def testGetDataWithEqualsInt(self):
        geometryData = self._runConstraintTest('etn', '=', 1000)
        for record in geometryData:
            self.assertEqual(record.getString('etn'), '1000')

    def testGetDataWithEqualsLong(self):
        geometryData = self._runConstraintTest('etn', '=', 1000)
        for record in geometryData:
            self.assertEqual(record.getString('etn'), '1000')

    def testGetDataWithEqualsFloat(self):
        geometryData = self._runConstraintTest('etn', '=', 1.0)
        for record in geometryData:
            self.assertEqual(round(float(record.getString('etn')), 1), 1.0)

    def testGetDataWithEqualsNone(self):
        geometryData = self._runConstraintTest('sig', '=', None)
        for record in geometryData:
            self.assertEqual(record.getType('sig'), 'NULL')

    def testGetDataWithNotEquals(self):
        geometryData = self._runConstraintTest('sig', '!=', 'Y')
        for record in geometryData:
            self.assertNotEqual(record.getString('sig'), 'Y')

    def testGetDataWithNotEqualsNone(self):
        geometryData = self._runConstraintTest('sig', '!=', None)
        for record in geometryData:
            self.assertNotEqual(record.getType('sig'), 'NULL')

    def testGetDataWithGreaterThan(self):
        geometryData = self._runConstraintTest('sig', '>', 'Y')
        for record in geometryData:
            self.assertGreater(record.getString('sig'), 'Y')

    def testGetDataWithLessThan(self):
        geometryData = self._runConstraintTest('sig', '<', 'Y')
        for record in geometryData:
            self.assertLess(record.getString('sig'), 'Y')

    def testGetDataWithGreaterThanEquals(self):
        geometryData = self._runConstraintTest('sig', '>=', 'Y')
        for record in geometryData:
            self.assertGreaterEqual(record.getString('sig'), 'Y')

    def testGetDataWithLessThanEquals(self):
        geometryData = self._runConstraintTest('sig', '<=', 'Y')
        for record in geometryData:
            self.assertLessEqual(record.getString('sig'), 'Y')

    def testGetDataWithInTuple(self):
        collection = ('Y', 'A')
        geometryData = self._runConstraintTest('sig', 'in', collection)
        for record in geometryData:
            self.assertIn(record.getString('sig'), collection)

    def testGetDataWithInList(self):
        collection = ['Y', 'A']
        geometryData = self._runConstraintTest('sig', 'in', collection)
        for record in geometryData:
            self.assertIn(record.getString('sig'), collection)

    def testGetDataWithInGenerator(self):
        collection = ('Y', 'A')
        generator = (item for item in collection)
        geometryData = self._runConstraintTest('sig', 'in', generator)
        for record in geometryData:
            self.assertIn(record.getString('sig'), collection)

    def testGetDataWithNotInList(self):
        collection = ['Y', 'W']
        geometryData = self._runConstraintTest('sig', 'not in', collection)
        for record in geometryData:
            self.assertNotIn(record.getString('sig'), collection)

    def testGetDataWithInvalidConstraintTypeThrowsException(self):
        with self.assertRaises(ValueError):
            self._runConstraintTest('sig', 'junk', 'Y')

    def testGetDataWithInvalidConstraintValueThrowsException(self):
        with self.assertRaises(TypeError):
            self._runConstraintTest('sig', '=', {})

    def testGetDataWithEmptyInConstraintThrowsException(self):
        with self.assertRaises(ValueError):
            self._runConstraintTest('sig', 'in', [])

    def testGetDataWithNestedInConstraintThrowsException(self):
        collection = ('Y', 'A', ())
        with self.assertRaises(TypeError):
            self._runConstraintTest('sig', 'in', collection)
