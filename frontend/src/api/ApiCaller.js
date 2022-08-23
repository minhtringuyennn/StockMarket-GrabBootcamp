
import axios from 'axios';

async function ApiCaller(url) {

    const res = await axios.get(url)

    return res.data
}

export default ApiCaller;
