import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse
from lxml import etree
import getpass
import pandas


import pytest

class ReportAgent(object):
    """
    An agent that can download a legal server report.
    """
    def __init__(self, report_url = None):
        if report_url:
            self.report_url = report_url

    def get_raw_xml(self):
        """
        Get the raw xml of a report from LegalServer

        This method uses `getpass` to ask you for the credentials for the report you are downloading.

        Args:
            none.

        Return:
            An `lxml` `ElementTree` object.
        """
        print("Enter the credential information for the report.")
        api_user = input("API USER NAME: ")
        api_user_pass = getpass.getpass("API PASS: ")
        report_key = getpass.getpass("REPORT KEY: ")
        req = requests.get(self.report_url,
                           auth=HTTPBasicAuth(api_user, api_user_pass),
                           params = {'api_key': report_key})
        return etree.XML(req.content)

    def row_2_dict(self, row_element):
        """
        Helper to translate a single table row into a dictionary of columns and column values.

        Args:
            row_element (Element): A single xml row element of a table.

        Returns:
            A dict whose keys are the column labels of the row, and the values are the column values.
        """
        row_dict = dict()
        for col_element in row_element.getchildren():
            row_dict[col_element.tag] = col_element.text
        return row_dict

    def xml_2_table(self, xml):
        """
        Transform an xml-formatted LegalServer report into a Pandas Dataframe of the report.

        Args:
            xml (ElementTree): An ElementTree object representing the xml LegalServer report.

        Returns:
            A Pandas Dataframe of the the LegalServer Report.
        """
        try:
            report = xml.getroot()
        except AttributeError:
            report = xml
        report_list = []
        for row in report:
            report_list.append(self.row_2_dict(row))
        return pandas.DataFrame(report_list)


    def get_report(self, format='pandas'):
        """
        Function for retrieving a LegalServer Report from the LegalServer Reports API.

        Usage:
            from ls_report_agent import ReportAgent
            agent = ReportAgent(reportURL)
            rpt = agent.get_report(format='pandas')
            assert isinstance(rpt, pandas.DataFrame)

        Args:
            format (string): Default is 'pandas'. The format of the table you'd like returned. Other options are
                - 'raw', to return the raw xml

        Return:
            A LegalServer report in a format dictated by the `format` parameter.
        """
        xml = self.get_raw_xml()
        if format == 'pandas':
            return(self.xml_2_table(xml))
        elif format == 'raw':
            return xml
        else:
            print("Format not recognized. Returning Pandas dataframe.")
            return(self.xml_2_table(xml))
