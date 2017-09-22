#!/usr/bin/python

import re
import sys
import yaml

YAML_VALID = True
REGEX_DESCRIPTIONS = {
    "^([0-9A-Za-z-._]{1,30})$":
        "string between 1 and 30 characters."
        " Allowed characters: '0-9A-Za-z-._'",
    "^([0-9A-Za-z-., \\(\\)]{1,40})$": "string between 1 and 40 characters. "
                                 "Allowed characters: '0-9A-Za-z-._ ()'",
    "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$":
        "valid MAC Address. Example: '78:24:af:45:d1:5a'",
    "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.)"
    "{3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$":
        "valid IPv4 Address. Example '192.168.100.10'",
    "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}"
    "([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\\/([0-9]"
    "|[1-2][0-9]|3[0-2]))$":
        "valid CIDR. Example '192.168.10.0/24'"
}


def load_yaml(filename):
    with open(filename, 'r') as stream:
        try:
            data = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit()
    return data


def save_yaml(filename, data):
    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


def return_data_type(datatype):
    if datatype == 'int':
        return int
    elif datatype == 'bool':
        return bool
    elif datatype == 'float':
        return float
    elif datatype == 'long':
        return long
    elif datatype == 'complex':
        return complex
    else:
        return False


def match_data_type(val, cpr_val, superkey):
    str_matchdatatype = cpr_val.split("matchDATATYPE:-", 1)[1]
    matchdatatype = return_data_type(str_matchdatatype)
    if not matchdatatype:
        print("ERROR: Invalid Datatype \"%s\" provided in template" %
            str_matchdatatype)
    if type(val) == matchdatatype:
        #pass
        print('DATATYPEMATCH - PASS: key: %s ' \
          'datatype: %s' % (superkey, str_matchdatatype))
    else:
        print("ERROR: %s should be datatype \"%s\"" %
            (superkey, str_matchdatatype))
        global YAML_VALID
        YAML_VALID = False


def regex_explanation(regex):
    if regex in REGEX_DESCRIPTIONS:
        return REGEX_DESCRIPTIONS[regex]
    else:
        return "value that matches regex: %s" % regex


def match_regex(regex, matchstring):
    return True if re.search(regex, matchstring) else False


def validate_dict(val, cpr_val):
    compare_value(val, cpr_val, '')
    return YAML_VALID


def update_key(key, cur_key):
    if key == "":
        return cur_key
    else:
        return key + " -> " + cur_key


def compare_value(val, cpr_val, key):
    global YAML_VALID
    if isinstance(val, type(cpr_val)):
        # Checking if data type is the same of both values.
        if isinstance(val, dict):
            # checking if data type is dictionary.
            for k, v in cpr_val.iteritems():
                # for each key in the template dictionary key.
                if k in val:
                    # if the same key exists in deploy.yaml data.
                    superkey = update_key(key, k)
                    if isinstance(val[k], type(cpr_val[k])):
                        # checking if value in both dicts has the
                        # same data type.
                        compare_value(val[k], cpr_val[k], superkey)
                    elif 'matchDATATYPE:-' in cpr_val[k]:
                        match_data_type(val[k], cpr_val[k], superkey)
                    else:
                        print("ERROR: %s should be datatype \"%s\"" %
                            (superkey, type(cpr_val[k]).__name__))
                        YAML_VALID = False
                elif 'NODE_ANCHORS' in k:
                    continue
                elif '<ANYVAL>' in k:
                    # if key is not in data then check if there is a
                    # <ANYVAL> wildcard in template dictionary.
                    for j, l in val.iteritems():
                        # for each key in data dict match values
                        # to the value of wildcard key.
                        superkey = update_key(key, j)
                        compare_value(val[j], cpr_val[k], superkey)
                elif 'matchREGEX:-' in k:
                    # if key is not in data dict then check if there is
                    # a REGEX provided in the key and match the key to
                    # the regex.
                    keyregex = k.split("matchREGEX:-", 1)[1]
                    for j, l in val.iteritems():
                        # for each key in data dict match key to the
                        # REGEX provided in the template dict.
                        superkey = update_key(key, j)
                        if match_regex(keyregex, j):
                            print('KEY-REGEXMATCH - PASS: key: %s ' \
                                 'regex: %s' % (superkey, keyregex))
                            compare_value(val[j], cpr_val[k], superkey)
                        else:
                            print('ERROR: %s should be a '
                                '%s' % (superkey, regex_explanation(keyregex)))
                            YAML_VALID = False
                else:
                    # Key is missing in deploy.yaml data .. Change the lock.
                    superkey = update_key(key, k)
                    print("ERROR: %s does not exist" % superkey)
                    YAML_VALID = False
        elif isinstance(val, list):
            # checking if data type is a list
            for i in val:
                # for each item in list (deploy.yaml)
                superkey = update_key(key, 'LIST-ITEM')
                if isinstance(i, type(cpr_val[0])):
                    # matching item with first item of template list
                    compare_value(i, cpr_val[0], superkey)
                elif 'matchDATATYPE:-' in cpr_val[0]:
                    match_data_type(i, cpr_val[0], superkey)
                else:
                    # data type not same of item value
                    print("ERROR: %s should be datatype \"%s\"" %
                        (superkey, type(cpr_val).__name__))
                    YAML_VALID = False
        else:
            # Key exists in the right structure. Checking for
            # corresponding regex.
            if match_regex(cpr_val, val):
                #pass
                print('PASS: key: %s val: %s  cpr_val: ' \
                     '%s' % (key, val, cpr_val))
            elif 'matchDATATYPE:-' in cpr_val:
                match_data_type(val, cpr_val, key)
            else:
                print("ERROR: %s : \"%s\" should be a %s" %
                    (key, val, regex_explanation(cpr_val)))
                YAML_VALID = False
    elif 'matchDATATYPE:-' in cpr_val:
        match_data_type(val, cpr_val, key)
    else:
        # data type does not match
        print("ERROR: %s : \"%s\" should be datatype \"%s\"" %
            (key, val, type(cpr_val).__name__))
        YAML_VALID = False


if __name__ == "__main__":
    dct = load_yaml(sys.argv[1])
    cpr_dct = load_yaml(sys.argv[2])
    compare_value(dct, cpr_dct, '')
