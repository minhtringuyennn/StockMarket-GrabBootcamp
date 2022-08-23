import { MarketPriceChart } from "./MarketPriceChart";
import { MarketTable } from "./MarketTable";
import { SplitView } from "../../splitview";
import ApiCaller from "../../../api/ApiCaller";
import { useEffect, useState } from 'react';

function Market() {
    const url = 'http://139.180.215.250/api/market-price?format=json';
    const table_data = []
    const [data, setData] = useState(null);

    const [current_market, setMarket ] = useState("VN-INDEX")

    async function fetchData() {
        const res = await ApiCaller(url);
        setData(res)
    }

    useEffect(() => {
        fetchData();
    }, []);



    return (
        <SplitView
            left={<MarketPriceChart data={data} current_market={current_market}/>}
            right={<MarketTable data={data} current_market={current_market} setMarket={setMarket} />}
        />
    )
}

export default Market;