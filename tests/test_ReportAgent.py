
from ls_report_agent import ReportAgent
from lxml import etree
import pandas
import pytest
from ruamel.yaml import YAML



@pytest.fixture
def secrets():
    yaml = YAML(typ='safe')
    secrets = yaml.load(open('secrets.yaml', 'r'))
    return(secrets)

class TestReportAgent(object):


    def test_init(self):
        agent = ReportAgent("fakeurl")
        assert isinstance(agent, ReportAgent)

    def test_get_raw_xml(self, secrets):
        # When running this test, use py.test -s to enable stdin
        agent = ReportAgent(secrets['reportURL'])
        raw = agent.get_raw_xml()
        assert raw.tag == 'report'

    def test_xml_2_table(self):
        xml = etree.parse("data/example.xml")
        agent = ReportAgent('fakeurl')
        pd_table = agent.xml_2_table(xml)
        assert isinstance(pd_table, pandas.DataFrame)

    def test_get_report_as_pandasDataFrame(self, secrets):
        agent = ReportAgent(secrets['reportURL'])
        pytest.set_trace()
        pd_table = agent.get_report('pandas')
        assert isinstance(pd_table, pandas.DataFrame)
