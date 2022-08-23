import React from "react";
import TreeMap from "./TreeMap";
import TwoHalfBarChart from "./TwoHalfBarChart";

function TwoChart() {
    return (
        <div className="row">
            <div className="col-lg-7 col-12">
                <TreeMap />
            </div>
            <div className="col-lg-5 col-12">
                <TwoHalfBarChart />
            </div>
        </div>
    )
};

export default TwoChart