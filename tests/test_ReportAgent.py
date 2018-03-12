
from ls_report_agent import ReportAgent
from lxml import etree
import pandas
import pytest
from ruamel.yaml import YAML
import getpass
import keyring
import keyring_jeepney

@pytest.fixture(scope="module")
def secrets():
    yaml = YAML(typ='safe')

    # get some secrets from a local yaml file
    secrets = yaml.load(open('secrets.yaml', 'r'))

    # or get some secrets from the local keyring.
    # keyring.set_keyring(keyring_jeepney.Keyring())
    # secrets['API_Username'] = keyring.get_password('demo.legalserver', 'api_username')
    # secrets['API_User_Pass'] = keyring.get_password('demo.legalserver', 'api_pass')
    # secrets['Report_Key'] = keyring.get_password('demo.legalserver', 'Test Report Key')

    #Or get secrets from the command line
    try:
        secrets['reportURL']
    except:
        secrets['reportURL'] = getpass.getpass('REPORT URL: ')

    try:
        secrets['API_Username']
    except:
        secrets['API_Username'] = getpass.getpass("API USER: ")

    try:
        secrets['API_User_Pass']
    except:
        secrets['API_User_Pass'] = getpass.getpass("API USER PASS: ")

    try:
        secrets['Report_Key']
    except:
        secrets['Report_Key'] = getpass.getpass("Report Key: ")

    return(secrets)

class TestReportAgent(object):


    def test_init(self, secrets):
        agent = ReportAgent(secrets['API_Username'],
                            secrets['API_User_Pass'],
                            secrets['reportURL'],
                            secrets['Report_Key'])
        assert isinstance(agent, ReportAgent)

    def test_get_raw_xml(self, secrets):
        # When running this test, use py.test -s to enable stdin
        agent = ReportAgent(secrets['API_Username'],
                            secrets['API_User_Pass'],
                            secrets['reportURL'],
                            secrets['Report_Key'])
        raw = agent.get_raw_xml()
        pytest.set_trace()
        assert raw.tag == 'report'

    def test_xml_2_table(self, secrets):
        xml = etree.parse("data/example.xml")
        agent = ReportAgent(secrets['API_Username'],
                            secrets['API_User_Pass'],
                            secrets['reportURL'],
                            secrets['Report_Key'])
        pd_table = agent.xml_2_table(xml)
        assert isinstance(pd_table, pandas.DataFrame)

    def test_get_report_as_pandasDataFrame(self, secrets):
        agent = ReportAgent(secrets['API_Username'],
                            secrets['API_User_Pass'],
                            secrets['reportURL'],
                            secrets['Report_Key'],
                            col_mapper = {
                                "zip": "Zip Code",
                                "identification_number":"Case Matter/Case ID#",
                                "first": "Client First Name",
                                "last": "Client Last Name",
                                "dob":"Client Date of Birt",
                                "matter_builtin_lookup_problem_code_legal_problem_code_expn": "Legal Problem Code"
                            })
        pd_table = agent.get_report('pandas')
        assert isinstance(pd_table, pandas.DataFrame)
