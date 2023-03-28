
from ls_report_agent import ReportAgent, BearerToken
from lxml import etree
import pandas
import pytest
import getpass


def test_xml_2_table():
    xml = """
        <report>
            <row>
                <id>1234</id>
                <name>Testy Test</name>
            </row>
        </report>
    """
    agent = ReportAgent(BearerToken("exampletoken"), "https://fakeurl?load=123&apikey=1234")
    xml = etree.XML(xml)
    
    tbl = agent.xml_2_table(xml)
    assert isinstance(tbl, pandas.DataFrame)
    assert tbl.loc[0]['name'] == 'Testy Test'



