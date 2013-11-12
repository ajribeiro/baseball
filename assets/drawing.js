var x=null,y=null;
var width = 700, height = 350; 
var xmargin = 150, ymargin = 75;
var navbarwid = 50;
var barwid = 20;
var mn=null,mx=null;
var mnx, mxx;
var dd;

function draw_nav_bars(data){

    var off = 75

    var r1 = svg.append('g').attr('class','nav')

    r1.append('rect')
        .attr('x',width+xmargin+10)
        .attr('y',ymargin+height/2-15-off)
        .attr('height',30)
        .attr('width',20)
        .style('fill','black')
        .style('stroke','none')

    r1.append('line')
        .attr('x1',width+xmargin+15)
        .attr('y1',ymargin+height/2-15-off)
        .attr('x2',width+xmargin+23)
        .attr('y2',ymargin+height/2-off)
        .attr('class','arr')

    r1.append('line')
        .attr('x1',width+xmargin+15)
        .attr('y1',ymargin+height/2+15-off)
        .attr('x2',width+xmargin+23)
        .attr('y2',ymargin+height/2-off)
        .attr('class','arr')

    r1.on('click',function(){
        datind++;
        update_bars(data)
    })


    var l1 = svg.append('g').attr('class','nav')

    l1.append('rect')
        .attr('x',width+xmargin+10)
        .attr('y',ymargin+height/2-18-off/2-3)
        .attr('height',30)
        .attr('width',20)
        .style('fill','black')
        .style('stroke','none')

    l1.append('line')
        .attr('x1',width+xmargin+15)
        .attr('y1',ymargin+height/2-off/2+3)
        .attr('x2',width+xmargin+23)
        .attr('y2',ymargin+height/2-off/2-15+3)
        .attr('class','arr')


    l1.append('line')
        .attr('x1',width+xmargin+15)
        .attr('y1',ymargin+height/2-off/2+3)
        .attr('x2',width+xmargin+23)
        .attr('y2',ymargin+height/2-off/2+15+3)
        .attr('class','arr')

    l1.on('click',function(){
        datind--;
        if(datind < 0) datind = 0;
        update_bars(data)
    })

    var r2 = svg.append('g').attr('class','nav')

    r2.append('rect')
        .attr('x',width+xmargin+10)
        .attr('y',ymargin+height/2-15+off/2-3)
        .attr('height',30)
        .attr('width',30)
        .style('fill','black')
        .style('stroke','none')

    r2.append('line')
        .attr('x1',width+xmargin+15)
        .attr('y1',ymargin+height/2-15+off/2-3)
        .attr('x2',width+xmargin+23)
        .attr('y2',ymargin+height/2+off/2-3)
        .attr('class','arr')

    r2.append('line')
        .attr('x1',width+xmargin+15)
        .attr('y1',ymargin+height/2+15+off/2-3)
        .attr('x2',width+xmargin+23)
        .attr('y2',ymargin+height/2+off/2-3)
        .attr('class','arr')

    r2.append('line')
        .attr('x1',width+xmargin+15+8)
        .attr('y1',ymargin+height/2-15+off/2-3)
        .attr('x2',width+xmargin+23+8)
        .attr('y2',ymargin+height/2+off/2-3)
        .attr('class','arr')

    r2.append('line')
        .attr('x1',width+xmargin+15+8)
        .attr('y1',ymargin+height/2+15+off/2-3)
        .attr('x2',width+xmargin+23+8)
        .attr('y2',ymargin+height/2+off/2-3)
        .attr('class','arr')

    r2.on('click',function(){
        datind += nbars;
        update_bars(data)
    })

    var l2 = svg.append('g').attr('class','nav')

    l2.append('rect')
        .attr('x',width+xmargin+10)
        .attr('y',ymargin+height/2-15+off)
        .attr('height',30)
        .attr('width',30)
        .style('fill','black')
        .style('stroke','none')

    l2.append('line')
        .attr('x1',width+xmargin+15)
        .attr('y1',ymargin+height/2+off)
        .attr('x2',width+xmargin+23)
        .attr('y2',ymargin+height/2+off-15)
        .attr('class','arr')

    l2.append('line')
        .attr('x1',width+xmargin+15)
        .attr('y1',ymargin+height/2+off)
        .attr('x2',width+xmargin+23)
        .attr('y2',ymargin+height/2+off+15)
        .attr('class','arr')

    l2.append('line')
        .attr('x1',width+xmargin+15+8)
        .attr('y1',ymargin+height/2+off)
        .attr('x2',width+xmargin+23+8)
        .attr('y2',ymargin+height/2+off-15)
        .attr('class','arr')

    l2.append('line')
        .attr('x1',width+xmargin+15+8)
        .attr('y1',ymargin+height/2+off)
        .attr('x2',width+xmargin+23+8)
        .attr('y2',ymargin+height/2+off+15)
        .attr('class','arr')

    l2.on('click',function(){
        datind = datind-nbars;
        if(datind < 0){
            datind = 0;
        }
        update_bars(data)
    })
}

