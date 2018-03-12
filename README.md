# LS Report Agent


Python Module to download and parse reports from LegalServer.

    from ls_report_agent import ReportAgent
    agent = ReportAgent(api_user, api_user_password, report_url, report_key, col_mapper = col_mapper)
    rpt = agent.get_report(format='pandas')
    assert isinstance(rpt, pandas.DataFrame)

The `ReportAgent` requires two parameters: `report_url` is the url to a LegalServer report with the `load` parameter included. `report_key` is the api key to the report.

`ReportAgent` also accepts an optional parameter, `col_mapper`. LegalServer reports are exported with internal legalserver column names, not the more readable column names that you can define yourself. So you can pass `ReportAgent` a dict that maps the LegalServer column names to your own.


## Managing passwords to the LegalServer API

You need to do this somehow, and I've experimented with a few options.

1. __Worst option__: A yaml file that you keep out of source control with the credential information. Passwords are still stored as plain text, so this is the worst idea.
2. Use `getpass` to just enter passwords yourself when you need it. Maybe the safest option, but also very inconvenient because it limits automation.
3. Use `keyring` and `keyring_jeepney` and your system's keyring to store the credentials.
4. Use something like Vault for very paranoid secret storage. Or you could work out some way to use Docker secrets.

To set the credentials:

        import keyring
        import keyring_jeepney
        keyring.set_keyring(keyring_jeepney.Keyring())
        #for each credential you'll store:
        keyring.set_password('namespace', 'label', 'secret')
