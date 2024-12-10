# 1. 获取API版本

```json
{ 
  "jsonrpc": "2.0", 
  "method": "apiinfo.version", 
  "id": 1, 
  "auth": null, 
  "params": {} 
} 
```



# 2. 获取Token

```json
{
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": "Admin",
        "password": "zabbix"
    },
    "id": 1,
    "auth": null
}
```



# 3.host

## 获取主机名、主机ID和接口

```json
{
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "output": [
            "hostid",
            "host"
        ],
        "selectInterfaces": [
            "interfaceid",
            "ip"
        ]
    },
    "id": 2,
    "auth": "f83e064cbaeed483200f347f5737a3a9"
}
```



## 获取挂载了某个模板的主机信息

```json
{
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "templateids": 10301,
            "output": ["hostid", "name", "ip"],
            "selectInterfaces": ["ip"],
            "selectGroups": ["name"]
        },
        "id": 2,
        "auth": "f83e064cbaeed483200f347f5737a3a9"
    }
```

## 根据主机名获取对应相关数据

```json
{
           "jsonrpc": "2.0",
           "method": "host.get",
           "params": {
               "output": ["hostid"],
               "selectGroups": "extend",
               "selectItems": "extend",
               "selectInterfaces": "extend",
               "selectMacros": "extend",
               "selectParentTemplates":"extend",
               "selectTriggers":"extend",
               "filter": {
                   "host": [
                       "Zabbix server"
                   ]
               },   # "hostid": 10084 也可以根据hostid
            "limitSelects":10
           },
           "auth": "f83e064cbaeed483200f347f5737a3a9",
           "id": 2
       }
```



## 根据标签查找主机

```json
{
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "output": ["hostid"],
        "selectTags": "extend",
        "evaltype": 0,
        "tags": [
            {
                "tag": "test",
                "value": "name",
                "operator": 1
            }
        ]
    },
    "auth": "f83e064cbaeed483200f347f5737a3a9",
    "id": 1
}
```



# 4.history

## 查看主机所有监控项历史数据

```json
{
    "jsonrpc": "2.0",
    "method": "history.get",
    "params": {
        "output": "extend",
        "history": 0,
        "sortfield": "clock",
        "sortorder": "DESC",
        "limit": 10
    },
    "auth": "f83e064cbaeed483200f347f5737a3a9",
    "id": 1
}
```



## 获取监控项的历史数据

```json
{
           "jsonrpc": "2.0",
           "method": "history.get",
           "params": {
               "output": "extend",
               "history": 0,
               "itemids": "23296",
               "sortfield": "clock",
               "sortorder": "DESC",
               "limit": 10
           },
           "auth": "038e1d7b1735c6a5436ee9eae095879e",
           "id": 1
       }
```





# 5.trend

## 获取监控项趋势数据

```
{
        "jsonrpc": "2.0",
        "method": "trend.get",
        "params": {
            "output": "extend",
            "itemids": itemid,
            "time_from": 1446199200,
            "time_till": 1646199200,
            "limit": "1"
        },
        "auth": token['result'],
        "id": 1
    }
```



# 6.item

## 通过键值模糊匹配

```json
{
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": ["itemid","name","key_"],
            "hostids": 10084,
            "search": { # 可以使用filter精确查找
                "key_": ["kernel.maxfiles","rabbitmq.node.disk_free"]
            },
            "searchByAny":true,   # 当使用search模糊查询多个时，需要加这个参数，否则只能会把所有参数之间用and连接
    		"startSearch":true # 使用右模糊匹配
        },
        "auth": "f83e064cbaeed483200f347f5737a3a9",
        "id": 1
    }
```



## 根据键值id查询

```json
{
           "jsonrpc": "2.0",
           "method": "item.get",
           "params":{
                "output":"extend",
                "itemids":"29688",
                "selectTags":"extend",
                "selectPreprocessing":"extend",
                "selectValueMap":"extend"
           },
           "auth": "f83e064cbaeed483200f347f5737a3a9",
           "id": 1
       }
```







# 7.event

## 根据触发器ID获取事件信息

```json
{
           "jsonrpc": "2.0",
           "method": "event.get",
           "params": {
           "output": "extend",
           "select_acknowledges": "extend",
           "selectTags": "extend",
           "selectSuppressionData": "extend",
           "objectids": "23392",
           "sortfield": ["clock", "eventid"],
           "sortorder": "DESC"
           },
           "auth": "f83e064cbaeed483200f347f5737a3a9",
           "id": 1
       }
```



## 根据时间段获取事件

```
{
           "jsonrpc": "2.0",
           "method": "event.get",
           "params": {
           "output": "extend",
           "time_from": "1349797228",
           "time_till": "1704679958",
           "sortfield": ["clock", "eventid"],
           "sortorder": "desc"
           },
           "auth": "f83e064cbaeed483200f347f5737a3a9",
           "id": 1
       }

# time_from表示的是创建时间，problem_time_from表示的是在这个时间区间处于问题状态
{
           "jsonrpc": "2.0",
           "method": "event.get",
           "params": {
           "output": "extend",
           "severities": [3,4],
           "sortfield": ["eventid"],
           "problem_time_from":1704237537,
           "problem_time_till":1704684639,
           "sortorder": "desc"
           },
           "auth": "f83e064cbaeed483200f347f5737a3a9",
           "id": 1
       }
```



## 根据事件ID范围

```json
{
           "jsonrpc": "2.0",
           "method": "event.get",
           "params": {
           "output": "extend",
           "eventid_from": "70",
           "eventid_till": "76",
           "sortfield": ["clock", "eventid"],
           "sortorder": "desc"
           },
           "auth": "f83e064cbaeed483200f347f5737a3a9",
           "id": 1
       }
```



## 根据严重级别

```json
{
           "jsonrpc": "2.0",
           "method": "event.get",
           "params": {
           "output": "extend",
           "severities": [3,4], # 0-5
           "sortfield": ["eventid"],
           "sortorder": "desc"
           },
           "auth": "f83e064cbaeed483200f347f5737a3a9",
           "id": 1
       }
```



# 8.proxy

```
{
    "jsonrpc": "2.0",
    "method": "proxy.get",
    "params": {
        "output": "extend",
        "selectInterface": "extend",
        "selectHosts":"extend"
    },
    "auth": "f83e064cbaeed483200f347f5737a3a9",
    "id": 1
}
```