function get_scale(data){

    if(type == 'seas'){
        mx = Math.max.apply(Math,data.seasons.map(function(o){return o[stat];}))
        mn = Math.min.apply(Math,data.seasons.map(function(o){return o[stat];}))
    } else if(type == 'car'){
        mx = Math.max.apply(Math,data.careers.map(function(o){return o[stat];}))
        mn = Math.min.apply(Math,data.careers.map(function(o){return o[stat];}))
    }

    x = d3.scale.linear()
        .domain([1+datind,datind+nbars+1])
        .range([xmargin,width+xmargin])

    y = d3.scale.linear()
        .domain([mn,mx])
        .range([height+ymargin,ymargin])
}

function set_tooltips(){

    d3.selectAll(".bar")
        .on('mouseover',function(d,i){
            d3.select('#'+d.hsh).style('stroke','yellow')
            var g = svg.append('g')
                        .attr("id", 'n'+d.name[0])

            var ibox = g.append('rect')
                .attr('class','infobox')
                .attr("x",function(a,b){
                    return x(i+1+datind);
                })
                .attr("y",function(a) {
                    return y(d[stat])-75;
                })
                .attr('width',250)
                .attr('height',50)
                .style('fill','black')

            g.append('text')
                .text(function(){
                    if(type == 'seas')
                        return d.name+' '+d.year+', '+stat+': '+d[stat]
                    else
                        return d.name+', '+stat+': '+d[stat]

                })
                .attr('class','infotext')
                .attr('x',function(){
                    return x(i+1+datind)+125;
                })
                .attr('y',function(){
                    return y(d[stat])-45;
                })
        })
        .on("mouseout", function(d){
            d3.select('#'+d.hsh).style('stroke','white')
            d3.select("#n" + d.name[0])
                .remove();
        });
        


}

function draw_bar_x_axis(){

    d3.selectAll('#xaxis').remove()
    var x_axis = d3.svg.axis().orient('top')
        .scale(x)
        .tickValues([datind+1,datind+6,datind+11,datind+16,datind+21,datind+26]);

    d3.select('#bchart')
        .append('g')
        .attr('class','x axis')
        .attr('id','xaxis')
        .attr("transform", "translate(0," + (ymargin) + ")")
        .call(x_axis);

    d3.selectAll('#xtitle').remove()
    svg.append('text')
        .attr('x',xmargin+width/2)
        .attr('y',ymargin-40)
        .attr('id','xtitle')
        .style('text-align','right')
        .text('Rank')

}

