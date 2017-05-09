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


def compare_value(val, cpr_val):
    #print "comparing "
    #print val
    #print cpr_val
    if isinstance(val, type(cpr_val)): # Checking if data type is the same of both values
        if isinstance(val, dict): # checking if data type is dictionary
            for k, v in cpr_val.iteritems(): # for each value in the template dictionary value
                if k in val: # if the same key exists in deploy.yaml data
                    if isinstance(val[k], type(cpr_val[k])): # checking if value in both dicts has the same data type
		        compare_value(val[k],cpr_val[k])
                    else:
        	        print k + "  value not same data type"
        	        sys.exit()
                elif '<ANYVAL>' in k: # if key is not in deploy.yaml data then check if there is a WILDCARD in template dictionary. 
                    match_cnt = 0
                    for j, l in val.iteritems(): # for each key in template dict that has the wildcard, iterate over all the keys in deploy.yaml dict and match values
                        #print "Printing j:"
                        #print j
                        compare_value(val[j],cpr_val[k])
                else: # Key is missing in deploy.yaml data .. Change the lock.
        	    print k + " should be present"
        	    sys.exit()
        elif isinstance(val, list): # checking if data type is a list
            for i in val: # for each item in list (deploy.yaml)
	        if isinstance(i, type(cpr_val[0])): # matching item with first item of template list
		    if isinstance(i, list): # if item value is a list then match with first item of first item of template list 
		        compare_value(i, cpr_val[0][0])
	            else:
		        compare_value(i, cpr_val[0]) # if any other data type then just compare with first item of template list
		else: # data type not same of item value
		    print i + "  value not same data type"
		    sys.exit()

        else: # Key exists in the right structure. Checking for corresponding regex.
            if match_regex(cpr_val,val):
                print 'PASS: val: %s  cpr_val: %s' % (val,cpr_val)
            else: 
                print 'MISMATCH XXXX: val: %s  cpr_val: %s' % (val,cpr_val)
    else: # data type does not match 
        #print k + "  value not same data type"
        sys.exit()

dct=load_yaml(sys.argv[1])
cpr_dct=load_yaml(sys.argv[2])
#compare_dicts(dct, cpr_dct)
compare_value(dct, cpr_dct)

