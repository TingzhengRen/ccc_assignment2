import React, { Component } from "react";
import ReactEcharts from "echarts-for-react";
import { Row, Col, Input } from "antd";
import "echarts-wordcloud";

export default class Wordcloud extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: null,
      keyword: ""
    };
  }

  componentDidMount() {
    this.fetchData();
  }

  fetchData = async () => {
    try {
      const { keyword } = this.state;
      const apiUrl = `http://127.0.0.1:8080/api_0/${keyword}`;
      const response = await fetch(apiUrl);
      const responseData = await response.json();
      this.setState({ data: responseData.data });
    } catch (error) {
      console.error(error);
    }
  };

  handleInputChange = (e) => {
    this.setState({ keyword: e.target.value });
  };

  handleSearch = () => {
    this.fetchData();
  };

  wordOption = () => {
    const { data } = this.state;

    let wordData = [];

    if (data) {
      wordData = data.map((item, index) => ({
        name: item.key,
        value: item.value,
      }));
    }

    let option = {
      backgroundColor: "#fff",
      tooltip: {
        pointFormat: "{series.name}: <b>{point.percentage:.1f}%</b>",
      },
      series: [
        {
          type: "wordCloud",
          gridSize: 1,
          sizeRange: [8, 55],
          rotationRange: [-45, 0, 45, 90],
          textStyle: {
            normal: {
              color: () =>
                `hsl(${Math.floor(Math.random() * 360)}, 70%, 50%)`, // Random color for each word
              opacity: 1,
              fontWeight: "bold",
              fontFamily: "Arial, sans-serif",
            },
          },
          left: "center",
          top: "center",
          right: null,
          bottom: null,
          width: "200%",
          height: "200%",
          data: wordData,
        },
      ],
    };
    return option;
  };

  render() {
    return (
      <div style={{ marginTop: "100px", width: "100%" }}>
        <Row>
          <Col md={24}>
            <Input
              placeholder="Type a word"
              onChange={this.handleInputChange}
              style={{ width: "300px", marginBottom: "10px" }}
              onPressEnter={this.handleSearch}
            />
            <ReactEcharts
              option={this.wordOption()}
              style={{ height: "400px" }} // Adjust the height as needed
              opts={{ renderer: "svg" }} // Use SVG renderer to avoid potential display issues
            />
          </Col>
        </Row>
      </div>
    );
  }
}
