import yaml
import sys
import re
import sys


def match_regex(regex, matchstring):
    return True if re.search(regex, matchstring) else False


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


def compare_value(val, cpr_val, key):
    if isinstance(val, type(cpr_val)):
        # Checking if data type is the same of both values.
        if isinstance(val, dict):
            # checking if data type is dictionary.
            for k, v in cpr_val.iteritems():
                # for each key in the template dictionary key.
                if k in val:
                    # if the same key exists in deploy.yaml data.
                    superkey = key + '->' + k
                    if isinstance(val[k], type(cpr_val[k])):
                        # checking if value in both dicts has the
                        # same data type.
                        compare_value(val[k], cpr_val[k], superkey)
                    else:
                        print "KEY VALUE ERROR: " + superkey + \
                              " value should be a: " + \
                              type(cpr_val[k]).__name__
                elif '<ANYVAL>' in k:
                    # if key is not in data then check if there is a
                    # <ANYVAL> wildcard in template dictionary.
                    for j, l in val.iteritems():
                        # for each key in data dict match values
                        # to the value of wildcard key.
                        superkey = key + '->' + j
                        compare_value(val[j], cpr_val[k], superkey)
                elif 'matchREGEX:-' in k:
                    # if key is not in data dict then check if there is
                    # a REGEX provided in the key and match the key to
                    # the regex.
                    keyregex = k.split("matchREGEX:-", 1)[1]
                    for j, l in val.iteritems():
                        # for each key in data dict match key to the
                        # REGEX provided in the template dict.
                        superkey = key + '->' + j
                        if match_regex(keyregex, j):
                            print 'KEY-REGEXMATCH - PASS: key: %s ' \
                                  'regex: %s' % (superkey, keyregex)
                            compare_value(val[j], cpr_val[k], superkey)
                        else:
                            print 'KEY ERROR: %s should match regex:' \
                                  '%s' % (superkey, keyregex)
                else:
                    # Key is missing in deploy.yaml data .. Change the lock.
                    superkey = key + '->' + k
                    print "KEY ERROR: " + superkey + " should exist " \
                          "with value: " + type(cpr_val[k]).__name__
        elif isinstance(val, list):
            # checking if data type is a list
            for i in val:
                # for each item in list (deploy.yaml)
                superkey = key + '-> LIST-ITEM '
                if isinstance(i, type(cpr_val[0])):
                    # matching item with first item of template list
                    compare_value(i, cpr_val[0], superkey)
                else:
                    # data type not same of item value
                    print "KEY VALUE ERROR: " + superkey + "  value should " \
                          "be a: " + type(cpr_val[0]).__name__
        else:
            # Key exists in the right structure. Checking for
            # corresponding regex.
            if match_regex(cpr_val, val):
                print 'PASS: key: %s val: %s  cpr_val: ' \
                      '%s' % (key, val, cpr_val)
            else:
                print 'KEY VALUE ERROR: key: %s value: %s should pass ' \
                      'REGEX: %s' % (key, val, cpr_val)
    else:
        # data type does not match
        print "KEY VALUE ERROR: " + key + " value should be a: " + \
              type(cpr_val).__name__

dct = load_yaml(sys.argv[1])
cpr_dct = load_yaml(sys.argv[2])
compare_value(dct, cpr_dct, '')
