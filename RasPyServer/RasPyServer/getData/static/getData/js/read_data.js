
document.getElementById('file').onchange = function readDoc(){

  var file = this.files[0];

  var reader = new FileReader();
  var LOOP_counter = 1;
  var smoothie = new SmoothieChart({interpolation:'step',
                                    grid:{fillStyle:'#ffffff',
                                          verticalSections:0,
                                          millisPerLine:12000},
                                    yRangeFunction:myYRangeFunction,
                                    millisPerPixel:58,});
  var startT = 0;
  var cServer_Time = new Date().getTime()
  send_interval = 0;
  var clr_array = ["#80b1d3",
                   "#8dd3c7",
                   "#bebada",
                   "#ffffb3",
                   "#fb8072",
                   "#fdb462",
                   "#b3de69"]

  cTime = 10000000;

  smoothie.streamTo(document.getElementById("myChart_smooth"));

  reader.onload = function(progressEvent,send_interval){
    // Entire file
    // console.log(this.result);
    // document.getElementById("name").textContent(lines.length )

    // By lines
    var lines = this.result.split('\n');

    var var_list = get_vars(lines);
    var nice_txt_regex =  RegExp("(.*)List", '')
    //document.getElementById("p2").innerHTML = cServer_Time;
    if (LOOP_counter === 1) {

        var ul = document.getElementById("legend");
        for( var i = (var_list.length-2); i > -1 ; i-- ) { 
            varN = var_list[i].match(nice_txt_regex);
            var li = document.createElement("li");
            li.appendChild(document.createTextNode(varN[1]+'s'));
            ul.appendChild(li);     
        } 


    }


    
    var event_times_unfilt = get_var_strings(lines,var_list);
    var out = parse_ev_string(event_times_unfilt,var_list);

    event_times = out[0];
    event_counters = out[1];
    event_types = out[2]
    send_interval = event_times[event_times.length-1][0]
    startT2 = event_times[event_times.length-1].slice(-1) - send_interval
    document.getElementById("sendInt").innerHTML = send_interval
    document.getElementById("stTime").innerHTML = startT2
    //document.getElementById("p1").innerHTML = event_types


    //document.getElementById("name").innerHTML = Number(startT)+(LOOP_counter*100)/1000



    for (var evCt=0; evCt<(var_list.length-1); evCt++){
        evTs = event_times[evCt]
        if (evTs.some(in_bounds,thisArg=[Number(startT)+(LOOP_counter*100)/1000,Number(startT)+((LOOP_counter+1)*100)/1000]))
           {
            var temp = new TimeSeries();
            var t = new Date().getTime()//(startT+LOOP_counter*100)/1000
            temp.append(t,evCt)
            temp.append(t+1,1*.8+evCt)
            //arr.push(temp)
            smoothie.addTimeSeries(temp, {lineWidth:2.5,strokeStyle: clr_array[evCt]});
            //document.getElementById("name").innerHTML = 'hoooo'


        }
    }



    if ((LOOP_counter % 20) ===0  || (LOOP_counter === 1) ){
        draw_chart(var_list,event_counters)
    };

  };

    document.getElementById("sendInt").innerHTML = "SO FAR"

    reader.readAsText(file)
//    document.getElementById("p2").innerHTML = dat
    //document.getElementById("name").innerHTML = sendTimes[sendTimes.length-1]

    //send_interval = sendTimes[sendTimes.length-1][0]

    //startT = event_times[event_times.length-1] - send_interval


    setInterval(function() {
        if (LOOP_counter>1 && LOOP_counter<10){
            var dat = document.getElementById("sendInt").innerHTML

            //document.getElementById("p2").innerHTML = dat
            //document.getElementById("p1").innerHTML = document.getElementById("stTime").innerHTML 
            startT = document.getElementById("stTime").innerHTML 


        }
        if (LOOP_counter>5){
            sendTimes = reader.readAsText(file);
        }

        
        LOOP_counter += 1;

        }, 100);
};
function myYRangeFunction(range) {
  // TODO implement your calculation using range.min and range.max
  return {min: 0, max: 3};
}

