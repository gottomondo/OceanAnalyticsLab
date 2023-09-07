#!/usr/bin/env python


def load_fields() -> dict:
    import json
    with open('tools/fields.json') as json_file:
        return json.load(json_file)


def get_output_var(id_field):
    data_fields = load_fields()
    out_variable = data_fields.get('id_field-out_variable', {}).get(id_field)
    if out_variable is None:
        raise Exception("Can't find " + id_field + " in id_field-out_variable")
    else:
        return out_variable


def get_cf_standard_name(id_field):
    data_fields = load_fields()
    fields_cf_std_name = data_fields['id_field-cf_standard_name']
    if id_field in fields_cf_std_name:
        cf_std_names = fields_cf_std_name[id_field]
    else:
        raise Exception("Field " + id_field + " unknown")

    return cf_std_names
