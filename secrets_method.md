# How Secrets are managed in this tool 

In this code, there is a need for various API keys, and account logon details. 

This toll is designed to be a shared/distributed process, whoich means code is shared amongst technical operators. 

To prevent the acciedental sharing of secrets, there is a carefully proscribed method that should be adhered to. 

## Summary

There is local file that is stored on any local machine, not in the git folder. It holds the various keys etc, and is never shared. 

The secrets file is read by the tool, and it retrieves any secrets it needs from the file. 

### Secrets file. 

You can store any secrets you need in this file. The googlesheet keys and location are the bare minimum, other harvesters (e.g. the instagram harvester) uses the same method to get its instagram username and password.

Its a simple text file. 

It must contain the heading 

    [configuration]
    
and then any secrets labelled accordingly. 

     my_api_key =  123456789abcdefg
     sprsh = https://docs.google.com/spreadsheets/d/12345678990qwerty

### the python code

    secrets_and_credentials_fold = r"C:\Source\secrets_and_credentials"
    sprsh_file = os.path.join(secrets_and_credentials_fold, "spreadsheet")
    config = configparser.ConfigParser()
    config.read(sprsh_file)
    
Set `secrets_and_credentials_fold` to the local folder you use to store the secrets file. 
Set the last arguemnt in `sprsh_file` (`"spreadsheet") to the filename of your secrets file. 

    ## credentials
    sprsh = config.get("configuration","sprsh")
    
This gets any secret from the secrets file, in the section caled `"configuration"` that is labelled `"sprsh"`
    
