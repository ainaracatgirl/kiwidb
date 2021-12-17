# KiwiDB
HTTP graph database built in Python 3.

## Reference Format
References are strings in the format:
```{refIDENTIFIER@GROUP}```

## Authentication
Currently, there is no authentication system. I'm working to implement one.

## HTTP API
### Query node by reference
**GET** /{refIDENTIFIER@GROUP}
*Response 200 with JSON body*

### Query nodes by group
**GET** /@GROUP
*Response 200 with JSON body*

### Insert node with reference
**PUT** /{refIDENTIFIER@GROUP}
*Request must have JSON body*<br>
*Response 201 with Location header*

### Insert node into group
**PUT** /@GROUP
*Request must have JSON body*<br>
*Response 201 with Location header*

### Remove node
**DELETE** /{refIDENTIFIER@GROUP}
*Response 200*

### Update node
**PATCH** /{refIDENTIFIER@GROUP}
*Request must have JSON body*<br>
*Response 200*