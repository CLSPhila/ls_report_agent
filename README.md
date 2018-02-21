# LS Report Agent


Python Module to download and parse reports from LegalServer.


    from ls_report_agent import ReportAgent
    agent = ReportAgent(reportURL)
    rpt = agent.get_report(format='pandas')
    assert isinstance(rpt, pandas.DataFrame)
    
