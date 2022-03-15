from flask import Flask, request
import requests
import json

# bot credentials
bot_name = 'alexandra@webex.bot'
#roomId = 'Y2lzY29zcGFyazovL3VzL1JPT00vMWM4ZWRjMjQtMzBmYi0zZTFjLTk3OTgtODU5ZGVlMTYyNThl'
token = 'ZDRjOWEyMzMtN2Q5OS00MTUwLTk3YzgtNjk5YjBjMjFjNjZhZWViZmQyNGItNTY3_PE93_8d150a97-48b0-4274-bc9d-59a26a936ea5'

header = {
    "content-type": "application/json; charset=utf-8",
    "authorization": "Bearer " + token
}

# Flask is started
app = Flask(__name__)


# checking the certificate of a hostname
def check_certificate(hostname):

    # used for port and fingerprint information
    response = requests.get("https://networkcalc.com/api/security/certificate/{website}".format(website = hostname))
    if (response.status_code != 200):
        return """Incorrect parameters. Usage **/certificate \{hostname\}.**"""

    # dns and ttl information
    dns_response = requests.get("https://networkcalc.com/api/dns/lookup/{website}".format(website = hostname))
    if (response.status_code != 200):
        return """Incorrect parameters. Usage **/certificate \{hostname\}.**"""


    hostname = response.json()['certificate']['hostname']
    port = response.json()['certificate']['port']
    issued_by = response.json()['certificate']['issued_by']
    fingerprint = response.json()['certificate']['fingerprint']
    raw = response.json()['certificate']['raw']
    dns_lookup = dns_response.json()['records']['A'][0]['address']
    ttl = dns_response.json()['records']['A'][0]['ttl']

    # beautifully markdowned
    markdown = """ Information about {host} 👇

    - 🏇 Hostname:         {host_n}
    - 🚪 Port:             {p}
    - 🏠 Issued by:        {i}
    - ☝️ Fingerprint:      {fprint}
    - 🧗 DNS:              {dns}
    - 🧟‍♂️ TTL:              {ttl}
    
    """.format(
        host = hostname,
        host_n = hostname,
        p = port,
        i = issued_by,
        fprint = fingerprint,
        dns = dns_lookup,
        ttl = ttl
    )

    return markdown


# conversion for different bases and radices
def convert_binary(number, base, to):

    # getting the base and radix
    response = requests.get("https://networkcalc.com/api/binary/{num}?from={b}&to={t}".format(num = number, b = base, t = to))
    if (response.status_code != 200):
        return """Incorrect parameters. Usage: **/convert {number} {base} {to}** (example: /convert 00010101 2 16)\nAcceptable parameters for **base** and **to** are [2,8,10,16] """

    original_num = response.json()['original']
    converted_num = response.json()['converted']

    # beautifully markdowned
    markdown = """ Conversion results 👇

    - 📩 [  base {b}  ] Original number   :           {org}
    - 🧮 [  base {t}  ] Converted number  :           {conv}

    """.format(
        b = base,
        t = to,
        org = original_num,
        conv = converted_num
    )
    return markdown

# subnetting 
def get_subnet(ip):


    response = requests.get("https://networkcalc.com/api/ip/{}?binary=true".format(ip))
    if (response.status_code != 200):
       return """IP Address is incorrect. Usage  **/subnet \{ip_address\}/{slash_notation\}** (example: 192.168.1.1/24) """ 
    
    # getting infromation from the API
    cidr_notation           = response.json()['address']['cidr_notation']
    subnet_bits             = response.json()['address']['subnet_bits']
    subnet_mask             = response.json()['address']['subnet_mask']
    wildcard_mask           = response.json()['address']['wildcard_mask']
    network_address         = response.json()['address']['network_address']
    broadcast_address       = response.json()['address']['broadcast_address']
    assignable_hosts        = response.json()['address']['assignable_hosts']
    first_assignable_host   = response.json()['address']['first_assignable_host']
    last_assignable_host    = response.json()['address']['last_assignable_host']

    # beautifully markdowned
    markdown = """ **Information about {ip_address} 👇**
    - 🔢    CIDR notation:                {cidr}
    - 👨‍💻    Subnet Bits:                  {subnet_b}
    - 🤿    Subnet Mask:                  {subnet_m}
    - 🐗    Wildcard Mask:                {wildcard}
    - 🕸️    Network Address:              {network}
    - 🦙    Broadcast Address:            {broadcast}
    - 👤    Assignable Hosts:             {host_num} 
    - 🥇    First Assignable Host:        {first_host} 
    - 🥉    Last Assignable Host:         {last_host} 
    """.format(
        ip_address = ip,
        cidr = cidr_notation,
        subnet_b = subnet_bits,
        subnet_m = subnet_mask,
        wildcard = wildcard_mask,
        network = network_address,
        broadcast = broadcast_address,
        host_num = assignable_hosts,
        first_host = first_assignable_host,
        last_host = last_assignable_host
    )

    return markdown

