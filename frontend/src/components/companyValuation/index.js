import { Spinner, Image, Text } from "@chakra-ui/react";
import axios from "axios";
import React, { useEffect, useState } from "react";
import { Col, Container, Row } from "react-bootstrap";
import { useParams } from "react-router-dom";

function CompanyValuation() {
    const [company, setCompany] = useState({});
    let { company_symbol } = useParams();

    const fetchCompanyInfo = async () => {
        axios
            .all([
                axios.get(`http://139.180.215.250/api/company/${company_symbol}`),
                axios.get(
                    `http://139.180.215.250/api/stock-price/${company_symbol}?start_date=${new Date().toISOString().split("T")[0]
                    }`
                ),
            ])
            .then(
                axios.spread((...responses) => {
                    const data = responses.map((res, idx) => {
                        return res.data;
                    })
                    console.log(data)
                    setCompany(Object.assign({}, ...data));
                })
            )
            .catch((e) => {
                console.log(e);
            });
    };

    useEffect(() => {
        fetchCompanyInfo();
    }, []);

    const renderStats = (stats) => {
        return (
            <Col
                xs={2}
                className="flex justify-between w-4/12 px-4 border-start border-secondary"
            >
                {stats.map((stat, idx) => {
                    return <Row key={idx}>{stat}</Row>;
                })}
            </Col>
        );
    };

    if (!company) {
        return (
            <Spinner
                thickness="4px"
                speed="0.65s"
                emptyColor="gray.200"
                color="blue.500"
                size="xl"
            />
        );
    } else {
        console.log(company)
        return (
            <Container fluid className="p-0 mt-0">
                <Row className="flex justify-between items-center pb-4 ps-1 space-x-10 shadow p-3 mb-5 bg-white">
                    <Col xs={1}>
                        <Image
                            objectFit="contain"
                            src={`https://wichart.vn/images/logo-dn/${company_symbol}.jpeg`}
                        />
                    </Col>
                    <Col xs={4}>
                        <Row>
                            <Text fontWeight="bold">
                                {company.company_name} ({company.symbol}){" "}
                            </Text>
                        </Row>
                        <Row>
                            <Text>{company.floor_code}</Text>
                        </Row>
                        <Row>
                            <Text>{company.industry_name}</Text>
                        </Row>
                    </Col>
                    {renderStats(["Vốn hóa", "KLGD TB15D", "KLCP lưu hành"])}
                    {renderStats(["EPS (D)", "P/E (D)", "PEG"])}
                    {renderStats(["Book value (D)", "P/B (D)", "Tỷ lệ cổ tức"])}
                </Row>
                <Row></Row>
            </Container>
        );
    }
}

export default CompanyValuation;
