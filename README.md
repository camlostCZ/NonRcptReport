# NonRcptReport
Tool to lookup up non-existing recipients in Postfix log and report them via CSV file

As contact list grows an organization often needs to validate individual contact's
e-mail address to minimize number of messages sent to non-existing recipients.
Otherwise the SMTP server would get temporarily blocked or even blacklisted.

This tool provides a report of non-existing recipients. It analyzes Postfix log files,
looks up typical SMTP server responses and collects e-mail addresses together with
some additional data into a CSV file.

That file can be used further to for example clear invalid e-mail addresses from CRM.