# funny excuse finder
def get_excuse():

    # collecting API reponse
    response = requests.get("https://excuser.herokuapp.com/v1/excuse")
    excuse = response.json()[0]['excuse']

    # beautifully markdowned
    markdown = """We won't tell anyone... 🤫

    {excuse}
     """.format(excuse = excuse)

    return markdown

# generated Chuck Norris joke with a nice gif of Chuck
def get_surprise():

    # collecting API response
    response = requests.get("https://api.chucknorris.io/jokes/random")
    surprise = response.json()['value']
    return surprise


@app.route("/", methods=["GET", "POST"])

def sendMessage():

    webhook = request.json

    url = 'https://webexapis.com/v1/messages'
    msg = {"roomId": webhook["data"]["roomId"]}
    sender = webhook["data"]["personEmail"]

    message = getMessage()

    if (sender != bot_name):  # will be re-evaluated and will mess up the bot

        # initial message, greetings message
        if (message == "/help"):
            msg["markdown"] = """ Hey **""" + sender + """**! I can do the following commands 👇


            - To calculate a subnet:                /subnet {ip_address}/{slash_notation} (example: /subnet 192.168.1.1/24)
            - Binary Converter:                     /convert {number} {base} {to} (example: /convert 00010101 2 16)
            - Look up the certificate of a host:    /certificate {hostname} (example: /certificate cisco.com)
            - Learn about me:                       /aboutbot
            - Do you need an excuse?                /excuse  
            - Wanna see a surprise?                 /surprise
            """
            # network gif
            file_intro = ["https://cdn.discordapp.com/attachments/702193409238106164/953196338336657468/network_intro_new.gif"]
            msg["files"] = file_intro

        # subnetting command
        elif (message.startswith("/subnet")):
            # checking if parameters are right
            try:
                command, ip = message.split()
                data = get_subnet(ip)
                msg["markdown"] = data

            except ValueError:
                print("IP Address not provided.")
                msg["markdown"] = """IP Address is incorrect. Usage  **/subnet \{ip_address\}/{slash_notation\}** (example: 192.168.1.1/24) """ 

        # certificate command
        elif (message.startswith("/certificate")):

            #checking if parameters are right
            try:
                command, hostname = message.split()
                markdown = check_certificate(hostname)    
                msg["markdown"] = markdown

            except ValueError:
                msg["markdown"] = """Incorrect parameters. Usage **/certificate \{hostname\}.**"""

        # conversion command
        elif (message.startswith("/convert")):

            try:
                command, number, base, to = message.split()
                data = convert_binary(number, base, to)
                msg["markdown"] = data

            except ValueError:
                msg["markdown"] = """Incorrect parameters. Usage: **/convert {number} {base} {to}** (example: /convert 00010101 2 16)\nAcceptable parameters for **base** and **to** are [2,8,10,16] """


        elif(message == "/aboutbot"):
            # about bot command
            msg["markdown"] = """

            Hello! My name is Alexandra, the networking bot 🤖. 
            I am here to meet all of your networking needs 🌎.
            My hobies and interests are: 
            - **Travelling** 🌄 (I travel all around Webex!)
            - **IT** 👩‍💻 (I help people get their subnets right!)
            - **Techno Music** 💿 (We all need some fun, right?)
            If you want to see what I am capable of type **/help** 🤙
            Developed with love by Edmond Vujici 💚
            
            """
            # Alexandra's gif
            file = ["https://cdn.discordapp.com/attachments/702193409238106164/953192958096715817/Scala_the_Smart_Bot.gif"]
            msg["files"] = file


        # excuse command
        elif (message == "/excuse"):

            data = get_excuse()

            markdown = data
            msg['markdown'] = markdown

        # surprise command
        elif (message == '/surprise'):
            data = get_surprise()

            markdown = data
            msg['markdown'] = markdown

            # chuck's gif
            file = ["https://cdn.discordapp.com/attachments/702193409238106164/953255551549202442/chuck_gif.gif"]
            msg['files'] = file


        # default when the command is not recognized
        else:
            msg["markdown"] = "Sorry! I didn't recognize that command. Type **/help** to see the list of available commands."
        requests.post(url, data=json.dumps(msg), headers=header, verify=True)

    

    return ""


def getMessage():
    webhook = request.json
    url = 'https://webexapis.com/v1/messages/' + webhook["data"]["id"]
    get_msgs = requests.get(url, headers=header, verify=True)
    message = get_msgs.json()['text']
    return message


app.run(debug=True)
