import React, { useEffect, useState, useMemo } from "react";
import Highcharts from "highcharts";
import HighchartsData from "highcharts/modules/data";
import HighchartsExporting from "highcharts/modules/exporting";
import HighchartsHeatmap from "highcharts/modules/heatmap";
import HighchartsTreeChart from "highcharts/modules/treemap";
import HighchartsReact from "highcharts-react-official";
import data from "./sectionPrice.json"
import { withTheme } from "@emotion/react";

HighchartsData(Highcharts);
HighchartsHeatmap(Highcharts);
HighchartsTreeChart(Highcharts);
HighchartsExporting(Highcharts);

var originalColor
// option for treemap
const createChartOptions = (points) => ({
  series: [
    {
      type: "treemap",
      layoutAlgorithm: "squarified",
      
      allowDrillToNode: true,
      animation: true,
      dataLabels: {
        enabled: true,
      },
      levelIsConstant: true,
      levels: [{
                level: 1,
                dataLabels: {
                  enabled: true,
                  inside: false,
                  y: 10,
                  allowOverlap: false,
                  crop: false,
                  backgroundColor: 'white',
                  filter: {
                    property: 'value',
                    operator: '>',
                    value: 10000000
                  },
                  align: "left",
                  color: 'black'
                },
                borderWidth: 2
              },
              {
                level: 2,
                dataLabels: {
                   enabled: true,
                   allowOverlap: false,
                   filter: {
                    property: 'value',
                    operator: '>',
                    value: 3000000
                  },
                 },
                 
                borderWidth: 1,
                 
              }
      ],
      data: points
    }
  ],
  subtitle: false,
  title: false,
  exporting: false,
  credits: false,
  chart:{
    height: 300
  }
});

// code start from here
function TreeMap() {
  const [points, setPoints] = useState([]);
  const chartOptions = useMemo(() => createChartOptions(points), [points]);
  // useEffect will be used when having the endpoint API
  useEffect(() => {
    var industryI = 0,
        industry,
        industryVal,
        idx
     
    for (industry in data) {
      industryVal = 0
      for(idx in data[industry]){
        var col ="#198754"
        var val = data[industry][idx].priceClose - data[industry][idx].priceOpen
        if (val < 0) {
          col = "#dc3545"
          val = -val
        }
        industryVal += data[industry][idx].totalVolume
        points.push({
          id: idx,
          name: data[industry][idx].symbol,
          change: val,
          parent: 'industry_' + industryI,
          color: col,
          value: data[industry][idx].totalVolume
        })
      }  
      points.push({
        id : 'industry_' + industryI,
        name: industry,
        color: "#f6d2d0",
        value: industryVal
      })
      industryI++
    }
    setPoints(points)
  })
  
  return (
    <div>
      <HighchartsReact highcharts={Highcharts} options={chartOptions} />
    </div>
  );
}


export default TreeMap;

