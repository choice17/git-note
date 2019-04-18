## PROTOBUF

- **[Sample](./protobuf/test_main.py)** 

## Install protobuf compiler  
```
sudo apt-get install protobuf-compiler
```

## src  
SRC_DIR=`pwd`  

## dst   
DST_DIR=`pwd`  

## compile .proto  
protoc -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/  {target_package}.proto  


## tag

> proto version 2 or 3
```
syntax = "proto2" 
```

> package name (not really necessary for python language)
```
package <tutorial> 
```

> message as class  
```
// define message type
message <MSG> {
	// basic definition
	required string name = 1;
	required int32 id = 2;
	optional string addr = 3;

	// Support enum
	enum EmploymentType {
		IT = 0;
		MKT = 1;
		RD = 2;
	}

	// Sub class inside <MSG class>
	message <Company> {
		required string number = 1;
		optional EmploymentType type = 2 [default = IT];
	}

	repeated Company companies = 4;
}

message <MsgBook> {
  repeated MSG msg = 1;
}

* required：cannot be missed  
* optional：can be ignored or optional existence   
* repeated：allow repeat or non-exist

```


## API   

1. Import  
```
import demo_pb2
```

2. Init object  
```
msg = demo_pb2.MsgBook()
```

3. Api  func
```
# <model>.<Msg class>.add()
thisMsg = msg.MSG.add()
thisMsg.name = "T C YU"
thisMsg.id = 147

# Write <object>.SerializeToString()
pb_file = "demo.pb"
with open(pb_file, "wb") as f:
  f.write(thisMsg.SerializeToString())

# Read 
msgbook = demo_pb2.MsgBook()
with open(pb_file, "rb") as f:
  msgbook.ParseFromString(f.read())

```


