# custom function to get object or return none if not found

def get_object_or_none(model_name, **kwargs):
    try:
        obj = model_name.objects.get(**kwargs)
        return obj
    except model_name.DoesNotExist:
        return None