function draw_y_axis(){

    d3.selectAll('#yaxis').remove()

    var y_axis = d3.svg.axis().scale(y).orient('left');
    d3.select('#bchart')
        .append('g')
        .attr('id','yaxis')
        .attr('class','y axis')
        .attr("transform", "translate(" + xmargin + ',0)')
        .call(y_axis);


    d3.selectAll('#ytitle').remove()
    svg.append('text')
        .text(stat)
        .attr('x',xmargin-90)
        .attr('y',ymargin+height/2)
        .attr('id','ytitle')
        .style('text-align','right')
        .attr('transform','rotate(-90,'+xmargin-30+','+ymargin+height/2+')')

}
function update_bars(data){

    if(type == 'seas')
        dd = data.seasons.sort(dynamicSort(stat,'year','name')).slice(datind,datind+nbars)
    else if(type == 'car')
        dd = data.careers.sort(dynamicSort(stat,'name')).slice(datind,datind+nbars)

    get_scale(data)


    var rect = svg.selectAll(".bar")
    
    rect.data(dd)

    rect.transition()
        .duration(750)
        .attr('x',function(d,i){
            return x(i+1+datind);
        })
        .attr('y',function(d) { 
            return y(d[stat]); 
        })
        .attr('width',barwid)
        .attr('height',function(d){
            return height + ymargin- y(d[stat]);
        })
        .style('fill',function(d){
            var c = intToARGB(hashCode(d.name))
            c = c.toString()
            c = c.slice(0,3)
            return '#'+c
        })
        .attr('id',function(d){return d.hsh})


    var names = d3.selectAll('.pname')

    if(names[0].length == 0){
        var names = svg.selectAll('text.pname')
            .data(dd)
            .enter()
            .append('text')
    } else
        names.data(dd)

    names.attr('class','pname')
        .transition()
        .duration(750)
        .attr('x',function(d,i){
            return x(i+1.75+datind);
        })
        .attr('y',height+ymargin+5)
        .style('stroke','white')
        .style('fill','white')
        .text(function(d){
            if(type === 'seas')
                return d.name+' '+d.year;
            else
                return d.name
        })
        .attr("transform", function(d,i) {
                return 'rotate(-90,'+x(i+1.75+datind)+','+(ymargin+height+5)+')'
        });

    draw_bar_x_axis()

    set_tooltips()
}

function draw_leaders(data){

    d = data

    d3.select('#bchart').remove()

    svg = d3.select("#chart")
        .append("svg")
        .attr("class", "barchart")
        .attr('id','bchart')
        .attr('height','1000')

    var dd = new Array(nbars)
    for(var i=0; i<nbars; i++) dd[i] = 0;

    get_scale(data)
    var bars = svg.selectAll("rect.bar")
        .data(dd)
        .enter()
        .append("rect")
        .attr("class","bar")
        .attr('x',function(d,i){
            return x(i+1+datind);
        })
        .attr('y',function(d) { 
            return ymargin+height; 
        })
        .attr('width',barwid)
        .attr('height',function(d){
            return 0;
        })

    update_bars(data)
    draw_y_axis()
    draw_nav_bars(data)
    draw_key(data)
    var box = svg.append('rect')
        .attr('x',xmargin)
        .attr('y',ymargin)
        .attr('height',height)
        .attr('width',width)
        .style('fill','none')
        .style('stroke','white')
    
}

