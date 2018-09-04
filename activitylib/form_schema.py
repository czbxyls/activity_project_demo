INTEGER_SCHEMA = {"type": "string", "pattern": r"^[0-9]+$"}
BOOLEAN_SCHEMA = {"type": "string", "pattern": r"^(True|False)$"}
STRING_SCHEMA = {"type": "string", "minLength": 1, "maxLength": 100, }
COUNTRY_SCHEMA = {"type": "string", "minLength": 2, "maxLength": 2, "pattern": r"^[A-Z]+$"}
COMMENT_SCHEMA = {"type": "string", "minLength": 1, "maxLength": 100}


API_OPS_CHANNEL_UPDATE_SCHEMA = {
    "type": "object",
    "properties": {
        "name": STRING_SCHEMA,
        "id": INTEGER_SCHEMA,
    },
    "required": ["name", "id"]
}

API_OPS_CHANNEL_ADD_SCHEMA = {
    "type": "object",
    "properties": {
        "name": STRING_SCHEMA
    },
    "required": ["name"]
}


API_OPS_CHANNEL_DEL_SCHEMA = {
    "type": "object",
    "properties": {
        "id": INTEGER_SCHEMA
    },
    "required": ["id"]
}


API_OPS_ACTIVITY_ADD_SCHEMA = {
    "type": "object",
    "properties": {
        "name": STRING_SCHEMA,
        "channel_id": INTEGER_SCHEMA,
        "begin_time": INTEGER_SCHEMA,
        "end_time": INTEGER_SCHEMA,
    },
    "required": ["name","channel_id","begin_time","end_time"]
}


API_OPS_ACTIVITY_DEL_SCHEMA = {
    "type": "object",
    "properties": {
        "id": INTEGER_SCHEMA
    },
    "required": ["id"]
}

API_OPS_ACTIVITY_UPDATE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": INTEGER_SCHEMA,
    },
    "required": ["id"]
}


API_ACTIVITY_JOIN_SCHEMA = {
    "type": "object",
    "properties": {
        "activity_id": INTEGER_SCHEMA,
        "is_join": BOOLEAN_SCHEMA,
    },
    "required": ["activity_id","is_join"]
}

API_ACTIVITY_COMMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "activity_id": INTEGER_SCHEMA,
        "content": STRING_SCHEMA,
    },
    "required": ["activity_id","content"]
}


API_ACTIVITY_QUERY_SCHEMA = {
    "type": "object",
    "properties": {
        "channel_id": INTEGER_SCHEMA,
        "begin_time": STRING_SCHEMA,
        "end_time": STRING_SCHEMA,
    }
}

API_ACTIVITY_COMMON_SCHEMA = {
    "type": "object",
    "properties": {
        "activity_id": INTEGER_SCHEMA
    },
    "required": ["activity_id"]
}


API_AUTH_LOGIN_SCHEMA = {
    "type": "object",
    "properties": {
        "username": STRING_SCHEMA,
        "password": STRING_SCHEMA,
    },
    "required": ["username", "password"]
}

# def schema_check(item_name,item_schema, value):
# 	if item_schema.has_key('minLength') or item_schema.has_key('maxLength'):
# 		length = len(value) if value else 0
# 		min_len = item_schema.get('minLength', 0)
# 		max_len = item_schema.get('maxLength', 0)
# 		if min_len > 0 and length < min_len:
# 			raise error.MessageError('%s\'min_len expected=%d, now=%d' %(item_name, min_len, length))
# 		if max_len > 0 and length > max_len:
# 			raise error.MessageError('%s\'max_len expected=%d, now=%d' %(item_name, max_len, length))
# 	if item_schema.has_key('pattern'):
# 		pattern_str = item_schema['item_schema']
# 		pattern = re.compile(pattern_str)
# 		if not pattern.match(value):
# 			raise error.MessageError('%s\'pattern doesn\'t match' %(item_name))
# 	if item_schema.has_key('minimum'):
# 		minimum = item_schema.get('minimum')
# 		if value < minimum:
# 			raise error.MessageError('%s\'minimum expected=%s, now=%s' %(item_name, str(minimum), str(value)))
# 	if item_schema.has_key('maximum'):
# 		maximum = item_schema.get('maximum')
# 		if value > maximum:
# 			raise error.MessageError('%s\'maximum expected=%s, now=%s' %(item_name, str(maximum), str(value)))