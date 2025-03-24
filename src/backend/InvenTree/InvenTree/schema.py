"""Schema processing functions for cleaning up generated schema."""

from common.currency import currency_code_mappings


def postprocess_currency_enums(result, generator, request, public):
    """Convert currency enums to string while leaving the richer help text that comes from processing choice field."""
    currency_values = set()
    for key, _name in currency_code_mappings():
        currency_values.add(key)

    schemas = result.get('components', {}).get('schemas', {})
    for schema in schemas.values():
        properties = schema.get('properties', {})
        for field in properties:
            values = properties.get(field)

            # only act on properties with an enum type that contains the currency enum
            if not currency_values.issubset(values.get('enum', [])):
                continue

            # remove currency enum attribute while maintaining description metadata
            values.pop('enum')
            values.pop('x-spec-enum-id')

    return result


def postprocess_required_nullable(result, generator, request, public):
    """Un-require nullable fields.

    Read-only values are all marked as required by spectacular, but InvenTree doesn't always include them in the response. This removes them from the required list to allow responses lacking read-only nullable fields to validate against the schema.
    """
    # Process schema section
    schemas = result.get('components', {}).get('schemas', {})
    for schema in schemas.values():
        required_fields = schema.get('required', [])
        properties = schema.get('properties', {})

        # copy list to allow removing from it while iterating
        for field in list(required_fields):
            field_dict = properties.get(field, {})
            if field_dict.get('readOnly') and field_dict.get('nullable'):
                required_fields.remove(field)
        if 'required' in schema and len(required_fields) == 0:
            schema.pop('required')

    return result