function draw_key_player(data){

    var key_boxes = svg.selectAll("rect")
        .data(stats)
        .enter()
        .append("rect")
        .attr("class",function(d){return d.replace('%','').replace('+','')})
        .attr("id",function(d){return d.replace('%','').replace('+','')+'_box'})
        .attr('x',xmargin+width+60)
        .attr('y',function(d,i){
            return ymargin+i*25;
        })
        .attr('height',15)
        .attr('width',15)
        .style('stroke','white')
        .style('stroke-width',2)
        .style('cursor','pointer')
        .style('fill',function(d){
            if(pstats.indexOf(d) > -1){
                return pcols[d.replace('%','').replace('+','')]
            }
            else{
                return 'black'
            }
        })

    key_boxes.on('click',function(d){
        if(pstats.indexOf(d) == -1){
            pstats.push(d)
            d3.select(this).style('fill',pcols[d.replace('%','').replace('+','')])
            draw_stat(data,d)
        } else{
            pstats.splice(pstats.indexOf(d),1)
            d3.select(this).style('fill','black')
            svg.select('#'+'c'+d.replace('%','').replace('+','')).remove()
        }
    })

    var key_names = svg.selectAll(".key_name")
        .data(stats)
        .enter()
        .append("text")
        .attr("class","key_name")
        .attr("id",function(d){return d.replace('%','').replace('+','')+'_name'})
        .attr('x',xmargin+width+60+25)
        .attr('y',function(d,i){
            return ymargin+i*25+12;
        })
        .text(function(d){return d})
        .on('mouseover',function(d){
            ddd = d
            d = d.replace('%','').replace('+','')
            d3.select('#'+d+'_name').attr('class','key_name_hi')
            var g = svg.append('g')
                        .attr('id',d+'_infobox')

            var ibox = g.append('rect')
                .attr('class','infobox')
                .attr('x',function(){
                    return +d3.select('#'+d+'_name').attr('x')+50
                })
                .attr('y',function(){
                    return +d3.select('#'+d+'_name').attr('y')-30
                })
                .attr('width',200)
                .attr('height',50)

            g.append('text')
                .text(defs[ddd])
                .attr('class','infotext')
                .attr('x',function(){
                    return +d3.select('#'+d+'_name').attr('x')+150
                })
                .attr('y',function(){
                    return +d3.select('#'+d+'_name').attr('y')
                })
        })
        .on('mouseout',function(d){
            d = d.replace('%','').replace('+','')
            d3.select('#'+d+'_infobox').remove()
            d3.select('#'+d+'_name').attr('class','key_name')

        })
}

function draw_key(data){
// HR,R,RBI,SB,BB%,K%,ISO,BABIP,AVG,OBP,SLG,wOBA,wRC+,WAR,

    var key_boxes = svg.selectAll(".key_box")
        .data(stats)
        .enter()
        .append("rect")
        .attr("class","key_box")
        .attr("id",function(d){return d+'_box'})
        .attr('x',xmargin+width+60)
        .attr('y',function(d,i){
            return ymargin+i*25;
        })
        .attr('height',15)
        .attr('width',15)
        .style('fill',function(d){
            if(d == stat){
                return 'white'
            }
            else{
                return 'black'
            }
        })

    key_boxes.on('click',function(d){
        datind = 0;
        stat = d;
        get_scale(data)
        draw_y_axis();
        svg.selectAll('.key_box')
            .style('fill',function(d){
                if(d == stat){
                    return 'white'
                }
                else{
                    return 'black'
                }
            })
        update_bars(data)
        
    })

    var key_names = svg.selectAll(".key_name")
        .data(stats)
        .enter()
        .append("text")
        .attr("class","key_name")
        .attr("id",function(d){return d.replace('%','').replace('+','')+'_name'})
        .attr('x',xmargin+width+60+25)
        .attr('y',function(d,i){
            return ymargin+i*25+12;
        })
        .text(function(d){return d})
        .on('mouseover',function(d){
            dd = d
            d = d.replace('%','').replace('+','')
            d3.select('#'+d+'_name').attr('class','key_name_hi')
            var g = svg.append('g')
                        .attr('id',d+'_infobox')

            var ibox = g.append('rect')
                .attr('class','infobox')
                .attr('x',function(){
                    return +d3.select('#'+d+'_name').attr('x')+50
                })
                .attr('y',function(){
                    return +d3.select('#'+d+'_name').attr('y')-30
                })
                .attr('width',200)
                .attr('height',50)

            g.append('text')
                .text(defs[dd])
                .attr('class','infotext')
                .attr('x',function(){
                    return +d3.select('#'+d+'_name').attr('x')+150
                })
                .attr('y',function(){
                    return +d3.select('#'+d+'_name').attr('y')
                })
        })
        .on('mouseout',function(d){
            d = d.replace('%','').replace('+','')
            d3.select('#'+d+'_infobox').remove()
            d3.select('#'+d+'_name').attr('class','key_name')

        })
}

