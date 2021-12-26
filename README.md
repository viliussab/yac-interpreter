# yac-interpreter
This is a learning application that is able to interpret a custom made language. It was implemented using python3.9 and python library "sly".

## Prerequisites
In order to the program yourself one must:
- Have python version 3.9 installed in your device
- Download sly library using pip
``` pip install sly ```

## Running
You can run the program using the command line:  
```
cd <path-to-yac>
python3.9 yac.py <text/code-file>
```
## Datatypes
The interpreted language is statically-typed and features such data types:
- dbl
- int
- str
<!-- end of the list -->

it is possible to cast between datatypes: ```int(3.2)``` would convert to 3.2 to 3.

## Function declaration
The distinct feature of this prototyped language is its requirement to provide return types for the functions created. For example the code fragment:
```
func funk (int a) : (int b, int c) { 
	b = 3; 
	c = 4; 
	a = 312312321312;
}
```
Would initialize a function with a name *funk*:
-  its in parameter is *a* of type int
-  function returns two arguments: *b* and *c*, both of type int
<!-- end of the list -->

## Examples
You can analyse all of the features of the language furthermore by using the provided test.yac file. You can run it as follows
```
cd <path-to-repository>
python3.9 yac.py test.yac
```
You can also redirect the input so it prints into the file like this: 
```
python3.9 yac.py test.yac >> answers.txt
```
