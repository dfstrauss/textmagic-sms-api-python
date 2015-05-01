[TextMagic](http://www.textmagic.com/) offers a quick, cost-effective way to send text messages from any computer. This package provides a simple Python API on top of the [TextMagic HTTPS API](http://api.textmagic.com/https-api); which is a web-based interface to the SMS functionality.

### Install ###
Install using easy\_install:
```
easy_install PyTextMagicSMS
```

**OR manually:**

  * download it from http://pypi.python.org/pypi/PyTextMagicSMS
  * unzip the downloaded file
  * change into the `PyTextMagicSMS-x.x` directory
  * run `setup.py` as follows
```
python setup.py install
```
  * `PyTextMagicSMS` depends on **one** of the following:
    * Python 2.6 or
    * django or
    * simplejson (which can be downloaded from http://pypi.python.org/pypi/simplejson or `easy_install simplejson`)

### Register ###
Before using the service you need to register at http://www.textmagic.com/ and obtain an API password (different from your login password) at https://www.textmagic.com/app/wt/account/api/cmd/password.

### Get Started ###
Now you are ready to send your first SMS:
```
import textmagic.client
client = textmagic.client.TextMagicClient('your_username', 'your_api_password')
result = client.send("Hello, World!", "1234567890")
message_id = result['message_id'].keys()[0]
```
And you can retrieve the delivery status of the message:
```
response = client.message_status(message_id)
status = response[message_id]['status']
```

There is more detail in the UserManual

# <a href='http://www.textmagic.com/affiliate/fordevelopers.html'>SMS Gateway Affiliate Programme For Developers</a> #

Here’s what you’ll get:

<li>A 10% share of the lifetime value of the customer. If a customer spends £5,000 on SMS credit during his or her membership of TextMagic, you’ll earn £500.</li>

<li>Bonus: we’ll pay you a £15 flat fee for each new paying customer referral. You’ll still get your 10% revenue share from their initial order, too.</li>
