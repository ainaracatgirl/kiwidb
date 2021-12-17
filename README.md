# KiwiDB
HTTP graph database built in Python 3.

## Reference Format
References are strings in the format:
```{refIDENTIFIER@GROUP}```

## Authentication
Currently, there is no authentication system. I'm working to implement one.

## Query depth
Currently, there is no query depth. I'm working to implement it.

## HTTP API
### Query node by reference
**GET** /{refIDENTIFIER@GROUP}<br>
*Response 200 with JSON body*

### Query nodes by group
**GET** /@GROUP<br>
*Response 200 with JSON body*

### Insert node with reference
**PUT** /{refIDENTIFIER@GROUP}<br>
*Request must have JSON body*<br>
*Response 201 with Location header*

### Insert node into group
**PUT** /@GROUP<br>
*Request must have JSON body*<br>
*Response 201 with Location header*

### Remove node
**DELETE** /{refIDENTIFIER@GROUP}<br>
*Response 200*

### Update node
**PATCH** /{refIDENTIFIER@GROUP}<br>
*Request must have JSON body*<br>
*Response 200*