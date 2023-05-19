import React, { useState, useEffect } from 'react';
import ReactEcharts from 'echarts-for-react';

export default function Home() {
  const [data, setData] = useState(null);

  async function fetchData() {
    try {
      const apiUrl = 'http://127.0.0.1:8080//api_4/broke_line'; // Change the API URL here
      const response = await fetch(apiUrl);
      const responseData = await response.json();
      setData(responseData.data); // Access the 'data' property of the response
    } catch (error) {
      console.error(error);
    }
  }

  useEffect(() => {
    fetchData();
  }, []);

  const option = {
    title: {
      text: 'Line'
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['VIC Female', 'Melbourne Female', 'VIC Male', 'Melbourne Male'] // Add legend for the new lines
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    toolbox: {
      feature: {
        saveAsImage: {}
      }
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['2011-2012', '2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: 'VIC Female',
        type: 'line',
        data: data ? data[0] : [] // Use the first array from the received data
      },
      {
        name: 'Melbourne Female',
        type: 'line',
        data: data ? data[1] : [] // Use the second array from the received data
      },
      {
        name: 'VIC Male',
        type: 'line',
        data: data ? data[2] : [] // Use the third array from the received data
      },
      {
        name: 'Melbourne Male',
        type: 'line',
        data: data ? data[3] : [] // Use the fourth array from the received data
      }
    ]
    
  };

  return (
    <div>
      <h1>Median employment income for male and female</h1>
      {data ? (
        <ReactEcharts option={option} style={{ width: '100%', height: '600px' }} />
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}
