# risloo-samples
## Samples list
### MBTI short form `MBTI9A`
### MBTI long form `MBTI93`
### Raven Standard `Raven9A`
### Raven Advanced `Raven93`
### Raven Colered `Raven9Q`

## Usage
`$serial.py [-type $type [raw, local, remote] -data $data [type data]] [-u run unittest]`
- examples
 - `MBTI9A.py -type local /home/risloo/samples/X1HQ74222.json`
 - `Raven93.py -type local /home/risloo/samples/X1HQ74222.json`
 
For running test, You must run `MBTI9A.py` [60 questions]  by the following options:
1. `MBTI9A.py -id [json file address (an absolute address not relative) in the local system or an url address or raw json data]  -it [type of your input ; for example : 'raw', 'local' , 'remote']`.

** for testing you can check this by the uplodaded json file :
`MBTI9A.py -id [X1HQ74222.json address in your local system] -it 'local' `.

2. If you want to run unittest for checking correctness :  `MBTI9A.py -id [json address] -it [input type] -u`.

*MBTI93.py [80 questions] is going to be prepared.
