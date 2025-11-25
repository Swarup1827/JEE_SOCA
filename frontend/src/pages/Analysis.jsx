import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import { motion } from 'framer-motion';

const Analysis = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { results } = location.state || {};

    if (!results) {
        return (
            <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
                <h2 className="text-2xl font-bold text-gray-800 mb-4">No results found</h2>
                <button
                    onClick={() => navigate('/')}
                    className="bg-indigo-600 text-white px-6 py-2 rounded-lg"
                >
                    Go Home
                </button>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4">
            <div className="max-w-4xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-white rounded-2xl shadow-xl overflow-hidden"
                >
                    <div className="bg-indigo-600 p-8 text-white">
                        <h1 className="text-3xl font-bold">Your SOCA Analysis</h1>
                        <p className="mt-2 text-indigo-100">AI-Generated Personal Performance Report</p>
                    </div>

                    <div className="p-8">
                        <ReactMarkdown
                            components={{
                                h1: ({ node, ...props }) => <h1 className="text-4xl font-extrabold text-indigo-900 mb-6 border-b-2 border-indigo-100 pb-2" {...props} />,
                                h2: ({ node, ...props }) => <h2 className="text-3xl font-bold text-gray-800 mt-8 mb-4" {...props} />,
                                h3: ({ node, ...props }) => <h3 className="text-2xl font-bold text-indigo-700 mt-6 mb-3" {...props} />,
                                strong: ({ node, ...props }) => <strong className="font-extrabold text-lg text-gray-900" {...props} />,
                                ul: ({ node, ...props }) => <ul className="list-disc pl-6 space-y-2 mb-4 text-gray-700" {...props} />,
                                li: ({ node, ...props }) => <li className="leading-relaxed" {...props} />,
                                p: ({ node, ...props }) => <p className="mb-4 text-gray-700 leading-relaxed" {...props} />,
                            }}
                        >
                            {results}
                        </ReactMarkdown>
                    </div>

                    <div className="bg-gray-50 p-8 border-t border-gray-100 flex justify-center">
                        <button
                            onClick={() => navigate('/')}
                            className="bg-indigo-600 text-white px-8 py-3 rounded-full font-bold shadow-lg hover:bg-indigo-700 transition-colors"
                        >
                            Take Another Test
                        </button>
                    </div>
                </motion.div>
            </div>
        </div>
    );
};

export default Analysis;
