import React from 'react';
import './App.css';
import Navbar from "./Component/Navigation/Navbar";
import Footer from "./Component/Navigation/Footer";
import FilterBar from "./Component/FilterBar/FilterBar";
import HomePage from "./Component/HomePage/HomePage";

function App() {
  return (
    <>
      <Navbar/>
        <FilterBar/>
        <HomePage/>
      <Footer/>
    </>
  );
}

export default App;
