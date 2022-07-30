def get_tag(tags, key):
    for tag in tags:
        if tag['Key'] == key:
            return tag['Value']
