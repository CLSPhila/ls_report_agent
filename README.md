# LS Report Agent


Python Module to download and parse reports from LegalServer.


    from ls_report_agent import ReportAgent
    agent = ReportAgent(reportURL)
    rpt = agent.get_report(format='pandas')
    assert isinstance(rpt, pandas.DataFrame)


## Managing passwords to the LegalServer API

You need to do this somehow, and I've experimented with a few options.

1. __Worst option__: A yaml file that you keep out of source control with the credential information. Passwords are still stored as plain text, so this is the worst idea.
2. Use `getpass` to just enter passwords yourself when you need it. Maybe the safest option, but also very inconvenient because it limits automation.
3. Use `keyring` and `keyring_jeepney` and your system's keyring to store the credentials. 

To set the credentials:

        import keyring
        import keyring_jeepney
        keyring.set_keyring(keyring_jeepney.Keyring())
        #for each credential you'll store:
        keyring.set_password('namespace', 'label', 'secret')
