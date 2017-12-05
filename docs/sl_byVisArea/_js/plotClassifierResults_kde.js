
// global vars
var slData
var selectedClassProb = 'Modality';

// set dimensions and margins for graph
var margin = {top: 10, right: 30, bottom: 30, left: 40};
var width = 460 - margin.left - margin.right;
var height = 250 - margin.top - margin.bottom;

// function to draw a single plot
function drawSubjPlot(subj, subjData){
    console.log('this subj: ' + subj);

    // set the x/y scales
    var xScale = d3.scaleLinear()
        .domain([0,100])
        .range([0, width]);
    var yScale = d3.scaleLinear()
        .domain([0, .1])
        .range([height, 0]);

    // set up x-axis
    var xAxis = d3.axisBottom(xScale)
                .ticks(2)

    var svg = d3.select("#subjPlots").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("id", 'subj' + subj)

    //**** V1
    var v1_data = subjData['V1']
    var v1_n = v1_data.length
    var v1_bins = d3.histogram().domain(xScale.domain())
            .thresholds(40)(v1_data);
    var v1_density = kernelDensityEstimator(kernelEpanechnikov(7), xScale.ticks(40))(v1_data);
    var v1_g = svg.append("g")
        .attr('class', 'V1')
    v1_g.append("path")
      .attr('class', 'V1_path')
      .datum(v1_density)
      .attr("fill", "none")
      .attr("stroke-width", 2.5)
      .attr("stroke-linejoin", "round")
      .attr("d",  d3.line()
          .curve(d3.curveBasis)
          .x(function(d) {
              return xScale(d[0]);
          })
          .y(function(d) {
              return yScale(d[1]);
          }));

    // V2 ---------------------
    var v2_data = subjData['V2']
    var v2_n = v2_data.length
    var v2_bins = d3.histogram().domain(xScale.domain())
            .thresholds(40)(v2_data);
    var v2_density = kernelDensityEstimator(kernelEpanechnikov(7), xScale.ticks(40))(v2_data);
    var v2_g = svg.append("g")
        .attr('class', 'v2')
    v2_g.append("path")
      .attr('class', 'V2_path')
      .datum(v2_density)
      .attr("fill", "none")
      .attr("stroke-width", 2.5)
      .attr("stroke-linejoin", "round")
      .attr("d",  d3.line()
          .curve(d3.curveBasis)
          .x(function(d) {
              return xScale(d[0]);
          })
          .y(function(d) {
              return yScale(d[1]);
          }));

    // V3 ---------------
    var v3_data = subjData['V3']
    var v3_n = v3_data.length
    var v3_bins = d3.histogram().domain(xScale.domain())
            .thresholds(40)(v3_data);
    var v3_density = kernelDensityEstimator(kernelEpanechnikov(7), xScale.ticks(40))(v3_data);
    var v3_g = svg.append("g")
        .attr('class', 'v3')
    v3_g.append("path")
      .attr('class', 'V3_path')
      .datum(v3_density)
      .attr("fill", "none")
      .attr("stroke-width", 2.5)
      .attr("stroke-linejoin", "round")
      .attr("d",  d3.line()
          .curve(d3.curveBasis)
          .x(function(d) {
              return xScale(d[0]);
          })
          .y(function(d) {
              return yScale(d[1]);
          }));

    // V4 ---------------
    var v4_data = subjData['V4']
    var v4_n = v4_data.length
    var v4_bins = d3.histogram().domain(xScale.domain())
            .thresholds(40)(v4_data);
    var v4_density = kernelDensityEstimator(kernelEpanechnikov(7), xScale.ticks(40))(v4_data);
    var v4_g = svg.append("g")
        .attr('class', 'v4')
    v4_g.append("path")
      .attr('class', 'V4_path')
      .datum(v4_density)
      .attr("fill", "none")
      .attr("stroke-width", 2.5)
      .attr("stroke-linejoin", "round")
      .attr("d",  d3.line()
          .curve(d3.curveBasis)
          .x(function(d) {
              return xScale(d[0]);
          })
          .y(function(d) {
              return yScale(d[1]);
          }));

    // set the chance line
    var chance = svg.append("line")
        .attr('id', 'chanceLine')
        .attr('x1', function(){
            if (selectedClassProb.substr(0,4).toLowerCase() == 'stim'){
                var chanceX = xScale(12.5);
            } else {
                var chanceX = xScale(50);
            }
            return chanceX
        })
        .attr('y1', yScale(0))
        .attr('x2', function(){
            if (selectedClassProb.substr(0,4).toLowerCase() == 'stim'){
                var chanceX = xScale(12.5);
            } else {
                var chanceX = xScale(50);
            }
            return chanceX
        })
        .attr('y2', yScale(.07))
        .style('stroke', 'white')
        .style('stroke-dasharray', ('3,2,3'));

    // Draw the subject
    svg.append('text')
        .attr('class','subjText')
        .attr('x', xScale(85))
        .attr('y', yScale(.06))
        .html(subj);


    // draw the axis
    svg.append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .call(xAxis);
}


// Kernel Density Estimators
function kernelDensityEstimator(kernel, X) {
  return function(V) {
    return X.map(function(x) {
      return [x, d3.mean(V, function(v) { return kernel(x - v); })];
    });
  };
}

