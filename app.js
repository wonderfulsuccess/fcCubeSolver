require('cubejs/lib/solve.js');
var Cube = require('cubejs/lib/cube.js');

var Serialport = require('serialport'); // include the serialport library

 
var decode = {
    "U": 0,
    "U2": 1,
    "U'": 2,
    "F": 3,
    "F2": 4,
    "F'": 5,
    "L": 6,
    "L2": 7,
    "L'": 8,
    "D": 9,
    "D2": 10,
    "D'": 11,
    "B": 12,
    "B2": 13,
    "B'": 14,
    "R": 15,
    "R2": 16,
    "R'": 17
};

var steps = 0;
var arr = new Array();
var cube_status="";

var p = function(x) {
    console.log(x);
}

var port = new Serialport('COM11');

var cube_status = process.argv.slice(2);
p(cube_status);
p(process.argv);
// p(process.argv.slice(3));

var decodeString = function(str) {
    var i = 0;
    for (i = 0; i < str.length; i++) {
        if (str[i] == ' ') {
            steps++;
            arr.push(i);
        }
    }
    steps++;

    var buf = new Buffer(steps + 1);
    buf[0] = steps;
    buf[1] = decode[str.slice(0, arr[0])];
    for (i = 1; i < steps; i++) {
        var str_temp = (str.slice(arr[i - 1] + 1, arr[i]));
        buf[i + 1] = decode[str_temp];
    }
 
    return buf;
}

var colorToPosition = function(color){
    var char_color = color.split('');
    p(char_color.length);
    var i=0;
    for(i=0; i<char_color.length; i++){
        if(char_color[i] == 'Y') char_color[i] = 'U';
        if(char_color[i] == 'R') char_color[i] = 'F';
        if(char_color[i] == 'G') char_color[i] = 'R';
        if(char_color[i] == 'W') char_color[i] = 'D';
        if(char_color[i] == 'B') char_color[i] = 'L';
        if(char_color[i] == 'O') char_color[i] = 'B';
    }
    return char_color.join("");
}

var portData;

port.on('open', openPort);

function openPort(){
    p("Serial opened");
    // var cube = Cube.random();
    var cube = Cube.fromString(colorToPosition(cube_status.toString()));
    // p(colorToPosition(cube_status.toString()));
    //创建一个魔方实例
    // var cube = new Cube();

    // var cube = Cube.fromString("DUFRUBBBDBDURRDFUFULLFFFBDRDFUDDLRFLFBLBLUBRRLRRLBUDLU");
    p(cube.asString());

    Cube.initSolver();
    var road = cube.solve();
    p(road);
    var data = decodeString(road);
    var counter = 0;
    p(data.length);
    p(data);
    portData = data;

    function sendData() {
         port.write(portData);
         p(portData);
         p('Send done')
    }

    setTimeout(sendData, 2000);
}