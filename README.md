# Steam Spy
A simple python program for sending e-mail messages of steam products with a discount.  
The program processes data from [Steam API](https://store.steampowered.com/api/featuredcategories).

## Usage
````
python3 steam_spy.py <-s> <sender_email>
                     <-p> <sender_password>
                     <-r> <receiver_email_1> [receiver_email_2] [..]
                     [-d] [<minimum_discount>]
                     [-l] [<report_lifespan>]
                     [-f] [<report_filepath>]
````
## Arguments
````
  -s, --sender        Sender's email address.
  -p, --password      Sender's password.
  -r, --receivers     Recipients email addresses.
  -d, --discount      Minimum percentage discount on the product for sending a message.
  -l, --lifespan      Lifetime of reports of the reported applications in days.
  -f, --filepath      Filepath of the reported applications.
````
## Configuration
The configuration file is located in the following path: `config/setting.yaml`.
The program takes the values from the configuration file as default values when the appropriate argument is not specified.
````
discount: 50
lifespan: 14
filepath: 'report_database'
sender:
  email: 'sender@gmail.com'
  password: 'the_sender_password'
receivers:
- 'receiver1@gmail.com'
- 'receiver2@gmail.com'
````
## Examples
Send the report to `receiver@gmail.com` with default setting:  
````
python3 steam_spy.py -s sender@gmail.com -p password -r receiver@gmail.com
````
Send the report to `receiver1@gmail.com` and `receiver2@gmail.com` with default setting:  
````
python3 steam_spy.py -s sender@gmail.com -p password -r receiver1@gmail.com receiver2@gmail.com
````
Send the report to `receiver@gmail.com` with a minimum product discount of `75%`:  
````
python3 steam_spy.py -s sender@gmail.com -p password -r receiver@gmail.com -d 75
````
Send the report to `receiver@gmail.com` with a lifetime of `21` days for reported products stored in `/tmp/report.log`:  
````
python3 steam_spy.py -s sender@gmail.com -p password -r receiver@gmail.com -l 21 -f /tmp/report.log
````
