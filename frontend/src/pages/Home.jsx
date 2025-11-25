import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

const Home = () => {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600 text-white p-4">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="text-center max-w-2xl"
            >
                <h1 className="text-5xl font-bold mb-6">JEE Aspirant SOCA Analysis</h1>
                <p className="text-xl mb-8 text-indigo-100">
                    Discover your Strengths, Opportunities, Challenges, and get a personalized Action Plan using AI.
                </p>

                <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 mb-8 text-left">
                    <h3 className="text-lg font-semibold mb-4">What you'll get:</h3>
                    <ul className="space-y-2">
                        <li className="flex items-center">✅ Comprehensive Subject Analysis</li>
                        <li className="flex items-center">✅ AI-Driven Insights</li>
                        <li className="flex items-center">✅ Personalized Study Plan</li>
                        <li className="flex items-center">✅ Well-being & Time Management Assessment</li>
                    </ul>
                </div>

                <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => navigate('/test')}
                    className="bg-white text-indigo-600 px-8 py-4 rounded-full font-bold text-lg shadow-lg hover:shadow-xl transition-all"
                >
                    Start Assessment
                </motion.button>
            </motion.div>
        </div>
    );
};

export default Home;
