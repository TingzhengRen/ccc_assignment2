import Navbar from './Navbar';
import Footer from './Footer'
import GroupInfo from'./pages/GroupInfo'
import Home from './pages/Home'
import Map from './pages/Map'
import Map1 from './pages/Map1'
import Visualone from './pages/VisualOne'
import Visualtwo from './pages/VisualTwo'

import{ Route, Routes } from 'react-router-dom'

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path='/group' element={<GroupInfo />} />
        <Route path='/' element={<Home />} />
        <Route path='/map' element={<Map />} />
        <Route path='/map1' element={<Map1 />} />
        <Route path='/visualone' element={<Visualone />} />
        <Route path='/visualtwo' element={<Visualtwo />} />
      </Routes>
      <Footer />
    </>

  );
}

export default App;
