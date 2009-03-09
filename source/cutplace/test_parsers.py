"""Tests for parsers"""
import logging
import parsers
import StringIO
import types
import unittest

_log = logging.getLogger("cutplace.parsers")

class DelimiterParserTest(unittest.TestCase):
    """TestCase for DelimiterParser."""
    
    def _createDefaultDialect(self):
        result = parsers.DelimitedDialect()
        result.lineDelimiter = parsers.LF
        result.itemDelimiter = ","
        result.quoteChar = "\""
        return result

    def _assertItemsEqual(self, expectedItems, readable, dialect=None):
        """Simply parse all items of readable using dialect and assert that the number of items read matches expectedItemCount."""
        assert expectedItems is not None
        assert readable is not None
        
        if isinstance(readable, types.StringTypes):
            actualReadable = StringIO.StringIO(readable)
        else:
            actualReadable = readable
        if dialect is None:
            actualDialect = self._createDefaultDialect()
        else:
            actualDialect = dialect
        parser = parsers.DelimitedParser(actualReadable, actualDialect)
        rows = []
        columns = []
        while not parser.atEndOfFile:
            _log.debug("eof=" + str(parser.atEndOfFile) + ",eol=" + str(parser.atEndOfLine) + ", item=" + str(parser.item))
            if parser.item is not None:
                columns.append(parser.item)
            if parser.atEndOfLine:
                rows.append(columns)
                columns = []
            parser.advance()
        self.assertEqual(rows, expectedItems)
        
    def testSingleCharCsv(self):
        self._assertItemsEqual([["x"]], "x")

    def testSingleLineCsv(self):
        self._assertItemsEqual([["hugo", "was", "here"]], "hugo,was,here")

    def testTwoLineCsv(self):
        self._assertItemsEqual([["a"], ["b", "c"]], "a" + parsers.LF + "b,c")
        self._assertItemsEqual([["hugo", "was"], ["here", "again"]], "hugo,was" + parsers.LF + "here,again")

    def testMixedQuotedLineCsv(self):
        self._assertItemsEqual([["hugo", "was", "here"]], "hugo,\"was\",here")
        
    def testEmptyCsv(self):
        self._assertItemsEqual([], "")

    def testEmptyLineWithLfCsv(self):
        self._assertItemsEqual([[""]], parsers.LF)
    
    def _testEmptyLineWithCrCsv(self):
        self._assertItemsEqual([[""]], parsers.CR)
    
    def _testEmptyLineWithCrLfCsv(self):
        self._assertItemsEqual([[""]], parsers.CRLF)
    
if __name__ == '__main__':
    logging.basicConfig()
    _log.setLevel(logging.INFO)
    unittest.main()
