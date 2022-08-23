import './App.css';
import SidebarWithHeader from './components/sidebar';
//import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { Route, Routes, BrowserRouter } from "react-router-dom";
import HomePage from './components/homepage/HomePage';
import CompanyValuation from './components/companyValuation';




function App() {
    return (
        // This is the Single-Page routing
        <BrowserRouter>
            {/* The Sidebar and Header is fixed on every page */}
            <SidebarWithHeader>
                <Routes>
                    <Route path="/" element={<HomePage/>} />

                    <Route path="/xxx" element={ <div> Nothing here yet! </div> } />
                    <Route path="/company/:company_symbol" element={<CompanyValuation />} />

                </Routes>

            </SidebarWithHeader>
        </BrowserRouter>

    );
}

export default App;
