
// global vars
var slData
var selectedClassProb = 'Modality';




// function to draw a single plot
function drawSubjPlot(subj, subjData){
    console.log('this subj: ' + subj);
    // for (s in subjData){
    //     console.log(d3.max(subjData[s]))
    // }
    //console.log(subjData)

    // set dimensions and margins for graph
    var margin = {top: 10, right: 30, bottom: 30, left: 40};
    var width = 960 - margin.left - margin.right;
    var height = 300 - margin.top - margin.bottom;

    // set the x/y scales
    var xScale = d3.scaleLinear()
        .domain([0,20])
        .range([0, width]);
    var yScale = d3.scaleLinear()
        .domain([0, 300])
        .range([height, 0]);

    // set up x-axis
    var xAxis = d3.axisBottom(xScale)
        .tickFormat(function(d,i){
            return d/20*100;
        }).ticks(2)

    var svg = d3.select("#subjPlots").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)

    //**** V1
    var v1_g = svg.append("g")
    v1_g.selectAll("rect")
        .data(subjData['V1'])
        .enter()
        .append("rect")
            .attr('class', 'V1')
            .attr('x', function(d,i){
                var newX = xScale(i)
                return newX;
            })
            .attr('y', function(d){
                return yScale(d);
            })
            .attr('width', xScale(.24))
            .attr('height', function(d){
                var newHeight = height-yScale(d);
                return newHeight
            });

    // V2 ---------------------
    var v2_g = svg.append("g")
    v2_g.selectAll("rect")
        .data(subjData['V2'])
        .enter()
        .append("rect")
            .attr('class', 'V2')
            .attr('x', function(d,i){
                var newX = xScale(i+.25)
                return newX;
            })
            .attr('y', function(d){
                return yScale(d);
            })
            .attr('width', xScale(.24))
            .attr('height', function(d){
                var newHeight = height-yScale(d);
                return newHeight
            });

    // V3 ---------------
    var v3_g = svg.append("g")
    v3_g.selectAll("rect")
        .data(subjData['V3'])
        .enter()
        .append("rect")
            .attr('class', 'V3')
            .attr('x', function(d,i){
                var newX = xScale(i+.5)
                return newX;
            })
            .attr('y', function(d){
                return yScale(d);
            })
            .attr('width', xScale(.24))
            .attr('height', function(d){
                var newHeight = height-yScale(d);
                return newHeight
            });

    // V4 ---------------
    var v3_g = svg.append("g")
    v3_g.selectAll("rect")
        .data(subjData['V4'])
        .enter()
        .append("rect")
            .attr('class', 'V4')
            .attr('x', function(d,i){
                var newX = xScale(i+.75)
                return newX;
            })
            .attr('y', function(d){
                return yScale(d);
            })
            .attr('width', xScale(.24))
            .attr('height', function(d){
                var newHeight = height-yScale(d);
                return newHeight
            });

    // set the chance line
    var chance = svg.append("rect")
        .attr('x1', xScale(10))
        .attr('y1', yScale(-10))
        .attr('x2', xScale(10))
        .attr('y2', yScale(height))
        .style('stroke', 'red');

    // draw the axis
    svg.append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .call(xAxis);


}



// parent function to call the drawing of each subject plot
function drawAllPlots(){
    // get the classification data for the selected problem
    classData = slData[selectedClassProb];

    // loop through each subject in the class data
    for (var subj in classData){
        drawSubjPlot(subj, classData[subj])
    }
}

// load data
d3.json('./_js/sl_allResults_hist.json', function(error, data){
    if (error) throw error;

    // load the data into the global var
    slData = data

    // now can call the plot
    drawAllPlots();
})



// generate the plots when first loaded



// handle on-click event of classProb selector
d3.select("#classProbSelector")
    .on('change', function(){
        selectedClassProb = d3.select(this).property('value');
        drawAllPlots();
    })
