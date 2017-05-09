import yaml
import sys

def load_yaml(filename):
    with open(filename, 'r') as stream:
        try:
            data =  yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return data


def save_yaml(filename,data):
    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


def compare_dicts(dct, cpr_dct):
    for k, v in cpr_dct.iteritems():
        if k not in dct:
	     print k + " should be present"
	     sys.exit()
        if not isinstance(dct[k], type(cpr_dct[k])):
	     print k + "  value not same data type"
	     sys.exit()
	if isinstance(dct[k], dict):
	     compare_dicts(dct[k],cpr_dct[k])
	else:
	     print 'dct value: '
	     print dct[k]
	     print 'cpr_dct value: '
	     print cpr_dct[k]
	     print "---------"

def compare_value(val, cpr_val):
    print "comparing "
    print val
    print cpr_val
    if isinstance(val, type(cpr_val)):
        if isinstance(val, dict):
            for k, v in cpr_val.iteritems():
                if k in val:
                    if isinstance(val[k], type(cpr_val[k])):
		        compare_value(val[k],cpr_val[k])
                    else:
        	        print k + "  value not same data type"
        	        sys.exit()
                elif '<ANYVAL>' in k:
                    match_cnt = 0
                    for j, l in val.iteritems():
                        print "Printing j:"
                        print j
                        compare_value(val[j],cpr_val[k])
                else: 
        	    print k + " should be present"
        	    sys.exit()

        #    for k, v in val.iteritems():
        #        if k in cpr_val:
        #            if isinstance(val[k], type(cpr_val[k])):
	#	        compare_value(val[k],cpr_val[k])
        #            else:
        #	        print k + "  value not same data type"
        #	        sys.exit()
        #        else: 
	#            anykey = next(iter(cpr_val))
	#	    print anykey
	#            if '<ANYVAL>' in anykey:
	#                compare_value(val[k],cpr_val[anykey])
	#            else:
        #	        print k + " should be present"
        #	        sys.exit()

                #if k not in cpr_val:
	        #    anykey = next(iter(cpr_val))
		#    print anykey
	        #    if '<ANYVAL>' in anykey:
	        #        compare_value(val[k],cpr_val[anykey])
	        #    else:
        	#        print k + " should be present"
        	#        sys.exit()
                #if not isinstance(val[k], type(cpr_val[anykey])):
        	#    print k + "  value not same data type"
        	#    sys.exit()
		#compare_value(val[k],cpr_val[k])
        	#if isinstance(dct[k], dict):
        	#     compare_value(val[k],cpr_val[k])
        	#else:
		#     compare_value(val,cpr_val)
        elif isinstance(val, list):
            for i in val:
	        if isinstance(i, type(cpr_val[0])):
		    if isinstance(i, list):
		        compare_value(i, cpr_val[0][0])
	            else:
		        compare_value(i, cpr_val[0])
		else:
		    print i + "  value not same data type"
		    sys.exit()

        else:
            print 'val: %s  cpr_val: %s' % (val,cpr_val)
            print "---------"
    else: 
        print k + "  value not same data type"
        sys.exit()

dct=load_yaml(sys.argv[1])
cpr_dct=load_yaml(sys.argv[2])
#compare_dicts(dct, cpr_dct)
compare_value(dct, cpr_dct)