function draw_player(data){

    dd = data['seasons']

    d3.select('#bchart').remove()

    svg = d3.select("#chart")
        .append("svg")
        .attr("class", "barchart")
        .attr('id','bchart')
        .attr('height','1000')

    dd = dd.filter(function(d){return d.lname == player})
    dd = dd.sort(dynamicSort2('year')).slice(datind,datind+nbars)


    for(var i=0; i<pstats.length; i++){

        draw_stat(data,pstats[i])

        var names = svg.selectAll('text.pname')
            .data(dd)
            .enter()
            .append('text')
            .attr('class','pname')
            .transition()
            .duration(750)
            .attr('x',function(d){
                return x(d['year']);
            })
            .attr('y',height+ymargin+5)
            .style('stroke','white')
            .style('fill','white')
            .text(function(d){
                 return d.year+', Age '+d.Age;
            })
            .attr("transform", function(d,i) {
                    return 'rotate(-90,'+x(d['year'])+','+(ymargin+height+5)+')'
            });

        draw_key_player(dd);

    }

    var box = svg.append('rect')
        .attr('x',xmargin)
        .attr('y',ymargin)
        .attr('height',height)
        .attr('width',width)
        .style('fill','none')
        .style('stroke','white')
}

function draw_stat(data,stat){

    mxx = Math.max.apply(Math,dd.map(function(o){return o['year'];}))
    mnx = Math.min.apply(Math,dd.map(function(o){return o['year'];}))

    mx = Math.max.apply(Math,dd.map(function(o){return o[stat];}))
    mn = Math.min.apply(Math,dd.map(function(o){return o[stat];}))

    x = d3.scale.linear()
        .domain([mnx,mxx])
        .range([xmargin,width+xmargin])

    y = d3.scale.linear()
        .domain([mn,mx])
        .range([height+ymargin,ymargin])


    var g = svg.append('g')
        .attr('id','c'+stat.replace('%','').replace('+',''))

    var circs = g.selectAll('circle.'+stat.replace('%','').replace('+',''))
        .data(dd)
        .enter()
        .append('circle')
        .attr('class',stat.replace('%','').replace('+',''))
        .attr('cx',function(d){
            return x(d['year'])
        })
        .attr('cy',function(d){
            return y(d[stat])
        })
        .attr('r',1)
        .on('mouseover',function(d){
            d3.select(this).attr('r',10)
           var yy = d3.select(this).attr('cy')
            var g = svg.append('g')
                .attr("id", 'n'+d.year+''+stat)

            g.append('rect')
                .attr('class','infobox')
                .attr("x",function(){
                    return x(d['year'])
                })
                .attr("y",function() {
                    return yy-75;
                })
                .attr('width',250)
                .attr('height',50)
                .style('fill','black')

            g.append('text')
                .text(d.year+', '+stat+': '+d[stat])
                .attr('class','infotext')
                .attr('x',function(){
                    var xx = x(d['year'])+125
                    return xx;
                })
                .attr('y',function(){
                    return yy-45
                })
        })
        .on('mouseout',function(d){
            d3.select(this).attr('r',5)
            d3.select("#n" + d.year+''+stat).remove();
        })

    circs.transition()
        .delay(function(d,i){
            return (dd.length-i)*75;
        })
        .attr('r',5)

    var line = d3.svg.line()
        .x(function(d){return x(d['year'])})
        .y(function(d){return y(d[stat])})

    g.append('path')
        .attr('d',line(dd))
        .attr('class',stat.replace('%','').replace('+',''))
        .style('fill','none')
}