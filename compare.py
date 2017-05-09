import yaml
import sys
import re
import sys


def match_regex(regex, matchstring):
    return True if re.search(regex, matchstring) else False

def load_yaml(filename):
    with open(filename, 'r') as stream:
        try:
            data =  yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit()
    return data


def save_yaml(filename,data):
    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


def compare_value(val, cpr_val, key):
    #print "comparing "
    #print val
    #print cpr_val
    #superkey=key[:]
    if isinstance(val, type(cpr_val)): # Checking if data type is the same of both values
        if isinstance(val, dict): # checking if data type is dictionary
            for k, v in cpr_val.iteritems(): # for each value in the template dictionary value
                if k in val: # if the same key exists in deploy.yaml data
                    superkey=key+'->'+k
                    if isinstance(val[k], type(cpr_val[k])): # checking if value in both dicts has the same data type
                        compare_value(val[k],cpr_val[k],superkey)
                    else:
                        print superkey + " value shoudl be a:" + type(cpr_val[k]).__name__
        	        #sys.exit()
                elif '<ANYVAL>' in k: # if key is not in deploy.yaml data then check if there is a WILDCARD in template dictionary. 
                    #superkey=key+'-> * '
                    match_cnt = 0
                    for j, l in val.iteritems(): # for each key in template dict that has the wildcard, iterate over all the keys in deploy.yaml dict and match values
                        #print "Printing j:"
                        #print j
                        superkey=key+'->'+j
                        compare_value(val[j],cpr_val[k],superkey)
                else: # Key is missing in deploy.yaml data .. Change the lock.
                    superkey=key+'->'+k
                    print superkey + " should be present with value:" + type(cpr_val[k]).__name__
        	    #sys.exit()
        elif isinstance(val, list): # checking if data type is a list
            for i in val: # for each item in list (deploy.yaml)
                superkey=key+'-> LIST_VALUE '
	        if isinstance(i, type(cpr_val[0])): # matching item with first item of template list
		    compare_value(i, cpr_val[0], superkey)
		    #if isinstance(i, list): # if item value is a list then match with first item of first item of template list 
		    #    compare_value(i, cpr_val[0], superkey)
	            #else:
		    #    compare_value(i, cpr_val[0], superkey) # if any other data type then just compare with first item of template list
		else: # data type not same of item value
		    print superkey + "  should be a " + type(cpr_val[0]).__name__
		    #sys.exit()

        else: # Key exists in the right structure. Checking for corresponding regex.
            if match_regex(cpr_val,val):
                print 'PASS: key: %s val: %s  cpr_val: %s' % (key, val,cpr_val)
            else: 
                print 'MISMATCH XXXX: key: %s val: %s  cpr_val: %s' % (key, val,cpr_val)
            #key = ''
    else: # data type does not match
        print val
        print cpr_val
        print key + "  value not same data type as " + type(cpr_val).__name__
        #key = ''
        #sys.exit()

dct=load_yaml(sys.argv[1])
cpr_dct=load_yaml(sys.argv[2])
#compare_dicts(dct, cpr_dct)
compare_value(dct, cpr_dct, '')

