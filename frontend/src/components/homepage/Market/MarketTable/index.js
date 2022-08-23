import 'react-tabulator/css/tabulator_bootstrap3.css';
import { ReactTabulator } from 'react-tabulator'



export const MarketTable = ({ data, current_market, setMarket }) => {
    const columns = [
        {
            title: "Thị trường", 
            field: "market_symbol", 
            width: 150, 
            cellClick: (e, cell) => {
                setMarket(cell.getData().market_symbol);
            },
            formatter: (cell, formatterParams, onRendered) => {
                //cell - the cell component
                //formatterParams - parameters set for the column
                //onRendered - function to call when the formatter has been rendered
                let cell_market = cell.getValue();
                if (cell_market === current_market) {
                    cell.getElement().style.fontWeight="bold";
                }
                return cell.getValue();
            },
        },
        { title: "Giá", field: "price_close" },
        { title: "%D", field: "day", hozAlign: "center" },
        { title: "%W", field: "week", hozAlign: "center" },
        { title: "%M", field: "month" },
        { title: "%3M", field: "three_month" },
        { title: "Y", field: "year", width: 300 }
    ];
    const market_table = []
    if (data) {

        // Đây là hàm để group by key
        let groupBy = function (xs, key) {
            return xs.reduce(function (rv, x) {
                (rv[x[key]] = rv[x[key]] || []).push(x);
                return rv;
            }, {});
        };
        let groupedByMarket = groupBy(data, 'market_symbol')

        const markets = Object.keys(groupedByMarket)


        markets.forEach(key => {
            let by_market = groupedByMarket[key]

            by_market = by_market.map(item => ({
                ...item,
                trading_date: new Date(item.trading_date).getTime()
            }));

            by_market.sort((a, b) => b.trading_date - a.trading_date);

            // const trading_date = by_market.map(item => item.trading_date);
            const price_close = by_market.map(item => item.price_close);

            const priceDiff = (i) => {
                return ((price_close[0] - price_close[i]) / price_close[i] * 100).toFixed(2) + "%"
            };

            const market_row = {
                market_symbol: key,
                price_close: price_close[0],
                day: priceDiff(1),
                week: priceDiff(5),
                month: priceDiff(20),
                three_month: priceDiff(60),
                year: priceDiff(720)
            };

            market_table.push(market_row)
        })

    }



    return (
        data ? <ReactTabulator
            data={market_table}
            columns={columns}
            layout="fitDataFill"
            height="350px"
        /> : <div> Data is loading... </div>
    );
}