function kernelEpanechnikov(k) {
  return function(v) {
    return Math.abs(v /= k) <= 1 ? 0.75 * (1 - v * v) / k : 0;
  };
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
d3.json('./_js/sl_allResults_kde.json', function(error, data){
    if (error) throw error;

    // load the data into the global var
    slData = data

    // now can call the plot
    drawAllPlots();
    updateClassifierLabel();

})


function updateAllPlots(){
    classData = slData[selectedClassProb];
    for (var subj in classData){
        console.log
        updateSubjPlot(subj, classData[subj])
    }
}


function updateSubjPlot(subj, subjData){
    var xScale = d3.scaleLinear()
        .domain([0,100])
        .range([0, width]);
    var yScale = d3.scaleLinear()
        .domain([0, .1])
        .range([height, 0]);

    var svg = d3.select("#subj" + subj)

    // V1 ----------------------------
    var v1_data = subjData['V1']
    var v1_n = v1_data.length
    var v1_bins = d3.histogram().domain(xScale.domain())
            .thresholds(40)(v1_data);
    var v1_density = kernelDensityEstimator(kernelEpanechnikov(7), xScale.ticks(40))(v1_data);
    var v1_path = svg.select('.V1_path')
      .datum(v1_density)
      .transition()
      .duration(500)
      .attr("d",  d3.line()
          .curve(d3.curveBasis)
          .x(function(d) {
              return xScale(d[0]);
          })
          .y(function(d) {
              return yScale(d[1]);
          }));

    // V2 ----------------------------
    var v2_data = subjData['V2']
    var v2_n = v2_data.length
    var v2_bins = d3.histogram().domain(xScale.domain())
            .thresholds(40)(v2_data);
    var v2_density = kernelDensityEstimator(kernelEpanechnikov(7), xScale.ticks(40))(v2_data);
    var v2_path = svg.select('.V2_path')
      .datum(v2_density)
      .transition()
      .duration(500)
      .attr("d",  d3.line()
          .curve(d3.curveBasis)
          .x(function(d) {
              return xScale(d[0]);
          })
          .y(function(d) {
              return yScale(d[1]);
          }));

      // v3 ----------------------------
      var v3_data = subjData['V3']
      var v3_n = v3_data.length
      var v3_bins = d3.histogram().domain(xScale.domain())
              .thresholds(40)(v3_data);
      var v3_density = kernelDensityEstimator(kernelEpanechnikov(7), xScale.ticks(40))(v3_data);
      var v3_path = svg.select('.V3_path')
        .datum(v3_density)
        .transition()
        .duration(500)
        .attr("d",  d3.line()
            .curve(d3.curveBasis)
            .x(function(d) {
                return xScale(d[0]);
            })
            .y(function(d) {
                return yScale(d[1]);
            }));

        // V4 ----------------------------
        var v4_data = subjData['V4']
        var v4_n = v4_data.length
        var v4_bins = d3.histogram().domain(xScale.domain())
                .thresholds(40)(v4_data);
        var v4_density = kernelDensityEstimator(kernelEpanechnikov(7), xScale.ticks(40))(v4_data);
        var v4_path = svg.select('.V4_path')
          .datum(v4_density)
          .transition()
          .duration(500)
          .attr("d",  d3.line()
              .curve(d3.curveBasis)
              .x(function(d) {
                  return xScale(d[0]);
              })
              .y(function(d) {
                  return yScale(d[1]);
              }));

       // chance line
       // set the chance line
       var chance = svg.select("#chanceLine")
           .transition()
           .duration(500)
           .attr('x1', function(){
               if (selectedClassProb.substr(0,4).toLowerCase() == 'stim'){
                   var chanceX = xScale(12.5);
               } else {
                   var chanceX = xScale(50);
               }
               return chanceX
           })
           .attr('x2', function(){
               if (selectedClassProb.substr(0,4).toLowerCase() == 'stim'){
                   var chanceX = xScale(12.5);
               } else {
                   var chanceX = xScale(50);
               }
               return chanceX
           })



}

function updateClassifierLabel(){
    if (selectedClassProb == 'Modality'){
        d3.select("#classLabel").text('Pics vs Words')
    } else if (selectedClassProb == 'Category'){
        d3.select("#classLabel").text('Dwellings vs Tools')
    } else if (selectedClassProb == 'categoryWords'){
        d3.select("#classLabel").text('Dwellings vs Tools (words only)')
    } else if (selectedClassProb == 'categoryPics'){
        d3.select("#classLabel").text('Dwellings vs Tools (pics only)')
    } else if (selectedClassProb == 'Stimuli'){
        d3.select("#classLabel").text('Unique stimulus')
    } else if (selectedClassProb == 'stimuliWords'){
        d3.select("#classLabel").text('Unique stimulus (words only)')
    } else if (selectedClassProb == 'stimuliPics'){
        d3.select("#classLabel").text('Unique stimulus (pics only)')
    }
}


// handle on-click event of classProb selector
d3.select("#classProbSelector")
    .on('change', function(){
        selectedClassProb = d3.select(this).property('value');

        // rebind all of the data
        updateAllPlots();
        updateClassifierLabel();

    })
