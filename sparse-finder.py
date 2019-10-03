#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ###############################################################################
# Copyright 2019 Larry Deck
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################


#
# Much of this code is adapted from example code in the repository
#   https://github.com/OCLC-Developer-Network/oclc-auth-python
#


from authliboclc import wskey, user
import requests
import xml.etree.ElementTree as ET
import sys


#
# Authentication Parameters
#
# Requires a WSKEY for OCLC's Metadata API
#   Request one at
#   https://platform.worldcat.org/wskey/keys/manage
#
# Also requires principleID and principleIDNS as per
#   https://www.oclc.org/developer/develop/authentication/user-level-authentication-and-authorization.en.html
#

key = '{wskey}'
secret = '{secret}'
principal_id = '{principleID}'
principal_idns = '{principleIDNS}'
authenticating_institution_id = '{registryID}'
context_institution_id = '{registryID}'

# Configure the wskey library object

my_wskey = wskey.Wskey(
    key=key,
    secret=secret,
    options={'services': ['WorldCatMetadataAPI']})

my_user = user.User(
    authenticating_institution_id=authenticating_institution_id,
    principal_id=principal_id,
    principal_idns=principal_idns
)

# Get an access token
access_token = my_wskey.get_access_token_with_client_credentials(
    authenticating_institution_id=authenticating_institution_id,
    context_institution_id=context_institution_id,
    user=my_user
)

# Describe the token received, or the error produced
print("")
if (access_token.access_token_string == None):
    if (key == '{wskey}'):
        print(
        "**** You must configure the key, secret, authenticating_institution_id and context_institution_id ****")
        print("")
    print("error_code:    " + `access_token.error_code`)
    print("error_message: " + access_token.error_message)
    print("error_url:     " + access_token.error_url)
else:
    print("access token:  " + access_token.access_token_string)
    print("expires_in:    " + `access_token.expires_in`)
    print("expires_at:    " + access_token.expires_at)
    print("type:          " + access_token.type)
    if (access_token.refresh_token != None):
        print("refresh_token: " + access_token.refresh_token)

authorization = 'Bearer ' + access_token.access_token_string
headers={'Authorization': authorization, 'Accept': 'application/atom+xml;content="application/vnd.oclc.marc21+xml"'}

#
# Take a list of OCLC numbers from stdin and search each one through the Metadata API
#


for line in sys.stdin:
    request_url = 'https://worldcat.org/bib/data/' + line
    

    try:
        r = requests.get(request_url, headers=headers)
        r.raise_for_status()
        
        # parse response as XML

        root = ET.fromstring(r.content)

        ns = {'atomns': 'http://www.w3.org/2005/Atom',
                'rb': 'http://worldcat.org/rb',
                'rec': 'http://www.loc.gov/MARC21/slim'}
        
        content = root.find('atomns:content', ns)
        response = content.find('rb:response', ns)
        record = response.find('rec:record', ns)

        # Sierra numbers are in the 036

        my036 =  record.find('rec:datafield[@tag="036"]', ns)
        mysierra = my036.find('rec:subfield[@code="a"]', ns).text

        my245 = record.find('rec:datafield[@tag="245"]', ns)
        mytitle = my245.find('rec:subfield[@code="a"]',ns).text
        
        try:
            print line.rstrip(), mysierra, mytitle
        except UnicodeEncodeError:
            print line.rstrip(), mysierra, "[ MISCODED TITLE ]"
    except requests.exceptions.HTTPError as err:
        print("Read failed. " + str(err.response.status_code))


