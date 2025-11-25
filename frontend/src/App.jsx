import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Test from './pages/Test';
import Analysis from './pages/Analysis';

function App() {
    return (
        <Router>
            <div className="min-h-screen bg-gray-50">
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/test" element={<Test />} />
                    <Route path="/analysis" element={<Analysis />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