function in_bounds(element){
    return ((element>this[0]) && (element<this[1]))
}

function lower_bound(element) {
  // checks whether an element is even
  return element>this ;
};

function upper_bound(element) {
  // checks whether an element is even
  return element<this ;
};

function isBigEnough(value) {
// stolen from https://stackoverflow.com/questions/13448799/return-array-elements-larger-than-a-number
    return function(element, index, array) {
        return (element >= value);
    }
}

function proc_file(lines){
    var var_list = get_vars(lines)
    //document.getElementById("p2").innerHTML = var_list;

    var event_times_unfilt = get_var_strings(lines,var_list);
    var out = parse_ev_string(event_times_unfilt,var_list);

    out2 = [out[0],out[1],var_list]
    return out

}

function parse_ev_string(event_times_unfilt,var_list) {

    // initialise variables
    var event_counters = [];
    var event_times = [];
    var event_types = [];

    for (var i=0; i<var_list.length; i++) {
        event_counters.push(0);
        event_times.push([]);
        event_types.push([]);
        }




    // Not actually extract the real event times


    var time_regex = RegExp("([0-9]{1,10}.[0-9]{1,10})", '');
    var type_regex = RegExp("[0-9]{1,10}.[0-9]{1,10}(.*)", '');

    for (var j=0; j<var_list.length; j++){

      var i = 0;
      for (var jj=0; jj <event_times_unfilt[j].length; jj++){
            temp = event_times_unfilt[j][jj].split("-");

            for (var jjj=0; jjj<temp.length; jjj++){

                var match = temp[jjj].match(time_regex);

                event_times[j].push(parseFloat(match[1]));
                event_types[j].push(temp[jjj].match(type_regex)[1])
                event_counters[j] += 1;

              }


        }
    }
    return [event_times, event_counters,event_types];
}

function get_var_strings(lines,var_list){


    // initialise variables
    var event_times_unfilt = [];

    for (var i=0; i<var_list.length; i++) {
        event_times_unfilt.push([]);
    }



    // run loop
    for (var j=0; j<var_list.length; j++){
        // var sound_regex = RegExp(var_list[j] + ":([0-9]+.*),",'')
        var sound_regex = RegExp(var_list[j] + ":([0-9]{1,10}.[0-9]{1,10}.*?(?=,))", '')

        // var sound_regex = /.*,sndList:([0-9]{1,10}.[0-9]{1,10}).*/;


        for(var line = 0; line < lines.length; line++){
            //var match = sound_regex.exec(lines[line]);
            var ll_upd = lines[line] +','

            var match = ll_upd.match(sound_regex)

            if (match != null) {

                if (match.length>=2){
                    for (var mch=1; mch<match.length; mch++){
                        event_times_unfilt[j].push(match[mch])

                     }
               }

        }



      }

   
    }
    return event_times_unfilt

}


function get_vars(lines) {

    var var_list = [];
    // This is the regex for finding stuff. Note to self (?<!a)b means b not preceded by a
    // + means 1 or more of something * means 0 or more of something2
    // purpose of the (?<!a)b here is to not split words e.g. lickList to kList
    var var_regex = /((?<![a-zA-Z])[a-zA-Z]+List):/mg;

    for(var line = 0; line < lines.length; line++){
            //var match = lines[line].match(var_regex);
            var match = var_regex.exec(lines[line])
            if (match != null) {
               //document.getElementById("p2").innerHTML = match

                for (var mch=1; mch<match.length; mch++){
                    if (!var_list.includes(match[mch])){
                      var_list.push(match[mch]);
                    }
                }

        }
    }
    
    return var_list

}

function draw_chart(nms,evs) {

    var ctx = document.getElementById("myChart");

    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: nms.slice(0, -1),
            datasets: [{
                label: '# of Events',
                data: evs.slice(0, -1),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)'
                    ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                  ],
                borderWidth: 1
            }]
        },
      maintainAspectRatio: false,
      showTooltips: false,

      options: {responsive: true,
                maintainAspectRatio: false,
                animation: false,



          scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero:true
                  }
              }]
          }
      }
  });    
} 
