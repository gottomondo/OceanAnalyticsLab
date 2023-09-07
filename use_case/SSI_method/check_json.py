#!/usr/bin/env python

import json


def print_id_name(mobj):
    # print("outFile ",type(mobj))
    for x in mobj:
        # print(x)
        # print(type(mobj[x]))
        for l in mobj[x]:  # type list
            # print(type(l))  #type dict
            print(l['id'], l['name'])
            # for m in l :
            #    print(m,l[m])


def get_id(resp):
    lId = list()
    for item in resp['itemlist']:
        # print(item['id'])
        lId.append((item['id'], item['name']))
    return lId


def main():
    mobj = json.load(open('outFile'))
    # print(json.dumps(mobj,indent=5))
    # print_id_name(mobj)
    print(get_id(mobj))


if __name__ == "__main__":
    main()
