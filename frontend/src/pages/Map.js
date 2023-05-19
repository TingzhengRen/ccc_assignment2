
import React,{useState} from 'react';
import 'leaflet/dist/leaflet.css';
import { MapContainer, TileLayer, GeoJSON} from 'react-leaflet';
import data from '../data_process/city_geo_data.json';
import './Map.css';

//import 'bootstrap/dist/css/bootstrap.min.css';
const features = data.features

const Map = ()=>{
    const [onselect, setOnselect] = useState({});

    const highlightFeature = (e=> {
        var layer = e.target;
        const { suburb_name, count } = e.target.feature.properties;
        setOnselect({
            suburb:suburb_name,
            density: count
        });
        layer.setStyle({
            weight: 2,
            color:"#DF1995",
            fillOpacity: 4
        });
    });
    const resetHighlight= (e =>{
        setOnselect({});
        e.target.setStyle(style(e.target.feature));
    })
    const onEachFeature= (feature, layer)=> {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
        });
    }
    const mapPolygonColorToDensity=(density => {
        return density > 2000
            ? '#800026'
            : density > 1000
            ? '#BD0026'
            : density > 500
            ? '#FC4E2A'
            : density > 5
            ? '#FD8D3C'
            : density > 1
            ? '#FEB24C' 
            : '#FFEDA0';
    })
    const style = (feature => {
        return ({
            fillColor: mapPolygonColorToDensity(feature.properties.count),
            weight: 1,
            opacity: 1,
            color: 'white',
            dashArray: '2',
            fillOpacity: 0.6
        });
    });

    const mapStyle = {
        height: '82vh',
        width: '100%',
        margin: '10',
    }
    const feature = features.map(feature=>{
        return(feature);
    });
    return(
        <div className="map">
            {!onselect.suburb && (
            <div className="census-info-hover">
                <strong>Tweets density</strong>
                <p>Hover on each suburb for more details</p>
            </div>
            )}
            {onselect.suburb && (
                <ul className="census-info">
                    <li><strong>{onselect.suburb}</strong></li><br/>
                    <li>Tweets density about employment: {onselect.density} tweets</li>
                </ul>
            )}
            <MapContainer zoom={8}
                scrollWheelZoom={true} 
                style={mapStyle} 
                center={[-37.286389, 144.517223]}>
                <TileLayer
                    attribution="Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL."
                    url="https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png"
                />
                {feature && (
                    <GeoJSON data={feature} 
                    style={style} 
                    onEachFeature={onEachFeature}/>
                )}
            </MapContainer>
            <div className="legend">
              <div style={{ "--color": '#800026' }}>2000+</div>
              <div style={{ "--color": '#BD0026' }}>1000 - 1999</div>
              <div style={{ "--color": '#FC4E2A' }}>500 - 999</div>
              <div style={{ "--color": '#FD8D3C' }}>5 - 499</div>
              <div style={{ "--color": '#FEB24C'}}>1 - 4</div>
              <div style={{ "--color": '#FFEDA0'}}>0</div>
            </div>
        </div>

    )
}
export default Map;