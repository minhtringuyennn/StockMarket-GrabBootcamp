import React from "react";
import res  from "./todayPrice.json"
import { Link } from "react-router-dom";

function TwoHalfBarChart(){
  // data processing
  // take symbol having highest totalForeignValue
  // take symbol having lowest totalForeignValue
  // take 10 symbol having highest totalForeignValue
  // take 10 symbol having lowest totalForeignValue
  const max_value_green = res[0].totalForeignValue;
  const max_value_red = res[res.length -1].totalForeignValue;
  const data_red = res.slice(-10).reverse().map(item => ({
    ...item,
    value: item.totalForeignValue * 100 / max_value_red
  }));;
  const data_green = res.slice(0,10).map(item => ({
    ...item,
    value: item.totalForeignValue * 100 / max_value_green
  }));
  // format data to show chart
  const list_green = data_green.map((item) => 
    <div className="d-flex flex-row-reverse ">
      <div className="col-4 text-end">
        <Link to={`/company/${item.symbol}`}>
          {item.symbol}
        </Link>
      </div>
      <div className="col-8 flex-col-reverse d-flex flex-row-reverse">
        <div className="bg-success my-auto rounded" style={{width:item.value, height:15}}></div>
      </div>
    </div>    
  )
  const list_red = data_red.map((item) => 
    <div className="d-flex">
      <div className="col-4">
        <Link to={`/company/${item.symbol}`}>
          {item.symbol}
        </Link>
      </div>
      <div className="col-8 flex-col-reverse d-flex flex-row">
        <div className="bg-danger my-auto rounded" style={{width:item.value, height:15}}></div>
      </div>
    </div>    
  )
  const list = (<div className="row" style={{maxWidth: 400}}>
            <div className="col-6">
              <div className="text-center text-success fw-bold"> Top mua ròng</div>
              {list_green}
            </div>
            <div className="col-6">
              <div className="text-center text-danger fw-bold"> Top bán ròng</div>
              {list_red}
            </div>
          </div>)
  return(
    <div>
      {list}
    </div>
  )
}

export default TwoHalfBarChart;